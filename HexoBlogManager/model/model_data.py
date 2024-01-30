from dataclasses import dataclass, field
import datetime

@dataclass
class OptionsData:
    data_dict: dict = field(default_factory=lambda: {
        "Blog Remote Url": "",
        "Blog Local Url": "",
        "Blog Root Path": "",
        "Posts Path": "",
        "Assets Path": "",
        "Templates Path": "",
        "News Page Path": "",
        "Weather Page Path": "",
        "Need Clan Up On Publish": False,
        "Update News On Publish": False,
        "Update Weather On Publish": False,
        "Auto Publish at boot": False,
        "Publish Timeout Limit:": 200
    })

@dataclass
class NavigationData:
    tags: list = []
    templates: list = []
    categorizations: list = []
    lastUpdateTime: int = 0
    postsData : dict = {}

@dataclass
class PostData:
    name: str
    path: str
    categorization: str
    tags: str
    words_num: int
    creation_time: datetime
    lastUpdateTime: int