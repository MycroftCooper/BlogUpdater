import os
from enum import Enum
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QWidget

class PathType(Enum):
    File = 1
    Dir = 2
    Url = 3

class PathWidget(QWidget):
    @property
    def path(self) -> str:
        return self.__input.text()
    @path.setter
    def path(self, value):
        self.__input.setText(value)

    @property
    def isPathExists(self) -> bool:
        return self.pathType == PathType.Url or os.path.exists(self.path)

    def __init__(self, layout:QGridLayout, labelStr:str, pathType:PathType):
        super().__init__()
        self.labelStr = labelStr
        self.pathType = pathType
        row = layout.rowCount()

        self.__label = QLabel(labelStr+":")
        layout.addWidget(self.__label, row, 0)
        self.__input = QLineEdit()
        layout.addWidget(self.__input, row, 1)
        if pathType != PathType.Url:
            self.__button = QPushButton('...')
            self.__button.clicked.connect(lambda _, : self.__openFileDialog())
            layout.addWidget(self.__button, row, 2)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.__input.setReadOnly(not enabled)
        if self.pathType != PathType.Url:
            self.__button.setEnabled(enabled)

    def __openFileDialog(self):
        targetPath = ""
        if self.pathType == PathType.Dir:
            targetPath = QFileDialog.getExistingDirectory(self, "Select Directory")
        elif self.pathType == PathType.File:
            targetPath, _  = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        self.__input.setText(targetPath)