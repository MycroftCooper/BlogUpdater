import os
import re

def fix_img_url(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()

                # 正则表达式匹配 Markdown 中的图片引用 URL
                pattern = r'!\[.*?\]\((.*?)\)'

                def replace_func(match):
                    url = match.group(1)
                    if url.startswith('images/'):
                        return f'![](/{url})'
                    return match.group(0)

                # 替换所有以 'images/' 开头的 URL 为 '/images/'
                new_content = re.sub(pattern, replace_func, content)

                # 将更改写回文件
                with open(file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(new_content)

                print(f"Processed {file_path}")

if __name__ == "__main__":
    directory = input("Enter the directory path to scan for .md files: ")
    fix_img_url(directory)
