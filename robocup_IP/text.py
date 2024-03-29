# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1217, 943)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 180, 341, 441))
        self.label.setStyleSheet("background-color: rgb(185, 185, 185);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(530, 180, 241, 31))
        self.label_2.setStyleSheet("background-color: rgb(211, 242, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 220, 261, 311))
        self.label_3.setStyleSheet("\n"
"background-color: rgb(198, 198, 198);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 567, 93, 51))
        self.pushButton.setStyleSheet("color: rgb(0, 170, 255);\n"
"background-color: rgb(202, 202, 202);")
        self.pushButton.setObjectName("pushButton")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(650, 570, 121, 41))
        self.commandLinkButton.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.commandLinkButton.setObjectName("commandLinkButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1217, 26))
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
        self.label.setText(_translate("MainWindow", "图片显示"))
        self.label_2.setText(_translate("MainWindow", "识别结果输出区"))
        self.label_3.setText(_translate("MainWindow", "识别程序输出状态"))
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.commandLinkButton.setText(_translate("MainWindow", "下一步"))

from text import Ui_MainWindow
from PyQt5 import QtCore ,QtGui, uic ,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        super(MyApp,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_vis)
    def show_vis(self):
        self.label.setPixmap(QPixmap("C:\\a.jpg"))
        self.label.setScaledContents(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())