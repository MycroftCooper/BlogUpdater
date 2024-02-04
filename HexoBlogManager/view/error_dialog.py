from PyQt5.QtWidgets import QMessageBox, QWidget


class ErrorDialog:
    @staticmethod
    def log_error(message, text: str, title: str = "ERROR"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(str(message))
        msg.setWindowTitle(title)
        msg.exec_()

    @staticmethod
    def log_warning(parent_widget: QWidget, title: str, message: str):
        QMessageBox.warning(parent_widget, title, message)
