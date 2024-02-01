import os
import math
from datetime import datetime
from PyQt5.QtWidgets import QGridLayout ,QFrame, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from .navigate_view_enum import InfoShowRule

class PostInfoWidget(QWidget):
    def __init__(self, parent: QWidget, post_data):
        super().__init__(parent)

        self.post_data = post_data

        # 创建布局
        layout = QVBoxLayout()

        # 创建并添加标签
        self.name_str = QLabel(self.post_data.name)
        self.categories_label = QLabel("Categories: ")
        self.categories_str = QLabel(', '.join(self.post_data.categories))
        self.tags_label = QLabel("Tags: ")
        self.tags_str = QLabel(', '.join(self.post_data.tags))
        self.size_label = QLabel("Size: ")
        self.size_str = QLabel(self.__convertBytes(self.post_data.size))
        self.creation_time_label = QLabel("Creation Time: ")
        self.creation_time_str = QLabel(self.__formatTimestamp(self.post_data.creation_time))
        self.last_update_time_label = QLabel("Last Update Time: ")
        self.last_update_time_str = QLabel(self.__formatTimestamp(self.post_data.lastUpdateTime))

        info_layout = QGridLayout()
        info_layout.addWidget(self.name_str, 0, 0)
        info_layout.addWidget(self.categories_label, 1, 0)
        info_layout.addWidget(self.categories_str, 1, 1)
        info_layout.addWidget(self.tags_label, 2, 0)
        info_layout.addWidget(self.tags_str, 2, 1)
        info_layout.addWidget(self.size_label, 3, 0)
        info_layout.addWidget(self.size_str, 3, 1)
        info_layout.addWidget(self.creation_time_label, 4, 0)
        info_layout.addWidget(self.creation_time_str, 4, 1)
        info_layout.addWidget(self.last_update_time_label, 5, 0)
        info_layout.addWidget(self.last_update_time_str, 5, 1)
        layout.addLayout(info_layout)

        # 创建按钮
        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.__onOpenBtnClick)
        self.edit_button = QPushButton("Edit Metadata")
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.edit_button)
        layout.addLayout(button_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

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
                
    def __convertBytes(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"