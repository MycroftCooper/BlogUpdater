from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QCheckBox, QSizePolicy)
from .post_info_widget import PostInfoWidget
from .navigate_view_enum import (GroupBy, SortBy, InfoShowRule)

class TabNavigateView(QWidget):
    postInfoViewDict: dict = None
    isReverse: bool = False
    infoShowRule: InfoShowRule = None
    infoSortBy: SortBy = None
    infoGroupBy: GroupBy = None
    searchStr: str = None

    navigateUpdateViewSignal = pyqtSignal()
    navigateUpdatePostDataSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 整体布局
        layout = QVBoxLayout()

        self.updateData_btn = QPushButton('Update Post Info Data')
        self.updateData_btn.clicked.connect(self.navigateUpdatePostDataSignal)
        layout.addWidget(self.updateData_btn)

        # 排序和分组布局
        sort_group_layout = QHBoxLayout()
        
        # Sort By组合框
        sort_by_label = QLabel("Sort By:")
        sort_by_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        for option in SortBy:
            self.sort_by_combo.addItem(option.name, option.value)
        self.sort_by_combo.currentIndexChanged.connect(self.onNeedUpdateView)
        sort_group_layout.addWidget(sort_by_label)
        sort_group_layout.addWidget(self.sort_by_combo)

        # Group By组合框
        group_by_label = QLabel("Group By:")
        group_by_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.group_by_combo = QComboBox()
        self.group_by_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        for option in GroupBy:
            self.group_by_combo.addItem(option.name, option.value)
        self.group_by_combo.currentIndexChanged.connect(self.onNeedUpdateView)
        sort_group_layout.addWidget(group_by_label)
        sort_group_layout.addWidget(self.group_by_combo)

        layout.addLayout(sort_group_layout)

        # 搜索布局
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        search_layout.addWidget(search_label)

        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        search_layout.addWidget(self.search_input)

        # 搜索按钮
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.onNeedUpdateView)
        search_layout.addWidget(self.search_button)

        # 取消搜索按钮
        self.clear_search_button = QPushButton("X")
        self.clear_search_button.clicked.connect(self.onNeedUpdateView)
        self.clear_search_button.setFixedSize(20, 20)  # 设置按钮的大小
        search_layout.addWidget(self.clear_search_button)

        layout.addLayout(search_layout)

        checkbox_layout = QHBoxLayout()
        self.reverse_checkbox = QCheckBox("Is Reverse")
        self.reverse_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.reverse_checkbox)
        self.show_categories_checkbox = QCheckBox("Show Categories")
        self.show_categories_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.show_categories_checkbox)
        self.show_tags_checkbox = QCheckBox("Show Tags")
        self.show_tags_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.show_tags_checkbox)
        self.show_size_checkbox = QCheckBox("Show Size")
        self.show_size_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.show_size_checkbox)
        self.show_creation_checkbox = QCheckBox("Show Creation Time")
        self.show_creation_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.show_creation_checkbox)
        self.show_last_update_time_checkbox = QCheckBox("Show Last Update Time")
        self.show_last_update_time_checkbox.stateChanged.connect(self.onInfoShowRuleChanaged)
        checkbox_layout.addWidget(self.show_last_update_time_checkbox)
        layout.addLayout(checkbox_layout)

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def onInfoShowRuleChanaged(self):
        self.isReverse = self.reverse_checkbox.isChecked()
        # 更新 InfoShowRule
        self.infoShowRule = InfoShowRule.NONE
        if self.show_categories_checkbox.isChecked():
            self.infoShowRule |= InfoShowRule.Categories
        if self.show_tags_checkbox.isChecked():
            self.infoShowRule |= InfoShowRule.Tags
        if self.show_size_checkbox.isChecked():
            self.infoShowRule |= InfoShowRule.Size
        if self.show_creation_checkbox.isChecked():
            self.infoShowRule |= InfoShowRule.CreationTime
        if self.show_last_update_time_checkbox.isChecked():
            self.infoShowRule |= InfoShowRule.LastUpdateTime

    def onNeedUpdateView(self):
        # 更新 SortBy
        self.infoSortBy = SortBy(self.sort_by_combo.currentData())
        # 更新 GroupBy
        self.infoGroupBy = GroupBy(self.group_by_combo.currentData())
        # 更新 Search String
        self.searchStr = self.search_input.text()
        self.navigateUpdateViewSignal.emit()

    def updateInfoTree(self):
        self.list_widget.clear()

        for group, posts in self.postInfoViewDict.items():
            # 添加组标签作为一个列表项
            group_item = QListWidgetItem(group, self.list_widget)
            group_item.setFlags(group_item.flags() | Qt.ItemIsUserCheckable)
            group_item.setCheckState(Qt.Unchecked)  # 可以设置为可折叠

            for post in posts:
                # 为每个帖子创建一个自定义的部件
                post_widget = PostInfoWidget(self ,post)
                post_item = QListWidgetItem(self.list_widget)
                self.list_widget.setItemWidget(post_item, post_widget)
                post_item.setSizeHint(post_widget.sizeHint())
