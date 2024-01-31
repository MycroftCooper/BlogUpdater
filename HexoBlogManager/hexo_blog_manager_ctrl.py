import os
import sys
import subprocess
from datetime import datetime

from view import *
from model import *

class HexoBlogManagerCtrl():
    def __init__(self, view:HexoBlogManagerView, model:HexoBlogManagerModel):
        self.view = view
        self.model = model
        self.bindViewSignal()
        self.initOptionsData()
        self.initNavigationData()
        
    def bindViewSignal(self):
        navigateTab = self.view.navigateTab
        navigateTab.navigateUpdateViewSignal.connect(self.updateNavigationView)
        navigateTab.navigateUpdatePostDataSignal.connect(self.updateNavigationData)

        optionsTab = self.view.optionsTab
        optionsTab.reloadOptionsDataSignal.connect(self.reloadOptionsData)
        optionsTab.saveOptionsDataSignal.connect(self.saveOptionsData)
        optionsTab.openHexoConfigSignal.connect(self.openHexoConfigFile)
    
#region Write Ctrl
    def refreshConfig(self):
        pass

    def createNewPost(self):
        pass
#endregion

#region Publish Ctrl
    def publish(self, isRemote:bool):
        pass

    def openBlog(self, isRemote:bool):
        pass
#endregion

#region Navigation Ctrl
    def initNavigationData(self):
        self.model.loadNavigationData()
        self.model.scanAllPost()
        self.updateNavigationView()

    def updateNavigationData(self):
        self.model.scanAllPost()
        self.updateNavigationView()

    def updateNavigationView(self):
        navigation = self.view.navigateTab
        data = self.model.navigation_data
        postsData = data.postsData.values()

        if navigation.searchStr:
            postsData = self.filter_posts(postsData, navigation.searchStr)

        viewDict = self.__groupPosts(postsData, navigation.infoGroupBy)

        if navigation.infoSortBy != SortBy.NONE:
            for group, posts in viewDict.items():
                sorted_posts = self.__sortPosts(posts, navigation.infoSortBy)
                viewDict[group] = sorted_posts
        
        navigation.postInfoViewDict = viewDict

        navigation.updateInfoTree()

    def __filterPosts(self, posts, search_str):
        pass

    def __groupPosts(self, posts, group_by):
        grouped_posts = {}
        if group_by == GroupBy.NONE:# 不进行分组，所有帖子都在同一组
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
                post_time = getattr(post, group_by.name)
                date_key = datetime.fromtimestamp(post_time).strftime('%Y-%m-%d')
                grouped_posts.setdefault(date_key, []).append(post)

        return grouped_posts

    def __sortPosts(self, posts, sort_by):
        # 根据不同的排序标准进行排序
        if sort_by == SortBy.Name:
            sorted_posts = sorted(posts, key=lambda post: post.name)
        elif sort_by == SortBy.Size:
            sorted_posts = sorted(posts, key=lambda post: post.size)
        elif sort_by == SortBy.CreationTime:
            sorted_posts = sorted(posts, key=lambda post: post.creation_time)
        elif sort_by == SortBy.LastUpdateTime:
            sorted_posts = sorted(posts, key=lambda post: post.lastUpdateTime)
        return sorted_posts

#endregion

#region Options Ctrl
    def saveOptionsData(self):
        data = self.view.optionsTab.data_dict
        self.model.options_data.data_dict = data
        self.model.saveOptionsData()

    def initOptionsData(self):
        self.model.loadOptionsData()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.initTabUI()

    def reloadOptionsData(self):
        self.model.loadOptionsData()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.updateOptions()

    def openHexoConfigFile(self):
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
            ErrorDialog.logError(e, "Ctrl>openHexoConfigFile")
            print(f"Error opening file: {e}")
#endregion