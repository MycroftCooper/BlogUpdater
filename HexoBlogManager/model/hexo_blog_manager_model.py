import dataclasses
import os
import ast
import time
import json
import subprocess
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from .hexo_cmd import HexoCmd
from view.error_dialog import ErrorDialog
from .model_data import OptionsData
from .model_data import (PostData, NavigationData)


class HexoBlogManagerModel:
    OptionsDataFilePath = "HexoBlogMgrOptionsData.json"
    NavigationDataFilePath = "HexoBlogMgrNavigationCacheData.json"

    options_data: OptionsData
    navigation_data: NavigationData

    def __init__(self):
        self.load_options_data()

    # region Options
    def load_options_data(self):
        options_file = Path(self.OptionsDataFilePath)
        if options_file.exists():
            with open(options_file, 'r', encoding='utf-8') as file:
                options_dict = json.load(file)
                self.options_data = OptionsData(**options_dict)
        else:
            self.options_data = OptionsData()
        HexoCmd.set_root(self.options_data.data_dict['Blog Root Path'])

    def save_options_data(self):
        try:
            with open(self.OptionsDataFilePath, 'w', encoding='utf-8') as file:
                options_dict = dataclasses.asdict(self.options_data)
                json.dump(options_dict, file, indent=4)
        except Exception as e:
            ErrorDialog.log_error(e, "model>saveOptionsData")

    # endregion

    # region Navigation
    def load_navigation_data(self):
        navigation_file = Path(self.NavigationDataFilePath)
        if navigation_file.exists():
            try:
                with open(navigation_file, 'r', encoding='utf-8') as file:
                    navigation_file_data = json.load(file)
                    # 单独处理 postsData
                    posts_data = {k: PostData(**v) for k, v in navigation_file_data.get('postsData', {}).items()}
                    # 更新 postsData
                    navigation_file_data['postsData'] = posts_data
                    self.navigation_data = NavigationData(**navigation_file_data)
            except Exception as e:
                ErrorDialog.log_error(e, "model>loadNavigationData")
        else:
            self.navigation_data = NavigationData()
            self.scan_all_post()

    def save_navigation_data(self):
        try:
            with open(self.NavigationDataFilePath, 'w', encoding='utf-8') as file:
                navigation_dict = dataclasses.asdict(self.navigation_data)
                # 仅将 PostData 实例转换为字典
                navigation_dict['postsData'] = {k: dataclasses.asdict(v) if isinstance(v, PostData) else v
                                                for k, v in self.navigation_data.postsData.items()}
                json.dump(navigation_dict, file, indent=4)
        except Exception as e:
            ErrorDialog.log_error(e, "model>saveNavigationData")

    def scan_all_post(self):
        last_scan_time = self.navigation_data.lastUpdateTime
        post_path_list = self.__load_all_post_path()
        post_data_dict = self.navigation_data.postsData
        for post_path in post_path_list:
            modification_time = os.path.getmtime(post_path)
            long_time = int(modification_time)  # 转换为整数
            is_scanned = post_path in post_data_dict
            if is_scanned and long_time < last_scan_time:  # 没有变动，可以不扫描更新
                continue

            if is_scanned:
                del post_data_dict[post_path]
            post_data = PostData.scan_post_data(post_path)
            post_data_dict[post_path] = post_data
        self.navigation_data.update_data(post_path_list)
        self.save_navigation_data()

    def __load_all_post_path(self):
        folder_path = self.options_data.data_dict["Posts Path"]
        if not os.path.exists(folder_path):
            ErrorDialog.log_error(f"Folder path '{folder_path}' does not exist.", "model>loadAllPostPath")
            return []
        md_file_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    md_file_path = os.path.join(root, file)
                    md_file_paths.append(md_file_path)
        return md_file_paths

    # endregion

    # region Write
    def create_new_post(self, title: str):
        is_success, output_str = False, ""
        std_err = b""  # 初始化 std_err

        try:
            std_out, std_err = HexoCmd.new(title)
            output_str = std_out.decode("utf-8")
            is_success = True
        except Exception as e:
            if std_err:  # 检查 std_err 是否已赋值
                output_str = std_err.decode("utf-8")

        return is_success, output_str

    def open_post(self, title: str):
        HexoCmd.open(title)
    # endregion

    def publish_blog(self, is_remote: bool):
        time_start = time.time()

        self.__update_news_and_weather()

        blog_path = self.options_data.blog_root_path
        os.chdir(blog_path)
        if self.options_data.need_clan_up:
            os.system("hexo clean")

        if is_remote:
            os.system("hexo d")
            return
        os.system("hexo g")
        os.system("hexo s")
        time_end = time.time()
        print('\n\n>>>Done!<<<\n总用时>', time_end - time_start)

    def open_blog(self, is_remote: bool):
        if is_remote:
            webbrowser.open_new(self.options_data.blog_remote_url)
        else:
            webbrowser.open_new(self.options_data.blog_local_url)

    def __update_news_and_weather(self):
        if self.options_data.update_news:
            pass
            # todo: 爬取新闻

        if self.options_data.update_weather:
            pass
            # todo: 爬取天气
