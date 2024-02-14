from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OptionsData:
    data_dict: dict = field(default_factory=lambda: {
        "Blog Remote Url": "",
        "Blog Local Url": "",
        "Port": 4000,
        "Blog Root Path": "",
        "Posts Path": "",
        "Assets Path": "",
        "News Page Path": "",
        "Weather Page Path": "",
        "Need Clan Up On Publish": False,
        "Update News On Publish": False,
        "Update Weather On Publish": False,
        "Auto Publish at boot": False,
        "Publish Timeout Limit": 200
    })


@dataclass
class NavigationData:
    tags: list = field(default_factory=list)
    categories: list = field(default_factory=list)
    lastUpdateTime: int = 0
    postsData: dict = field(default_factory=dict)

    def update_data(self, new_path_list: list):
        need_del = []
        for path in self.postsData.keys():
            if not new_path_list.__contains__(path):
                need_del.append(path)
        for delPath in need_del:
            del self.postsData[delPath]

        self.update_statistic_data()
        self.lastUpdateTime = int(datetime.now().timestamp())

    def update_statistic_data(self):
        self.tags.clear()
        self.categories.clear()
        for postData in self.postsData.values():
            for tag in postData.tags:
                if not self.tags.__contains__(tag):
                    self.tags.append(tag)
            for category in postData.categories:
                if not self.categories.__contains__(category):
                    self.categories.append(category)


@dataclass
class PostData:
    title: str = ""
    path: str = ""
    categories: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    size: int = 0
    creationTime: int = 0
    lastUpdateTime: int = 0
