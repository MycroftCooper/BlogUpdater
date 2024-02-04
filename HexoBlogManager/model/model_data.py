import re
import os
from dataclasses import dataclass, field
from datetime import datetime
from view.error_dialog import ErrorDialog


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
    categories: list = field(default_factory=list)
    lastUpdateTime: int = 0
    postsData: dict = field(default_factory=dict)

    def update_data(self, new_path_list: list, templates_path: str):
        need_del = []
        for path in self.postsData.keys():
            if not new_path_list.__contains__(path):
                need_del.append(path)
        for delPath in need_del:
            del self.postsData[delPath]

        self.tags.clear()
        self.categories.clear()
        for postData in self.postsData.values():
            for tag in postData.tags:
                if not self.tags.__contains__(tag):
                    self.tags.append(tag)
            for category in postData.categories:
                if not self.categories.__contains__(category):
                    self.categories.append(category)

        self.templates.clear()
        if not os.path.exists(templates_path):
            print("指定的路径不存在")
            ErrorDialog.log_error(f"{templates_path}not exists!", "model>NavigationData>updateData>load templates")
            return
        for _, _, files in os.walk(templates_path):
            for file in files:
                if file.endswith(".md"):
                    filename_without_extension, _ = os.path.splitext(file)
                    self.templates.append(filename_without_extension)

        self.lastUpdateTime = int(datetime.now().timestamp())


@dataclass
class PostData:
    title: str = ""
    path: str = ""
    categories: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    size: int = 0
    creationTime: int = 0
    lastUpdateTime: int = 0

    @staticmethod
    def scan_post_data(path):
        mata_data_str = PostData.__get_metadata_str(path)
        data = PostData.__parse_metadata(mata_data_str, path)
        return data

    @staticmethod
    def __get_metadata_str(path):  # 提取属性字段
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
    def __parse_metadata(metadata_str, path):
        post_data = PostData(path=path)

        title_pattern = r'^title:\s*(.*)$'
        date_pattern = r'^date:\s*(.*)$'
        categories_pattern = r'^categories:\s*\n(^\s*- .*$)+'
        category_pattern = r'^\s*- (.*)$'
        tags_pattern = r'^tags:\s*\n(^\s*- .*$)+'
        tag_pattern = r'^\s*- (.*)$'

        for line in metadata_str.split('\n'):
            title_match = re.match(title_pattern, line, re.M)
            if title_match:
                post_data.title = title_match.group(1).strip()

            date_match = re.match(date_pattern, line, re.M)
            if date_match:
                date_str = date_match.group(1).strip()
                # 解析日期时间字符串
                try:
                    post_data.creationTime = int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp())
                except ValueError:
                    post_data.creationTime = 0

            categories_match = re.search(categories_pattern, metadata_str, re.M)
            if categories_match:
                categories = re.findall(category_pattern, categories_match.group(0), re.M)
                post_data.categories = [category.strip() for category in categories]

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
