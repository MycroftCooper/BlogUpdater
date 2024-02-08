from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import pyqtSignal, QObject


class ErrorDialog(QObject):
    error_signal = pyqtSignal(str, str)
    warning_signal = pyqtSignal(str, str)

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ErrorDialog, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.error_signal.connect(self.log_error)
        self.warning_signal.connect(self.log_warning)
        self.__initialized = True

    def log_error(self, message, text: str):
        print(f"Error: message:\t{message}\ntext:\t{text}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(str(message))
        msg.setWindowTitle("ERROR")
        msg.exec_()

    def log_warning(self, title: str, message: str):
        print(f"Warning: title:\t{title}\nmessage:\t{message}")
        QMessageBox.warning(None, title, message)
