from PyQt5.QtWidgets import (QFrame, QLabel, QFileDialog, QWidget, QVBoxLayout, QFormLayout, QPushButton, QLineEdit,
                             QComboBox, QDateTimeEdit)
from PyQt5.QtCore import (QDateTime, Qt, pyqtSignal)
from PyQt5.QtGui import QDragEnterEvent, QDropEvent


class TabWriteView(QWidget):
    refreshConfigSignal = pyqtSignal()
    createNewPostSignal = pyqtSignal(dict)
    importNewPostSignal = pyqtSignal(list)

    templateList = []
    categorizationList = []

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__init_tab_ui()

    def __init_tab_ui(self):
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()

        # 刷新配置按钮
        refresh_config_btn = QPushButton('Refresh Config')
        refresh_config_btn.clicked.connect(self.refreshConfigSignal)
        self.layout.addWidget(refresh_config_btn)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)

        create_layout = QVBoxLayout()

        # 表单布局
        form_layout = QFormLayout()

        # 文章名称输入
        self.title_input = QLineEdit()
        form_layout.addRow("Title:", self.title_input)

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
        create_layout.addLayout(form_layout)

        # 创建新文章按钮
        create_post_btn = QPushButton('Create New Post')
        create_post_btn.clicked.connect(self.__on_create_new_post_btn_click)
        create_layout.addWidget(create_post_btn)
        self.layout.addLayout(create_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)

        # 导入文章
        import_layout = QVBoxLayout()

        self.setGeometry(100, 100, 400, 300)
        import_label = QLabel("Drop .md files here to import")
        import_label.setAlignment(Qt.AlignCenter)
        import_layout.addWidget(import_label)
        self.layout.addLayout(import_layout)

        import_post_btn = QPushButton('Import Posts')
        import_post_btn.clicked.connect(self.__on_import_post_btn_click)
        import_layout.addWidget(import_post_btn)

        self.setLayout(self.layout)

    def __on_create_new_post_btn_click(self):
        new_post_info_dict = {
            "title": self.title_input.text()

        }

    def __on_import_post_btn_click(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_filter = "Markdown Files (*.md)"
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Import Posts", "", file_filter, options=options)

        if file_paths:
            print("Selected Files:")
            for file_path in file_paths:
                print(file_path)
            self.importNewPostSignal.emit(file_paths)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        # 获取拖放的所有文件路径
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]

        # 筛选出.md文件路径并进行处理
        md_file_paths = [path for path in file_paths if path.endswith(".md")]

        if md_file_paths:
            for file_path in md_file_paths:
                print(file_path)
            self.importNewPostSignal.emit(file_paths)
