from PyQt5.QtWidgets import QMessageBox, QWidget

class ErrorDialog:
    @staticmethod
    def logError(message, text:str, title:str = "ERROR"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(str(message))
        msg.setWindowTitle(title)
        msg.exec_()

    @staticmethod
    def logWraning(parentWidget : QWidget, title:str, message: str):
        QMessageBox.warning(parentWidget, title, message)
