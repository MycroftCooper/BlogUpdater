import re
import os
import shutil
import subprocess
from .model_data import PostData
from util.error_dialog import ErrorDialog
from util.format_helper import FormatHelper


class PostHelper:
    post_root: str
    img_root: str

    @staticmethod
    def load_all_post_path():
        folder_path = PostHelper.post_root
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
    def set_root(post_root: str, img_root: str):
        PostHelper.post_root = post_root
        PostHelper.img_root = img_root

    @staticmethod
    def get_post_path(title: str):
        return os.path.join(PostHelper.post_root, f"{title}.md")

    @staticmethod
    def get_post_img_root_path(title: str):
        return os.path.join(PostHelper.img_root, title)

    @staticmethod
    def get_post_img_url(post_title: str, img_name: str):
        post_root_parent = os.path.dirname(PostHelper.post_root)
        img_sub_folder = PostHelper.get_post_img_root_path(post_title)
        img_target_path = os.path.join(img_sub_folder, img_name)
        new_url = os.path.relpath(img_target_path, post_root_parent)
        new_url = new_url.replace(os.sep, '/')  # 将路径分隔符替换为 '/'
        return '/' + new_url

    @staticmethod
    def get_post_title(path: str):
        filename_with_extension = os.path.basename(path)
        filename_without_extension = os.path.splitext(filename_with_extension)[0]
        return filename_without_extension

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

        # 检查并重命名图片文件夹
        old_title = PostHelper.get_post_title(old_path)
        old_img_folder = PostHelper.get_post_img_root_path(old_title)
        new_img_folder = PostHelper.get_post_img_root_path(new_name)
        if os.path.exists(old_img_folder) and old_img_folder != new_img_folder:
            os.rename(old_img_folder, new_img_folder)

        try:
            with open(new_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 正则表达式查找 Markdown 文件中的图片引用
            pattern = r'!\[.*?\]\((.*?)\)'
            matches = re.findall(pattern, content)

            for url in matches:
                img_filename = os.path.basename(url)
                new_url = PostHelper.get_post_img_url(new_name, img_filename)
                content = content.replace(url, new_url)

            # 保存修改后的文件
            with open(new_path, 'w', encoding='utf-8') as file:
                file.write(content)

        except Exception as e:
            ErrorDialog().error_signal.emit(f"Error occurred while updating image URLs: {e}", "model>rename_post")

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

        # 删除文章的图片目录
        post_title = PostHelper.get_post_title(target_str)
        img_folder_path = PostHelper.get_post_img_root_path(post_title)
        if os.path.exists(img_folder_path):
            shutil.rmtree(img_folder_path)  # 删除目录及其所有内容
        return True

    @staticmethod
    def set_post_meta_data(post_data: PostData):
        new_metadata_str = "---\n"
        new_metadata_str += "title: " + post_data.title + "\n"
        new_metadata_str += ("date: " + FormatHelper.int_timestamp_2_str(post_data.creationTime) + "\n")
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
    def import_post(path: str):
        if not os.path.exists(path):
            return False, f"File <{path}> does not exist."
        if not path.endswith('.md'):
            return False, f"File <{path}>  is not a markdown file."

        # 构造目标文件路径
        filename = os.path.basename(path)
        target_path = os.path.join(PostHelper.post_root, filename)

        # 检查是否已存在同名文件
        if os.path.exists(target_path):
            return False, f"A file with the same name already exists in the destination<{target_path}>."

        # 复制文件
        try:
            shutil.copy(path, target_path)
            is_success, output = PostHelper.__import_post_img_assets(path, target_path)
            if is_success:
                return True, f"{output}\nFile <{path}> imported successfully."
            else:
                return False, output
        except Exception as e:
            return False, f"Error occurred while copying file <{path}>: {e}"

    # region 更改图片URL相关
    @staticmethod
    def __import_post_img_assets(import_post_path: str, target_post_path: str):
        # 确保路径存在且文件为.md
        if not all(os.path.exists(p) and p.endswith('.md') for p in [import_post_path, target_post_path]):
            return False, "Invalid path or file type."

        try:
            with open(target_post_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 使用正则表达式查找 Markdown 文件中的图片引用
            pattern = r'!\[.*?\]\((.*?)\)'
            matches = re.findall(pattern, content)

            post_title = os.path.splitext(os.path.basename(target_post_path))[0]  # 提取 Markdown 文件名（无后缀）
            img_sub_folder = PostHelper.get_post_img_root_path(post_title)  # 图片存储子文件夹
            os.makedirs(img_sub_folder, exist_ok=True)

            for url in matches:
                original_url_str = url
                if url.startswith('http://') or url.startswith('https://'):
                    continue  # 网址，跳过

                # 处理相对路径和绝对路径
                if not os.path.isabs(url):
                    url = os.path.join(os.path.dirname(import_post_path), url)

                PostHelper.__copy_img_to_post_img_root(post_title, url)

                # 构建新的相对路径并替换 URL
                img_filename = os.path.basename(url)
                new_url = PostHelper.get_post_img_url(post_title, img_filename)
                content = content.replace(original_url_str, new_url)

            # 保存修改后的文件
            with open(target_post_path, 'w', encoding='utf-8') as file:
                file.write(content)

            return True, "Assets imported and updated successfully."

        except Exception as e:
            return False, f"Error occurred: {e}"

    @staticmethod
    def __copy_img_to_post_img_root(post_title: str, source_img_path: str):
        if source_img_path.startswith('http://') or source_img_path.startswith('https://'):
            return  # 网址，后面加上下载逻辑吧

        # 复制图片资源
        img_filename = os.path.basename(source_img_path)
        img_sub_folder = PostHelper.get_post_img_root_path(post_title)
        img_target_path = os.path.join(img_sub_folder, img_filename)
        shutil.copy(source_img_path, img_target_path)
    # endregion

    # region 提取属性相关
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
                post_data.creationTime = FormatHelper.time_str_2_int_timestamp(date_str)

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
    # endregion

    @staticmethod
    def clean_empty_img_root():
        for root, dirs, files in os.walk(PostHelper.img_root, topdown=False):
            for d in dirs:
                dir_path = os.path.join(root, d)
                if not os.listdir(dir_path):  # 检查目录是否为空
                    os.rmdir(dir_path)  # 删除空目录
