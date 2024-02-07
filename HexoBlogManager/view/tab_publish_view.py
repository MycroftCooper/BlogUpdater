from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QPushButton, QTextEdit)
from PyQt5.QtCore import (pyqtSignal)


class TabPublishView(QWidget):
    publishSignal = pyqtSignal(bool, bool)
    openBlogSignal = pyqtSignal(bool)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__init_tab_ui()

    def __init_tab_ui(self):
        layout = QVBoxLayout()

        # 复选框
        self.cleanup_checkbox = QCheckBox("Need Clean Up")
        layout.addWidget(self.cleanup_checkbox)

        # 按钮和文本输入框的网格布局
        h_box_layout = QHBoxLayout()
        self.publish_local_btn = QPushButton("Publish To Local")
        self.publish_local_btn.clicked.connect(lambda: self.publishSignal.emit(False, self.cleanup_checkbox.isChecked()))
        self.publish_remote_btn = QPushButton("Publish To Remote")
        self.publish_remote_btn.clicked.connect(lambda: self.publishSignal.emit(True, self.cleanup_checkbox.isChecked()))
        h_box_layout.addWidget(self.publish_local_btn)
        h_box_layout.addWidget(self.publish_remote_btn)
        layout.addLayout(h_box_layout)

        # 文本显示区域
        self.publish_output = QTextEdit()
        self.publish_output.setReadOnly(True)
        self.publish_output.setPlaceholderText("Publish Process Output:")
        layout.addWidget(self.publish_output)

        # 底部的按钮
        h_box_layout = QHBoxLayout()
        self.open_local_btn = QPushButton("Open Local Blog")
        self.open_local_btn.clicked.connect(lambda: self.openBlogSignal.emit(False))
        self.open_remote_btn = QPushButton("Open Remote Blog")
        self.open_remote_btn.clicked.connect(lambda: self.openBlogSignal.emit(True))
        h_box_layout.addWidget(self.open_local_btn)
        h_box_layout.addWidget(self.open_remote_btn)
        layout.addLayout(h_box_layout)

        self.setLayout(layout)
