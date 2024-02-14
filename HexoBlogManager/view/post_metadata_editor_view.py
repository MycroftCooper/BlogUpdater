from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime
from util.format_helper import FormatHelper


class PostMetadataEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Post Metadata")

        layout = QVBoxLayout(self)

        # 创建标签和文本框
        self.pathLabel = QLabel("Path:")
        self.pathLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.titleEdit = QLineEdit(self)
        self.categoriesEdit = QLineEdit(self)
        self.tagsEdit = QLineEdit(self)
        self.creationTimeEdit = QDateTimeEdit(self)
        self.creationTimeEdit.setCalendarPopup(True)
        self.creationTimeEdit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.pathLabel)
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
        path = data["path"]
        self.pathLabel.setText(f"Path: \n{path}")
        if "title" in data:
            self.titleEdit.setText(data["title"])
        if "categories" in data:
            self.categoriesEdit.setText(FormatHelper.list_data_2_str_data(data["categories"], ";"))
        if "tags" in data:
            self.tagsEdit.setText(FormatHelper.list_data_2_str_data(data["tags"], ";"))
        if "creationTime" in data:
            self.creationTimeEdit.setDateTime(FormatHelper.int_timestamp_2_qt_time(data["creationTime"]))

    def get_data(self):
        categories = FormatHelper.str_data_2_list_data(self.categoriesEdit.text(), ";")
        tags = FormatHelper.str_data_2_list_data(self.tagsEdit.text(), ";")
        int_timestamp = FormatHelper.qt_time_2_int_timestamp(self.creationTimeEdit.dateTime())

        return {
            "title": self.titleEdit.text(),
            "categories": categories,
            "tags": tags,
            "creationTime": int_timestamp
        }
