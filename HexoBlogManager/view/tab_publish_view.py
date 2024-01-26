from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QPushButton, QTextEdit)

class TabPublishView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__initTabUI()

    def __initTabUI(self):
        layout = QVBoxLayout()

        # 复选框
        self.cleanup_checkbox = QCheckBox("Need Clean Up")
        self.update_news_checkbox = QCheckBox("Updated News")
        self.update_weather_checkbox = QCheckBox("Updated Weather")

        layout.addWidget(self.cleanup_checkbox)
        layout.addWidget(self.update_news_checkbox)
        layout.addWidget(self.update_weather_checkbox)

        # 按钮和文本输入框的网格布局
        hBox_layout = QHBoxLayout()
        self.publish_local_button = QPushButton("Publish To Local")
        self.publish_remote_button = QPushButton("Publish To Remote")
        hBox_layout.addWidget(self.publish_local_button)
        hBox_layout.addWidget(self.publish_remote_button)
        layout.addLayout(hBox_layout)

        # 文本显示区域
        self.publish_output = QTextEdit()
        self.publish_output.setReadOnly(True)
        self.publish_output.setPlaceholderText("Publish Process Output:")
        layout.addWidget(self.publish_output)

        # 底部的按钮
        hBox_layout = QHBoxLayout()
        self.open_local_button = QPushButton("Open Local Blog")
        self.open_remote_button = QPushButton("Open Remote Blog")
        hBox_layout.addWidget(self.open_local_button)
        hBox_layout.addWidget(self.open_remote_button)
        layout.addLayout(hBox_layout)

        self.setLayout(layout)
