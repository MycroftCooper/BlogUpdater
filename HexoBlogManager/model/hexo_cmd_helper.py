import subprocess
import threading


class HexoCmdHelper:
    root: str  # hexo框架根目录
    process = None  # 用于保存当前正在运行的进程
    timeout_limit = 30  # 静态属性：默认超时限制（秒）

    @staticmethod
    def init(root: str, timeout_limit: int):
        HexoCmdHelper.root = root
        HexoCmdHelper.timeout_limit = timeout_limit

    @staticmethod
    def __run_cmd(command, callback=None):

        def target():
            is_success = False
            output_str = ""
            try:
                HexoCmdHelper.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                         stderr=subprocess.PIPE,
                                                         cwd=HexoCmdHelper.root)
                std_output, std_err = HexoCmdHelper.process.communicate(timeout=HexoCmdHelper.timeout_limit)
                # 将输出解码为字符串
                std_output = std_output.decode()
                std_err = std_err.decode()
                # 检查返回码
                return_code = HexoCmdHelper.process.returncode
                if return_code == 0:
                    is_success = True
                    output_str = std_output
                else:
                    is_success = False
                    output_str = std_err
                output_str = f"IsSuccess:[{is_success}]\n" + output_str
            except subprocess.TimeoutExpired:
                HexoCmdHelper.terminate_process()  # 超时时终止进程
                is_success = False
                output_str = "Time Out!"
            finally:
                if callback:
                    callback(is_success, output_str)

        thread = threading.Thread(target=target)
        thread.start()

    @staticmethod
    def terminate_process():
        if HexoCmdHelper.process:
            HexoCmdHelper.process.terminate()

    @staticmethod
    def new(title, callback=None):
        HexoCmdHelper.__run_cmd(f'hexo new "{title}"', callback)

    @staticmethod
    def server(port=4000):
        command = f"start cmd /k hexo server -p {port}"
        subprocess.Popen(command, shell=True, cwd=HexoCmdHelper.root)

    @staticmethod
    def generate(callback=None):
        HexoCmdHelper.__run_cmd('hexo generate', callback)

    @staticmethod
    def deploy(callback=None):
        HexoCmdHelper.__run_cmd('hexo deploy', callback)

    @staticmethod
    def clean(callback=None):
        HexoCmdHelper.__run_cmd('hexo clean', callback)
