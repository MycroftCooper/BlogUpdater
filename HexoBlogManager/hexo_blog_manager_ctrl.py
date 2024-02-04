import os
import sys
import subprocess
from datetime import datetime

from view import *
from model import *


class HexoBlogManagerCtrl:
    def __init__(self, view: HexoBlogManagerView, model: HexoBlogManagerModel):
        self.view = view
        self.model = model
        self.bind_view_signal()
        self.init_options_data()
        self.init_navigation_data()

    def bind_view_signal(self):
        navigate_tab = self.view.navigateTab
        navigate_tab.navigateUpdateViewSignal.connect(self.update_navigation_view)
        navigate_tab.navigateUpdatePostDataSignal.connect(self.update_navigation_data)

        options_tab = self.view.optionsTab
        options_tab.reloadOptionsDataSignal.connect(self.reload_options_data)
        options_tab.saveOptionsDataSignal.connect(self.save_options_data)
        options_tab.openHexoConfigSignal.connect(self.open_hexo_config_file)

    # region Write Ctrl
    def refresh_config(self):
        pass

    def create_new_post(self):
        pass

    # endregion

    # region Publish Ctrl
    def publish(self, is_remote: bool):
        pass

    def open_blog(self, is_remote: bool):
        pass

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

        if navigation.infoSortBy != SortBy.NONE:
            for group, posts in view_dict.items():
                sorted_posts = self.__sort_posts(posts, navigation.infoSortBy, navigation.isReverse)
                view_dict[group] = sorted_posts

        navigation.postInfoViewDict = view_dict

        navigation.update_posts_info()

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
