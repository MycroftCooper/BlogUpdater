from PyQt5.QtWidgets import (QMainWindow, QTabWidget)

from .tab_write_view import TabWriteView
from .tab_options_view import TabOptionsView
from .tab_publish_view import TabPublishView
from .tab_navigate_view import TabNavigateView


class HexoBlogManagerView(QMainWindow):
    TAB_HEIGHT = 40  # 类属性，定义标签的高度
    writeTab = None
    publishTab = None
    optionsTab = None

    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):
        # 初始化用户界面
        self.setWindowTitle('Hexo Blog Manager')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumWidth(600)
        self.__init_tab_bar()
        self.adjustSize()

    # region 标题栏相关
    def __init_tab_bar(self):
        # 初始化标签栏
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # 设置标签栏的样式
        style_sheet = (
            f"QTabBar::tab {{ height: {self.TAB_HEIGHT}px; }}"
            "QTabWidget::pane { border: 0; }"
            "QTabWidget { background: transparent; }"
            "QTabBar { background: transparent; }"
        )
        self.tabs.setStyleSheet(style_sheet)

        self.writeTab = TabWriteView(self)
        self.tabs.addTab(self.writeTab, 'Write')
        self.navigateTab = TabNavigateView(self)
        self.tabs.addTab(self.navigateTab, 'Navigation')
        self.publishTab = TabPublishView(self)
        self.tabs.addTab(self.publishTab, 'Publish')
        self.optionsTab = TabOptionsView(self)
        self.tabs.addTab(self.optionsTab, 'Options')

        # 重写resizeEvent来处理窗口大小改变
        self.tabs.resizeEvent = self.__resize_tabs
        self.tabs.currentChanged.connect(self.__handle_tab_change)

    def __resize_tabs(self, event):
        # 调整标签页的大小以适应窗口宽度
        super(HexoBlogManagerView, self).resizeEvent(event)
        tab_count = self.tabs.count()
        tab_width = self.tabs.width() // tab_count
        self.tabs.setStyleSheet(
            f"QTabBar::tab {{ width: {tab_width}px; height: {self.TAB_HEIGHT}px; }}"
        )

    def __handle_tab_change(self, _):
        self.adjustSize()  # 调整主窗口的大小以适应内容
# endregion
