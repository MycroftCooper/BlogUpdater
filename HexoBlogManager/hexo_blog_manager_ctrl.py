import os
import subprocess
import sys

from view import *
from model import *

class HexoBlogManagerCtrl():
    def __init__(self, view:HexoBlogManagerView, model:HexoBlogManagerModel):
        self.view = view
        self.model = model
        self.bindViewSignal()
        self.initOptionsData()
        
    def bindViewSignal(self):
        self.view.optionsTab.reloadOptionsSignal.connect(self.reloadOptionsData)
        self.view.optionsTab.saveOptionsSignal.connect(self.saveOptionsData)
        self.view.optionsTab.openHexoConfigSignal.connect(self.openHexoConfigFile)
    
#region Write Ctrl
    def refreshConfig(self):
        pass

    def createNewPost(self):
        pass
#endregion

#region Publish Ctrl
    def publish(self, isRemote:bool):
        pass

    def openBlog(self, isRemote:bool):
        pass
#endregion

#region Options Ctrl
    def saveOptionsData(self):
        data = self.view.optionsTab.data_dict
        self.model.options_data.data_dict = data
        self.model.saveOptionsData()

    def initOptionsData(self):
        self.model.loadOptionsData()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.initTabUI()

    def reloadOptionsData(self):
        self.model.loadOptionsData()
        self.view.optionsTab.data_dict = self.model.options_data.data_dict
        self.view.optionsTab.updateOptions()

    def openHexoConfigFile(self):
        folder_path = self.model.options_data.data_dict['Blog Root Path']
        file_name = '_config.yml'
        file_path = os.path.join(folder_path, file_name)
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", file_path])
            else:
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            ErrorDialog.logError(e, "Ctrl>openHexoConfigFile")
            print(f"Error opening file: {e}")
#endregion