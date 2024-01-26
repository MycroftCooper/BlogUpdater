from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QWidget

class PathWidget(QWidget):
    def __init__(self, layout:QGridLayout, labelStr:str, canEdite:bool):
        super().__init__()
        self.labelStr = labelStr
        self.__label = QLabel(labelStr+":")
        self.__input = QLineEdit()
        self.__button = QPushButton('...')
        self.__button.clicked.connect(lambda _, : self.__openFileDialog())
        row = layout.rowCount()
        layout.addWidget(self.__label, row, 0)
        layout.addWidget(self.__input, row, 1)
        layout.addWidget(self.__button, row, 2)
        self.setCanEdit(canEdite)

    def setCanEdit(self, canEdite:bool):
        self.__input.setReadOnly(not canEdite)
        self.__button.setEnabled(canEdite)

    def __openFileDialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.__input.setText(directory)

    def getPath(self):
        return self.__input.text()