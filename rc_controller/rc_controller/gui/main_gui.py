# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(517, 327)
        MainWindow.setToolTip("")
        MainWindow.setAccessibleName("")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 40, 191, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_left = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_left.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_left.sizePolicy().hasHeightForWidth())
        self.btn_left.setSizePolicy(sizePolicy)
        self.btn_left.setBaseSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_left.setFont(font)
        self.btn_left.setObjectName("btn_left")
        self.gridLayout.addWidget(self.btn_left, 1, 0, 1, 1)
        self.btn_forward = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_forward.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_forward.sizePolicy().hasHeightForWidth())
        self.btn_forward.setSizePolicy(sizePolicy)
        self.btn_forward.setBaseSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_forward.setFont(font)
        self.btn_forward.setCheckable(False)
        self.btn_forward.setAutoDefault(False)
        self.btn_forward.setDefault(False)
        self.btn_forward.setFlat(False)
        self.btn_forward.setObjectName("btn_forward")
        self.gridLayout.addWidget(self.btn_forward, 0, 1, 1, 1)
        self.btn_backward = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_backward.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_backward.sizePolicy().hasHeightForWidth())
        self.btn_backward.setSizePolicy(sizePolicy)
        self.btn_backward.setBaseSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_backward.setFont(font)
        self.btn_backward.setObjectName("btn_backward")
        self.gridLayout.addWidget(self.btn_backward, 2, 1, 1, 1)
        self.btn_right = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_right.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_right.sizePolicy().hasHeightForWidth())
        self.btn_right.setSizePolicy(sizePolicy)
        self.btn_right.setBaseSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.btn_right.setFont(font)
        self.btn_right.setObjectName("btn_right")
        self.gridLayout.addWidget(self.btn_right, 1, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 240, 251, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 260, 251, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 517, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IP Car Controller"))
        self.btn_left.setText(_translate("MainWindow", "←"))
        self.btn_forward.setText(_translate("MainWindow", "↑"))
        self.btn_backward.setText(_translate("MainWindow", "↓"))
        self.btn_right.setText(_translate("MainWindow", "→"))
        self.label.setText(_translate("MainWindow", "- Use arrow keys or w, a, s, d for movement."))
        self.label_2.setText(_translate("MainWindow", "- Hold SHIFT for go faster."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

