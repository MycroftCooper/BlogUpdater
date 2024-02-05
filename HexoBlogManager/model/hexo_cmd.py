import os
import subprocess


class HexoCmd:
    root: str

    @staticmethod
    def set_root(root_path: str):
        HexoCmd.root = root_path

    @staticmethod
    def run_cmd(command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=HexoCmd.root)
        std_output, std_err = process.communicate()
        return std_output, std_err

    @staticmethod
    def new(title):
        return HexoCmd.run_cmd(f'hexo new "{title}"')

    @staticmethod
    def server(port=4000):
        return HexoCmd.run_cmd(f'hexo server -p {port}')

    @staticmethod
    def generate():
        return HexoCmd.run_cmd('hexo generate')

    @staticmethod
    def deploy():
        return HexoCmd.run_cmd('hexo deploy')

    @staticmethod
    def open(title):
        path = os.path.join(HexoCmd.root, "source", f"_posts", f"{title}.md")
        if not os.path.exists(path):
            return False
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', path])
        return True
