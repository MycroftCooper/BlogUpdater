import re
import os
from dataclasses import dataclass, field
from datetime import datetime

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
    tags: list = field(default_factory=list)
    templates: list = field(default_factory=list)
    categorizations: list = field(default_factory=list)
    lastUpdateTime: int = 0
    postsData : dict = field(default_factory=dict)
    
    def addTag(self, tagStr:str):
        if not self.tags.__contains__(tagStr):
            self.tags.append(tagStr)
        

@dataclass
class PostData:
    name: str = ""
    path: str = ""
    categorization: str = ""
    tags: list = field(default_factory=list)
    size: int = 0
    creation_time: int = 0
    lastUpdateTime: int = 0
    
    @staticmethod
    def scanPostData(path):
        matadata_str = PostData.__getMetadataStr(path)
        data = PostData.__parseMetadata(matadata_str, path)
        return data

    @staticmethod
    def __getMetadataStr(path):# 提取属性字段
        with open(path, 'r', encoding='utf-8') as file:
            metadata_str = ''
            is_metadata_section = False
            for line in file:
                if line.strip() == '---':
                    if is_metadata_section:
                        break
                    else:
                        is_metadata_section = True
                        continue
                if is_metadata_section:
                    metadata_str += line
            return metadata_str

    @staticmethod
    def __parseMetadata(metadata_str, path):
        post_data = PostData(path=path)

        title_pattern = r'^title:\s*(.*)$'
        date_pattern = r'^date:\s*(.*)$'
        categories_pattern = r'^categories:\s*\n\s*- (.*)$'
        tags_pattern = r'^tags:\s*\n(^\s*- .*$)+'
        tag_pattern = r'^\s*- (.*)$'

        for line in metadata_str.split('\n'):
            title_match = re.match(title_pattern, line, re.M)
            if title_match:
                post_data.name = title_match.group(1).strip()

            date_match = re.match(date_pattern, line, re.M)
            if date_match:
                date_str = date_match.group(1).strip()
                # 解析日期时间字符串
                try:
                    post_data.creation_time = int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp())
                except ValueError:
                    post_data.creation_time = 0

            categories_match = re.match(categories_pattern, line, re.M)
            if categories_match:
                post_data.categorization = categories_match.group(1).strip()

            tags_match = re.search(tags_pattern, metadata_str, re.M)
            if tags_match:
                tags = re.findall(tag_pattern, tags_match.group(0), re.M)
                post_data.tags = [tag.strip() for tag in tags]

        # 获取文件最后修改时间
        post_data.lastUpdateTime = int(os.path.getmtime(path))

        # 获取文件大小
        try:
            post_data.size = os.path.getsize(path)  # 文件大小，以字节为单位
        except OSError:
            post_data.size = -1
        return post_data