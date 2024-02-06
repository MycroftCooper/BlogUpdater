from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDateTimeEdit
from PyQt5.QtCore import QDateTime


class PostMetadataEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Post Metadata")

        layout = QVBoxLayout(self)

        # 创建标签和文本框
        self.titleEdit = QLineEdit(self)
        self.categoriesEdit = QLineEdit(self)
        self.tagsEdit = QLineEdit(self)
        self.creationTimeEdit = QDateTimeEdit(self)
        self.creationTimeEdit.setCalendarPopup(True)
        self.creationTimeEdit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.titleEdit)
        layout.addWidget(QLabel("Categories:"))
        layout.addWidget(self.categoriesEdit)
        layout.addWidget(QLabel("Tags:"))
        layout.addWidget(self.tagsEdit)
        layout.addWidget(QLabel("Creation Time:"))
        layout.addWidget(self.creationTimeEdit)

        # 创建按钮
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")

        # 连接按钮的信号
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.okButton)
        button_layout.addWidget(self.cancelButton)
        layout.addLayout(button_layout)

    def set_data(self, data):
        if "title" in data:
            self.titleEdit.setText(data["title"])
        if "categories" in data:
            self.categoriesEdit.setText(data["categories"])
        if "tags" in data:
            self.tagsEdit.setText(data["tags"])
        if "creation_time" in data:
            # 假设 creation_time 是以 'YYYY-MM-DD HH:MM:SS' 格式的字符串
            creation_time = QDateTime.fromString(data["creation_time"], "yyyy-MM-dd HH:mm:ss")
            self.creationTimeEdit.setDateTime(creation_time)

    def get_data(self):
        return {
            "title": self.titleEdit.text(),
            "categories": self.categoriesEdit.text(),
            "tags": self.tagsEdit.text(),
            "creation_time": self.creationTimeEdit.dateTime().toString()
        }
