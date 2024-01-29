from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QCheckBox, QSpinBox, QLabel)
from .path_widget import PathWidget
from PyQt5.QtCore import (pyqtSignal)

class TabOptionsView(QWidget):
    saveOptionsSignal = pyqtSignal()
    __widgets = []
    
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

        paths = ['Blog Root Path','Blog Remote Url','Blog Local Url', 'Posts Path', 'Assets Path', 'Templates Path', 'News Page Path', 'Weather Page Path']
        for path_label in paths:
            path_widget = PathWidget(grid_layout, path_label, False)
            self.path_widgets[path_label] = path_widget
            
        row = grid_layout.rowCount()
        
        timeout_limit_label = QLabel("Publish Timeout Limit:")
        grid_layout.addWidget(timeout_limit_label, row, 0)
        self.publish_timeout_limit_spin_box = QSpinBox(self)
        self.publish_timeout_limit_spin_box.setMinimum(100)  # 设置最小值
        self.publish_timeout_limit_spin_box.setMaximum(2000)  # 设置最大值
        self.publish_timeout_limit_spin_box.setValue(200)  # 设置初始值
        self.publish_timeout_limit_spin_box.setSingleStep(100)
        self.publish_timeout_limit_spin_box.setEnabled(False)
        grid_layout.addWidget(self.publish_timeout_limit_spin_box, row, 1)
        self.__widgets.append(self.publish_timeout_limit_spin_box)
        
        row += 1
        
        self.auto_publish_checkbox = QCheckBox('Auto Publish at boot')
        self.auto_publish_checkbox.setEnabled(False)
        grid_layout.addWidget(self.auto_publish_checkbox, row, 0)
        self.__widgets.append(self.auto_publish_checkbox)
        
        self.need_clan_up_checkbox = QCheckBox('Need Clan Up On Publish')
        self.need_clan_up_checkbox.setEnabled(False)
        grid_layout.addWidget(self.need_clan_up_checkbox, row, 1)
        self.__widgets.append(self.need_clan_up_checkbox)
        
        row += 1
        
        self.update_news_checkbox = QCheckBox('Update News On Publish')
        self.update_news_checkbox.setEnabled(False)
        grid_layout.addWidget(self.update_news_checkbox, row, 0)
        self.__widgets.append(self.update_news_checkbox)
        
        self.update_weather_checkbox = QCheckBox('Update Weather On Publish')
        self.update_weather_checkbox.setEnabled(False)
        grid_layout.addWidget(self.update_weather_checkbox, row, 1)
        self.__widgets.append(self.update_weather_checkbox)
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def onEditBtnClick(self):
        self.__isEditing = not self.__isEditing

        for path_widget in self.path_widgets.values():
            path_widget.setEnabled(self.__isEditing)
        for w in self.__widgets:
            w.setEnabled(self.__isEditing)
            
        if self.__isEditing:
            self.edit_btn.setText('Save Options')
        else:
            self.edit_btn.setText('Edit Options')
            self.saveOptionsSignal.emit()