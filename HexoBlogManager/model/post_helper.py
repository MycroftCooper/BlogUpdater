import re
import os
from datetime import datetime
from .model_data import PostData
from view.error_dialog import ErrorDialog


class PostHelper:
    root: str

    @staticmethod
    def load_all_post_path():
        folder_path = PostHelper.root
        if not os.path.exists(folder_path):
            ErrorDialog().error_signal.emit(f"Folder path '{folder_path}' does not exist.", "model>loadAllPostPath")
            return []
        md_file_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".md"):
                    md_file_path = os.path.join(root, file)
                    md_file_paths.append(md_file_path)
        return md_file_paths

    @staticmethod
    def set_posts_root(path: str):
        PostHelper.root = path

    @staticmethod
    def get_post_path(title: str):
        return os.path.join(PostHelper.root, f"{title}.md")

    @staticmethod
    def is_post_exists_in_folder(target_str, is_title: bool = False):
        if is_title:
            target_str = PostHelper.get_post_path(target_str)
        return os.path.exists(target_str)

    @staticmethod
    def open_post(target_str, is_title: bool = False):
        if is_title:
            target_str = PostHelper.get_post_path(target_str)
        if not os.path.exists(target_str):
            return False
        if os.name == 'nt':  # Windows
            os.startfile(target_str)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', target_str])
        return True

    @staticmethod
    def rename_post(old_path: str, new_name: str, data: PostData):
        if not PostHelper.is_post_exists_in_folder(old_path):
            ErrorDialog().error_signal.emit(f"cant rename，because post<{old_path}> is not exist!", "model>rename_post")
            return False
        new_path = PostHelper.get_post_path(new_name)
        if new_path != old_path and PostHelper.is_post_exists_in_folder(new_path):
            ErrorDialog().error_signal.emit(f"cant rename，because post<{old_path}> is already exist!", "model>rename_post")
            return False
        data.title = new_name
        data.path = new_path
        if new_path != old_path:
            os.rename(old_path, new_path)
        PostHelper.set_post_meta_data(data)
        return True

    @staticmethod
    def scan_post_data(target_str, is_title: bool = False):
        if is_title:
            target_str = PostHelper.get_post_path(target_str)
        mata_data_str = PostHelper.__get_metadata_str(target_str)
        data = PostHelper.__parse_metadata(mata_data_str, target_str)
        return data

    @staticmethod
    def del_post(target_str, is_title: bool = False):
        if is_title:
            target_str = PostHelper.get_post_path(target_str)
        if not PostHelper.is_post_exists_in_folder(target_str):
            return False
        os.remove(target_str)
        return True

    @staticmethod
    def set_post_meta_data(post_data: PostData):
        new_metadata_str = "---\n"
        new_metadata_str += "title: " + post_data.title + "\n"
        new_metadata_str += ("date: " + datetime.fromtimestamp(post_data.creationTime).
                             strftime("%Y-%m-%d %H:%M:%S") + "\n")
        new_metadata_str += "tags:\n" + '\n'.join(['    - ' + tag for tag in post_data.tags]) + "\n"
        new_metadata_str += "categories:\n" + '\n'.join(
            ['    - ' + category for category in post_data.categories]) + "\n"
        new_metadata_str += "typora-root-url: ..\n"
        new_metadata_str += "---\n"

        with open(post_data.path, 'r', encoding='utf-8') as file:
            content = file.read()

        end_of_old_metadata = content.find('\n---', 1)  # 从第二个字符开始查找第二个 '---'
        if end_of_old_metadata != -1:
            content = content[end_of_old_metadata + 4:]  # 跳过第二个 '---' 及其后的换行符

        with open(post_data.path, 'w', encoding='utf-8') as file:
            file.write(new_metadata_str + content)

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
        category_pattern = r'^\s*- (.*)$'
        tag_pattern = r'^\s*- (.*)$'

        in_tags_section = False
        in_categories_section = False

        for line in metadata_str.split('\n'):
            # Title
            title_match = re.match(title_pattern, line)
            if title_match:
                post_data.title = title_match.group(1).strip()

            # Date
            date_match = re.match(date_pattern, line)
            if date_match:
                date_str = date_match.group(1).strip()
                try:
                    post_data.creationTime = int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp())
                except ValueError:
                    post_data.creationTime = 0

            # Detect sections
            if line.strip() == 'tags:':
                in_tags_section = True
                in_categories_section = False
                post_data.tags = list()
                continue
            elif line.strip() == 'categories:':
                in_categories_section = True
                in_tags_section = False
                post_data.categories = list()
                continue

            if in_tags_section:
                tag_match = re.match(tag_pattern, line)
                if tag_match:
                    post_data.tags.append(tag_match.group(1).strip())

            if in_categories_section:
                category_match = re.match(category_pattern, line)
                if category_match:
                    post_data.categories.append(category_match.group(1).strip())

        # Get file last update time and size
        post_data.lastUpdateTime = int(os.path.getmtime(path))
        try:
            post_data.size = os.path.getsize(path)
        except OSError:
            post_data.size = -1

        return post_data
