import subprocess
import threading


class HexoCmdHelper:
    root: str           # hexo框架根目录
    process = None      # 用于保存当前正在运行的进程
    timeout_limit = 30  # 静态属性：默认超时限制（秒）

    @staticmethod
    def init(root: str, timeout_limit: int):
        HexoCmdHelper.root = root
        HexoCmdHelper.timeout_limit = timeout_limit

    @staticmethod
    def __run_cmd(command, callback=None):
        def target():
            try:
                HexoCmdHelper.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                         cwd=HexoCmdHelper.root)
                std_output, std_err = HexoCmdHelper.process.communicate(timeout=HexoCmdHelper.timeout_limit)
                # 将输出解码为字符串
                std_output = std_output.decode()
                std_err = std_err.decode()
            except subprocess.TimeoutExpired:
                HexoCmdHelper.terminate_process()  # 超时时终止进程
                std_output = ""
                std_err = "Time Out!"

            if callback:
                callback(std_output, std_err)

        thread = threading.Thread(target=target)
        thread.start()

    @staticmethod
    def terminate_process():
        if HexoCmdHelper.process:
            HexoCmdHelper.process.terminate()

    @staticmethod
    def new(title, callback=None):
        return HexoCmdHelper.__run_cmd(f'hexo new "{title}"', callback)

    @staticmethod
    def server(port=4000, callback=None):
        return HexoCmdHelper.__run_cmd(f'hexo server -p {port}', callback)

    @staticmethod
    def generate(callback=None):
        return HexoCmdHelper.__run_cmd('hexo generate', callback)

    @staticmethod
    def deploy(callback=None):
        return HexoCmdHelper.__run_cmd('hexo deploy', callback)

    @staticmethod
    def clean(callback=None):
        return HexoCmdHelper.__run_cmd('hexo clean', callback)
