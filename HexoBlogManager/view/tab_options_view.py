from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QCheckBox)
from .path_widget import PathWidget

class TabOptionsView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.__initTabUI()

    def __initTabUI(self):
        layout = QVBoxLayout()

        self.__isEditing = False
        self.edit_btn = QPushButton('Edit Options')
        self.edit_btn.clicked.connect(self.onEditBtnClick)
        layout.addWidget(self.edit_btn)

        # 使用网格布局
        grid_layout = QGridLayout()
        self.path_widgets = {}

        paths = ['Blog Root Path', 'Posts Path', 'Templates Path', 'News Page Path', 'Weather Page Path']
        for path_label in paths:
            path_widget = PathWidget(grid_layout, path_label, False)
            self.path_widgets[path_label] = path_widget

        layout.addLayout(grid_layout)

        self.auto_publish_checkbox = QCheckBox('Auto Publish at boot')
        self.auto_publish_checkbox.setEnabled(False)
        layout.addWidget(self.auto_publish_checkbox)

        self.setLayout(layout)

    def onEditBtnClick(self):
        self.__isEditing = not self.__isEditing

        if self.__isEditing:
            self.edit_btn.setText('Save Options')
        else:
            self.edit_btn.setText('Edit Options')

        for path_widget in self.path_widgets.values():
            path_widget.setCanEdit(self.__isEditing)
        
        self.auto_publish_checkbox.setEnabled(self.__isEditing)