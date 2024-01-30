import dataclasses
import os
import ast
import time
import json
import threading
import webbrowser
from pathlib import Path
from .model_data import OptionsData
from .model_data import (PostData, NavigationData)
from view.error_dialog import ErrorDialog

class HexoBlogManagerModel():
    OptionsDataFilePath = "HexoBlogMgrOptionsData.json"
    NavigationDataFilePath = "HexoBlogMgrNavigationCacheData.json"

    options_data: OptionsData
    navigation_data: PostData

    def __init__(self):
        self.loadOptionsData()

    #region Options
    def loadOptionsData(self):
        options_file = Path(self.OptionsDataFilePath)
        if options_file.exists():
            with open(options_file, 'r', encoding='utf-8') as file:
                options_dict = json.load(file)
                self.options_data = OptionsData(**options_dict)
        else:
            self.options_data = OptionsData()
    
    def saveOptionsData(self):
        try:
            with open(self.OptionsDataFilePath, 'w', encoding='utf-8') as file:
                options_dict = dataclasses.asdict(self.options_data)
                json.dump(options_dict, file, indent=4)
        except Exception as e:
            ErrorDialog.logError(e, "model>saveOptionsData")
    #endregion
    
    #region Navigation
    def loadNavigationData(self):
        navigation_file = Path(self.NavigationDataFilePath)
        if navigation_file.exists():
            try:
                with open(navigation_file, 'r', encoding='utf-8') as file:
                    navigation_dict = json.load(file)
                    self.navigation_data = NavigationData(**navigation_dict)
            except Exception as e:
                ErrorDialog.logError(e, "model>loadNavigationData")
        else:
            self.scanAllPost()
            self.saveNavigationData()

    def saveNavigationData(self):
        try:
            with open(self.NavigationDataFilePath, 'w', encoding='utf-8') as file:
                navigation_dict = dataclasses.asdict(self.navigation_data)
                json.dump(navigation_dict, file, indent=4)
        except Exception as e:
            ErrorDialog.logError(e, "model>saveNavigationData")
    
    def scanAllPost(self):
        last_scan_time = self.navigation_data.lastUpdateTime
        post_path_list = self.__loadAllPostPath()
        for post_path in post_path_list:
            modification_time = os.path.getmtime(post_path)
            long_time = int(modification_time)  # 转换为整数
            if long_time < last_scan_time:# 没有变动，可以不扫描更新
                continue
            properties = self.__scanPostProperties(post_path)


    def __loadAllPostPath(self):
        folder_path = OptionsData.data_dict["Posts Path"]
        if not os.path.exists(folder_path):
            ErrorDialog.logError(f"Folder path '{folder_path}' does not exist.", "model>loadAllPostPath")
            return []
        md_file_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    md_file_path = os.path.join(root, file)
                    md_file_paths.append(md_file_path)
        return md_file_paths

    def __scanPostProperties(self, path):
        pass
    #endregion
    
    def createNewPost(self, title: str, temp: str):
        if not temp:
            os.system(f"hexo new {title}")
        else:
            os.system(f"hexo new {temp} {title}")
            
    def publishBlog(self ,isRemote:bool):
        time_start=time.time()
        
        self.__updateNewsAndWeather()
        
        blogPath = self.options_data.blog_root_path
        os.chdir(blogPath)
        if self.options_data.need_clan_up:
            os.system("hexo clean")
        
        if isRemote:
            os.system("hexo d")
            return
        os.system("hexo g")
        os.system("hexo s")
        time_end=time.time()
        print('\n\n>>>Done!<<<\n总用时>',time_end-time_start)
            
    
    def openBlog(self ,isRemote:bool):
        if isRemote:
            webbrowser.open_new(self.options_data.blog_remote_url)
        else:
            webbrowser.open_new(self.options_data.blog_local_url)

    def __updateNewsAndWeather(self):
        if self.options_data.update_news:
            todo: 爬取新闻
        
        if self.options_data.update_weather:
            todo: 爬取天气