from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QCheckBox, QSpinBox, QLabel, QMessageBox)
from PyQt5.QtCore import (pyqtSignal)
from .path_widget import (PathWidget, PathType)
from .error_dialog import ErrorDialog


class TabOptionsView(QWidget):
    reloadOptionsDataSignal = pyqtSignal()
    saveOptionsDataSignal = pyqtSignal()
    openHexoConfigSignal = pyqtSignal()

    data_dict = {}
    view_data_dict = {}

    def init_tab_ui(self):
        layout = QVBoxLayout()
        self.__is_editing = False

        self.reload_btn = QPushButton('Reload Options')
        self.reload_btn.clicked.connect(self.reloadOptionsDataSignal)
        layout.addWidget(self.reload_btn)

        self.edit_btn = QPushButton('Edit Options')
        self.edit_btn.clicked.connect(self.__on_edit_btn_click)
        layout.addWidget(self.edit_btn)

        self.path_widgets = {}

        # 使用网格布局
        self.grid_layout = QGridLayout()

        for key, value in self.data_dict.items():
            row = self.grid_layout.rowCount()
            widget = None

            if isinstance(value, str):
                path_label = key
                if path_label.__contains__("Url"):
                    widget = PathWidget(self.grid_layout, path_label, PathType.Url)
                elif path_label.__contains__("Page Path"):
                    widget = PathWidget(self.grid_layout, path_label, PathType.File)
                else:
                    widget = PathWidget(self.grid_layout, path_label, PathType.Dir)
                widget.path = value
                widget.setEnabled(False)
                self.path_widgets[key] = widget

            elif isinstance(value, bool):
                widget = QCheckBox(key)
                widget.setEnabled(False)
                widget.setChecked(value)
                self.grid_layout.addWidget(widget, row, 0)

            elif isinstance(value, int):
                label = QLabel(key)
                self.grid_layout.addWidget(label, row, 0)
                widget = QSpinBox(self)
                widget.setMinimum(100)  # 设置最小值
                widget.setMaximum(20000)  # 设置最大值
                widget.setValue(value)  # 设置初始值
                widget.setSingleStep(100)
                widget.setEnabled(False)
                self.grid_layout.addWidget(widget, row, 1)

            self.view_data_dict[key] = widget

        layout.addLayout(self.grid_layout)

        self.open_config_file_btn = QPushButton('Open Hexo Config File')
        self.open_config_file_btn.clicked.connect(self.openHexoConfigSignal)
        layout.addWidget(self.open_config_file_btn)

        self.setLayout(layout)

    def update_options(self):
        for key, value in self.data_dict.items():
            widget = self.view_data_dict[key]
            if isinstance(widget, PathWidget):
                widget.path = value

            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)

            elif isinstance(widget, QSpinBox):
                widget.setValue(value)

    def __on_edit_btn_click(self):
        if not self.__is_editing:
            self.edit_btn.setText('Save Options')
            self.__is_editing = True
        else:
            if not self.__check_submission():
                return
            self.edit_btn.setText('Edit Options')
            self.__view_2_data()
            self.saveOptionsDataSignal.emit()
            self.__is_editing = False

        for widget in self.view_data_dict.values():
            widget.setEnabled(self.__is_editing)

    def __check_submission(self):
        for path_widget in self.path_widgets.values():
            if not path_widget.path:
                ErrorDialog.warning_signal.emit("Options Save Warning", f"{path_widget.labelStr} cant be null!")
                return False

            if not path_widget.is_path_exists:
                ErrorDialog.warning_signal.emit("Options Save Warning", f"{path_widget.labelStr} : {path_widget.path} not exists!")
                return False
        return True

    def __view_2_data(self):
        for k, v in self.view_data_dict.items():
            value = None
            if isinstance(v, PathWidget):
                value = v.path
            elif isinstance(v, QCheckBox):
                value = v.isChecked()
            elif isinstance(v, QSpinBox):
                value = v.value()
            self.data_dict[k] = value
