from view import *
from model import *

class HexoBlogManagerCtrl():
    def __init__(self, view:HexoBlogManagerView, model:HexoBlogManagerModel):
        self.view = view
        self.model = model
        self.bindViewSignal()
        
    def bindViewSignal(self):
        self.view.optionsTab.saveOptionsSignal.connect(self.saveOptions)
    
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
    def saveOptions(self):
        print("save!")

    def loadOptions(self):
        pass
#endregion