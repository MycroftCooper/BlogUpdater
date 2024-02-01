from PyQt5.QtWidgets import QFrame, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import QSize
from .post_info_widget import PostInfoWidget

class PostGroupWidget(QWidget):
    def __init__(self, parent: QListWidget, group_name, posts):
        super().__init__(parent)

        self.is_reverse = False
        self.is_collapsed = False

        layout = QVBoxLayout(self)

        # 创建标题栏
        self.header_widget = QWidget()
        header_layout = QHBoxLayout(self.header_widget)
        self.toggle_button = QPushButton("[-]")
        self.toggle_button.setFixedSize(30, 30)
        self.toggle_button.clicked.connect(self.__toggleContent)
        header_layout.addWidget(self.toggle_button)
        header_layout.addWidget(QLabel(group_name))
        header_layout.addWidget(QLabel(f"Posts Num:{len(posts)}"))
        self.header_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        layout.addWidget(self.header_widget)

        # 创建内容区域
        self.content_area = QWidget()
        content_layout = QVBoxLayout(self.content_area)
        
        for post in posts:
            content_layout.addWidget(PostInfoWidget(self, post))
        layout.addWidget(self.content_area)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        self.list_item = QListWidgetItem(parent)
        parent.setItemWidget(self.list_item, self)
        self.setLayout(layout)
        self.updateSize()
        
    def __toggleContent(self):
        self.is_collapsed = not self.is_collapsed
        self.content_area.setVisible(not self.content_area.isVisible())
        self.toggle_button.setText("[+]" if self.is_collapsed else "[-]")
        self.updateSize()

    def reverseOrder(self, isReverse):
        if isReverse == self.is_reverse:
            return
        self.is_reverse = isReverse
        
        content_layout = self.content_area.layout()
        # 从布局中移除所有部件，同时保留它们的引用
        widgets = []
        for i in range(content_layout.count()):
            item = content_layout.itemAt(i)
            widget = item.widget()
            if widget:
                content_layout.removeWidget(widget)
                widgets.append(widget)

        # 倒序添加部件
        for widget in reversed(widgets):
            content_layout.addWidget(widget)

    def sizeHint(self):
        header_size_hint = self.header_widget.sizeHint()
        margins = self.layout().contentsMargins()
        total_height = header_size_hint.height() + margins.top() + margins.bottom()
        header_size_hint = QSize(header_size_hint.width() + margins.left() + margins.right(), total_height)

        if self.is_collapsed:
            return header_size_hint

        total_height = self.header_widget.sizeHint().height()
        content_layout = self.content_area.layout()
        margins = content_layout.contentsMargins()
        spacing = content_layout.spacing()
        for i in range(content_layout.count()):
            item = content_layout.itemAt(i)
            if item.widget():
                total_height += item.widget().sizeHint().height()
                # 增加间隔，但最后一个widget不需要增加
                if i < content_layout.count() - 1:
                    total_height += spacing
        # 增加上下边距
        total_height += margins.top() + margins.bottom()
        return QSize(header_size_hint.width(), header_size_hint.height() + total_height)


    def updateSize(self):
        self.list_item.setSizeHint(self.sizeHint())
        self.parent().update()  # 刷新QListWidget