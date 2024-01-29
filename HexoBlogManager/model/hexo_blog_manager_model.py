import dataclasses
import os
import ast
import time
import json
import threading
import webbrowser
from pathlib import Path
from .model_data import OptionsData
from .model_data import PostData

class HexoBlogManagerModel():
    options_data: OptionsData
    posts_data: dict
    
    def loadOptionsData(self):
        options_file = Path('HexoBlogMgrOptionsData.json')
        if options_file.exists():
            with open(options_file, 'r', encoding='utf-8') as file:
                options_dict = json.load(file)
                self.options_data = OptionsData(**options_dict)
        else:
            self.options_data = OptionsData()
            self.saveOptionsData()
    
    def saveOptionsData(self):
        with open('HexoBlogMgrOptionsData.json', 'w', encoding='utf-8') as file:
            options_dict = dataclasses.asdict(self.options_data)
            json.dump(options_dict, file, indent=4)
    
    def scanAllPost(self):
        pass
    
    def createNewPost(self, title: str, temp: str):
        if not temp:
            os.system(f"hexo new {title}")
        else:
            os.system(f"hexo new {temp} {title}")
    
    def __updateNewsAndWeather(self):
        if self.options_data.update_news:
            todo: 爬取新闻
        
        if self.options_data.update_weather:
            todo: 爬取天气
            
    
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