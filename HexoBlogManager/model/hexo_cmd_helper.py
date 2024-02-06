import os
import subprocess


class HexoCmdHelper:
    root: str

    @staticmethod
    def set_root(root_path: str):
        HexoCmdHelper.root = root_path

    @staticmethod
    def run_cmd(command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd=HexoCmdHelper.root)
        std_output, std_err = process.communicate()
        return std_output, std_err

    @staticmethod
    def new(title):
        return HexoCmdHelper.run_cmd(f'hexo new "{title}"')

    @staticmethod
    def server(port=4000):
        return HexoCmdHelper.run_cmd(f'hexo server -p {port}')

    @staticmethod
    def generate():
        return HexoCmdHelper.run_cmd('hexo generate')

    @staticmethod
    def deploy():
        return HexoCmdHelper.run_cmd('hexo deploy')
