import os
import sys
import subprocess
import webbrowser
from datetime import datetime

import model
from view import *
from model import *


class HexoBlogManagerCtrl:
    def __init__(self, view: HexoBlogManagerView, mgr_model: HexoBlogManagerModel):
        self.view = view
        self.model = mgr_model
        self.bind_view_signal()
        self.init_options_data()
        self.init_navigation_data()
        self.init_write_tab()

    def bind_view_signal(self):
        navigate_tab = self.view.navigateTab
        navigate_tab.navigateUpdateViewSignal.connect(self.update_navigation_view)
        navigate_tab.navigateUpdatePostDataSignal.connect(self.update_navigation_data)
        navigate_tab.navigateOpenPostSignal.connect(lambda path: PostHelper.open_post(path))
        navigate_tab.navigateEditPostMetadataSignal.connect(lambda data: self.editor_post_properties(data["path"], data))
        navigate_tab.navigateDeletePostSignal.connect(self.delete_post)

        options_tab = self.view.optionsTab
        options_tab.reloadOptionsDataSignal.connect(self.reload_options_data)
        options_tab.saveOptionsDataSignal.connect(self.save_options_data)
        options_tab.openHexoConfigSignal.connect(self.open_hexo_config_file)

        write_tab = self.view.writeTab
        write_tab.refreshConfigSignal.connect(self.refresh_write_tab_config)
        write_tab.createNewPostSignal.connect(self.create_new_post)
        write_tab.importNewPostSignal.connect(self.import_posts)

        publish_tab = self.view.publishTab
        publish_tab.publishSignal.connect(self.publish)
        publish_tab.openBlogSignal.connect(self.open_blog)

    # region Write Ctrl
    def init_write_tab(self):
        write_tab = self.view.writeTab
        model_data = self.model.navigation_data
        write_tab.existentCategoryList = model_data.categories
        write_tab.existentTagList = model_data.tags
        write_tab.update_config()

    def refresh_write_tab_config(self):
        self.update_navigation_data()
        self.init_write_tab()

    def create_new_post(self, new_post_info_dict: dict):
        if not new_post_info_dict.__contains__("title") or not new_post_info_dict["title"]:
            ErrorDialog.log_error(f"Post title cant be null!", "ctrl>create_new_post")
            return

        posts_data = self.model.navigation_data.postsData
        title = new_post_info_dict["title"]
        path = PostHelper.get_post_path(title)
        if posts_data.__contains__(path):
            ErrorDialog.log_error(f"Post '{path}' already exist.", "ctrl>create_new_post")
            return

        is_success, output_str = self.model.create_new_post(title)
        self.view.writeTab.std_output_text.clear()
        self.view.writeTab.std_output_text.setText(output_str)

        if not is_success:
            return
        new_post_info_dict["path"] = path
        self.editor_post_properties(path, new_post_info_dict)
        PostHelper.open_post(path)

    def editor_post_properties(self, path: str, post_info_dict: dict):
        self.model.change_post_meta_data(path, post_info_dict)
        self.refresh_write_tab_config()


    def import_posts(self, posts_list: list):
        pass

    # endregion

    # region Publish Ctrl
    def publish(self, is_remote: bool, is_need_clean: bool):
        output_text_edit = self.view.publishTab.publish_output
        output_text_edit.clear()

        if is_need_clean:
            std_output, std_err = HexoCmdHelper.clean()
            output_text_edit.append("Clean Output:\n" + std_output.decode() + "\n" + std_err.decode())

        std_output, std_err = HexoCmdHelper.generate()
        output_text_edit.append("Generate Output:\n" + std_output.decode() + "\n" + std_err.decode())

        if is_remote:
            std_output, std_err = HexoCmdHelper.deploy()
            output_text_edit.append("Deploy Output:\n" + std_output.decode() + "\n" + std_err.decode())
        else:
            std_output, std_err = HexoCmdHelper.server(self.model.options_data.data_dict["Port"])
            output_text_edit.append("Server Output:\n" + std_output.decode() + "\n" + std_err.decode())

    def open_blog(self, is_remote: bool):
        data_dict = self.model.options_data.data_dict

        if is_remote:
            if not data_dict.__contains__("Blog Remote Url") or not data_dict["Blog Remote Url"]:
                ErrorDialog.log_error("options didn't set Blog Remote Url!", "ctrl>open_blog")
                return
            target_url = data_dict["Blog Remote Url"]
        else:
            if not data_dict.__contains__("Blog Local Url") or not data_dict["Blog Local Url"]:
                ErrorDialog.log_error("options didn't set Blog Local Url!", "ctrl>open_blog")
                return
            target_url = data_dict["Blog Local Url"]

        webbrowser.open(target_url)

    # endregion

    # region Navigation Ctrl
    def init_navigation_data(self):
        self.model.load_navigation_data()
        self.model.scan_all_post()
        self.view.navigateTab.on_need_update_view()

    def update_navigation_data(self):
        self.model.scan_all_post()
        self.update_navigation_view()

    def update_navigation_view(self):
        navigation = self.view.navigateTab
        data = self.model.navigation_data
        posts_data = data.postsData.values()

        if navigation.searchStr:
            posts_data = self.__filter_posts(posts_data, navigation.searchStr)

        view_dict = self.__group_posts(posts_data, navigation.infoGroupBy)

        for group, posts in view_dict.items():
            sorted_posts = self.__sort_posts(posts, navigation.infoSortBy, navigation.isReverse)
            view_dict[group] = sorted_posts

        navigation.postInfoViewDict = view_dict

        navigation.update_posts_info()

    def delete_post(self, path):
        if not self.model.delete_post(path):
            return
        self.update_navigation_view()

    @staticmethod
    def __filter_posts(posts, search_str):
        # 初始化结果数组
        result = []

        # 遍历所有帖子
        for post in posts:
            # 检查名称、类别和标签是否包含搜索字符串
            if search_str.lower() in post.title.lower() or \
                    any(search_str.lower() in category.lower() for category in post.categories) or \
                    any(search_str.lower() in tag.lower() for tag in post.tags):
                result.append(post)

        return result

    def __group_posts(self, posts, group_by):
        grouped_posts = {}
        if group_by == GroupBy.NONE:  # 不进行分组，所有帖子都在同一组
            grouped_posts["NONE"] = list(posts)
            return grouped_posts

        for post in posts:
            if group_by == GroupBy.Category:
                for category in self.model.navigation_data.categories:
                    if category in post.categories:
                        grouped_posts.setdefault(category, []).append(post)

            elif group_by == GroupBy.Tag:
                for tag in self.model.navigation_data.tags:
                    if tag in post.tags:
                        grouped_posts.setdefault(tag, []).append(post)

            elif group_by in [GroupBy.CreationTime, GroupBy.LastUpdateTime]:
                if group_by == GroupBy.CreationTime:
                    group_by_str = "creationTime"
                else:
                    group_by_str = "lastUpdateTime"
                post_time = getattr(post, group_by_str)
                date_key = datetime.fromtimestamp(post_time).strftime('%Y-%m-%d')
                grouped_posts.setdefault(date_key, []).append(post)

        return grouped_posts

    @staticmethod
    def __sort_posts(posts, sort_by, is_reverse):
        sorted_posts = posts
        # 根据不同的排序标准进行排序
        if sort_by == SortBy.Title:
            sorted_posts = sorted(posts, key=lambda post: post.title, reverse=is_reverse)
        elif sort_by == SortBy.Size:
            sorted_posts = sorted(posts, key=lambda post: post.size, reverse=is_reverse)
        elif sort_by == SortBy.CreationTime:
            sorted_posts = sorted(posts, key=lambda post: post.creation_time, reverse=is_reverse)
        elif sort_by == SortBy.LastUpdateTime:
            sorted_posts = sorted(posts, key=lambda post: post.lastUpdateTime, reverse=is_reverse)
        return sorted_posts

    # endregion

    # region Options Ctrl
    def save_options_data(self):
        data = self.view.optionsTab.data_dict
        self.model.options_data.data_dict = data
        self.model.save_options_data()

    def init_options_data(self):
        self.model.load_options_data()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.init_tab_ui()

    def reload_options_data(self):
        self.model.load_options_data()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.update_options()

    def open_hexo_config_file(self):
        folder_path = self.model.options_data.data_dict['Blog Root Path']
        file_name = '_config.yml'
        file_path = os.path.join(folder_path, file_name)
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", file_path])
            else:
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            ErrorDialog.log_error(e, "Ctrl>openHexoConfigFile")
            print(f"Error opening file: {e}")
    # endregion
