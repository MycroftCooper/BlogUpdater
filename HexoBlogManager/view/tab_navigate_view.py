from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QCheckBox, QSizePolicy)

class TabNavigateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 整体布局
        layout = QVBoxLayout()

        # 排序和分组布局
        sort_group_layout = QHBoxLayout()
        
        # Sort By组合框
        sort_by_label = QLabel("Sort By:")
        sort_by_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sort_group_layout.addWidget(sort_by_label)
        sort_group_layout.addWidget(self.sort_by_combo)

        # Group By组合框
        group_by_label = QLabel("Group By:")
        group_by_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.group_by_combo = QComboBox()
        self.group_by_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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
        search_layout.addWidget(self.search_button)

        # 取消搜索按钮
        self.clear_search_button = QPushButton("X")
        self.clear_search_button.setFixedSize(20, 20)  # 设置按钮的大小
        search_layout.addWidget(self.clear_search_button)

        layout.addLayout(search_layout)

        # 反向排序复选框
        self.reverse_checkbox = QCheckBox("Is Reverse")
        layout.addWidget(self.reverse_checkbox)

        # 树形视图
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Articles")
        self.populate_tree()  # 用示例数据填充树
        layout.addWidget(self.tree_widget)

        self.setLayout(layout)

    def populate_tree(self):
        # 示例数据填充方法
        root = QTreeWidgetItem(self.tree_widget, ["TreeItem 1"])
        child1 = QTreeWidgetItem(root, ["TreeItem 1.2"])
        child2 = QTreeWidgetItem(child1, ["TreeItem 1.2.1"])
        child3 = QTreeWidgetItem(child1, ["TreeItem 1.2.2"])
        root.addChild(child1)
        child1.addChild(child2)
        child1.addChild(child3)
        self.tree_widget.expandAll()
