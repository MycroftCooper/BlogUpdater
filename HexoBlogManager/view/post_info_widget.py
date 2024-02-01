import os
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from .navigate_view_enum import InfoShowRule

class PostInfoWidget(QWidget):
    def __init__(self, parent: QWidget, post_data):
        super().__init__(parent)

        self.post_data = post_data

        # 创建布局
        layout = QVBoxLayout()

        # 创建并添加标签
        self.name_label = QLabel(f"Name: {self.post_data.name}")
        self.categories_label = QLabel(f"Categories: {', '.join(self.post_data.categories)}")
        self.tags_label = QLabel(f"Tags: {', '.join(self.post_data.tags)}")
        self.size_label = QLabel(f"Size: {self.post_data.size} bytes")
        self.creation_time_label = QLabel(f"Creation Time: {self.__formatTimestamp(self.post_data.creation_time)}")
        self.last_update_time_label = QLabel(f"Last Update Time: {self.__formatTimestamp(self.post_data.lastUpdateTime)}")

        layout.addWidget(self.name_label)
        layout.addWidget(self.categories_label)
        layout.addWidget(self.tags_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.creation_time_label)
        layout.addWidget(self.last_update_time_label)

        # 创建按钮
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.__onOpenBtnClick)
        self.edit_button = QPushButton("Edit Metadata")
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.edit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def setInfoVisible(self, rule:InfoShowRule):
        # 根据规则设置每个信息的可见性
        self.categories_label.setVisible(bool(rule & InfoShowRule.Categories))
        self.tags_label.setVisible(bool(rule & InfoShowRule.Tags))
        self.size_label.setVisible(bool(rule & InfoShowRule.Size))
        self.creation_time_label.setVisible(bool(rule & InfoShowRule.CreationTime))
        self.last_update_time_label.setVisible(bool(rule & InfoShowRule.LastUpdateTime))

    def __formatTimestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def __onEditMetadataBtnClick(self):
        pass

    def __onOpenBtnClick(self):
        if os.path.exists(self.post_data.path):
            if os.name == 'nt':  # Windows
                os.startfile(self.post_data.path)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', self.post_data.path])