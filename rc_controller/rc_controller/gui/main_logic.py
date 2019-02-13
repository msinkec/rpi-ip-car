from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from .main_gui import Ui_MainWindow

def run(sock):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

