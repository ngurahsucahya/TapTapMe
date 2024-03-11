from PyQt5 import QtCore, QtGui, QtWidgets
import importlib.util

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1282, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.judul = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.judul.sizePolicy().hasHeightForWidth())
        self.judul.setSizePolicy(sizePolicy)
        self.judul.setMaximumSize(QtCore.QSize(600, 100))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.judul.setFont(font)
        self.judul.setAlignment(QtCore.Qt.AlignCenter)
        self.judul.setObjectName("judul")
        self.verticalLayout.addWidget(self.judul, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sahabatBerhitung = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sahabatBerhitung.sizePolicy().hasHeightForWidth())
        self.sahabatBerhitung.setSizePolicy(sizePolicy)
        self.sahabatBerhitung.setMaximumSize(QtCore.QSize(500, 250))
        self.sahabatBerhitung.setObjectName("sahabatBerhitung")
        self.sahabatBerhitung.clicked.connect(self.run_my_program)
        self.horizontalLayout_2.addWidget(self.sahabatBerhitung)
        self.sahabatSehat = QtWidgets.QPushButton(self.centralwidget)
        self.sahabatSehat.setMaximumSize(QtCore.QSize(500, 250))
        self.sahabatSehat.setObjectName("sahabatSehat")
        self.horizontalLayout_2.addWidget(self.sahabatSehat)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1282, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.judul.setText(_translate("MainWindow", "Tap Tap Me"))
        self.sahabatBerhitung.setText(_translate("MainWindow", "Sahabat Berhitung"))
        self.sahabatSehat.setText(_translate("MainWindow", "Sahabat Sehat"))

    def run_my_program(self):
        # Path to the Python file you want to run
        file_path = 'memindahkanObjectGAS.py'

        # Load the module
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call a function from the loaded module if necessary
        # module.your_function()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
