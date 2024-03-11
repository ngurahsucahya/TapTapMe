import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap  # Mengimpor QPixmap dari modul QtGui
from PyQt5 import QtGui
from taptapme import Ui_MainWindow  # Mengimpor kelas Ui_MainWindow dari file UI yang sudah dibuat
from PyQt5 import QtCore, QtGui, QtWidgets
import importlib.util

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sahabatBerhitung.clicked.connect(self.run_my_program)

    def run_my_program(self):
        # Path to the Python file you want to run
        file_path = 'sahabatBerhitung.py'

        # Load the module
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())