import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import importlib.util

from menusahabatsehat import Ui_MainWindow as mainMenuUI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = mainMenuUI()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.sahabatSehat)

    def sahabatSehat(self):
        try:
            file_path = 'sahabatSehat(memasangkan).py'

            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
