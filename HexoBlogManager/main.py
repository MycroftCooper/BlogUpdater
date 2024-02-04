import sys
from PyQt5.QtWidgets import QApplication
from view import HexoBlogManagerView
from model import HexoBlogManagerModel
from hexo_blog_manager_ctrl import HexoBlogManagerCtrl

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = HexoBlogManagerView()
    model = HexoBlogManagerModel()
    ctrl = HexoBlogManagerCtrl(view, model)
    view.show()
    sys.exit(app.exec_())
