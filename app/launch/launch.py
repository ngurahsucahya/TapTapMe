import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap  # Mengimpor QPixmap dari modul QtGui
from PyQt5 import QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
import importlib.util

from taptapme2 import Ui_MainWindow as mainMenuUI # Mengimpor kelas Ui_MainWindow dari file UI yang sudah dibuat
from menusahabatsehat import Ui_MainWindow as sahabatSehatMenu

# class SahabatSehatWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = sahabatSehatMenu()
#         self.ui.setupUi(self)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = mainMenuUI()
        self.ui.setupUi(self)
        self.ui.SahabatBerhitung.clicked.connect(self.sahabatBerhitung)
        self.ui.CekKamera.clicked.connect(self.cekKamera)
        self.ui.SahabatSehat.clicked.connect(self.SahabatSehat)

    def sahabatBerhitung(self):
        try:
            # Path to the Python file you want to run
            file_path = 'sahabatBerhitung.py'

            # Load the module
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print("Error:", e)

    def cekKamera(self):
        try:
            # Path to the Python file you want to run
            file_path = 'deteksiTangan.py'

            # Load the module
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception as e:
            print("Error:", e)

    def SahabatSehat(self):
        self.sahabat_sehat_window = QtWidgets.QMainWindow()
        self.ui_sahabat_sehat = sahabatSehatMenu()
        self.ui_sahabat_sehat.setupUi(self.sahabat_sehat_window)
        self.sahabat_sehat_window.show()

    # ini cuman buat pengetahuan aja
    # def tampilWindowSahabatSehat(self):
    #     self.sahabat_sehat_window = SahabatSehatWindow()
    #     self.sahabat_sehat_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
