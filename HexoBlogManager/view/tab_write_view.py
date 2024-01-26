from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QComboBox, QDateTimeEdit)
from PyQt5.QtCore import (QDateTime, Qt, pyqtSignal)

class TabWriteView(QWidget):
    refashConfigSignal = pyqtSignal()
    createNewPostSignal = pyqtSignal()

    templateList = []
    categorizationList = []

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__initTabUI()

    def __initTabUI(self):
        self.layout = QVBoxLayout()
        
        # 刷新配置按钮
        refresh_config_btn = QPushButton('Refresh Config')
        refresh_config_btn.clicked.connect(self.refashConfigSignal)
        self.layout.addWidget(refresh_config_btn)

        # 表单布局
        form_layout = QFormLayout()

        # 文章名称输入
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)

        # 文章模板下拉选择
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.templateList)  # 示例模板
        form_layout.addRow("Template:", self.template_combo)

        # 文章分类下拉选择
        self.categorization_combo = QComboBox()
        self.categorization_combo.setEditable(True)
        self.categorization_combo.addItems(["Technology", "Life", "Misc"])  # 示例分类
        form_layout.addRow("Categorization:", self.categorization_combo)

        # 文章标签输入
        self.tags_input = QLineEdit()
        form_layout.addRow("Tags:", self.tags_input)

        # 创建时间选择器
        self.creation_time_edit = QDateTimeEdit()
        self.creation_time_edit.setCalendarPopup(True)
        self.creation_time_edit.setDateTime(QDateTime.currentDateTime())  # 设置当前时间
        form_layout.addRow("Creation Time:", self.creation_time_edit)

        self.layout.addLayout(form_layout)

        # 创建新文章按钮
        create_post_btn = QPushButton('Create New Post')
        create_post_btn.clicked.connect(self.createNewPostSignal)
        self.layout.addWidget(create_post_btn)

        self.setLayout(self.layout)
