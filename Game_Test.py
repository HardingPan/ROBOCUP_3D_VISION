# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Game_Test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_game_MainWindow(object):
    def setupUi(self, game_MainWindow):
        game_MainWindow.setObjectName("game_MainWindow")
        game_MainWindow.resize(1000, 572)
        self.centralwidget = QtWidgets.QWidget(game_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 9, 981, 511))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 641, 481))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.common_video_label = QtWidgets.QLabel(self.frame_2)
        self.common_video_label.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.common_video_label.setText("")
        self.common_video_label.setObjectName("common_video_label")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(690, 440, 241, 61))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.Start_Button = QtWidgets.QPushButton(self.frame_4)
        self.Start_Button.setGeometry(QtCore.QRect(50, 0, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Start_Button.setFont(font)
        self.Start_Button.setObjectName("Start_Button")
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setGeometry(QtCore.QRect(660, 10, 311, 361))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.Msg_message = QtWidgets.QTextEdit(self.frame_5)
        self.Msg_message.setGeometry(QtCore.QRect(0, 0, 311, 361))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Msg_message.setFont(font)
        self.Msg_message.setReadOnly(True)
        self.Msg_message.setObjectName("Msg_message")
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setGeometry(QtCore.QRect(660, 380, 311, 51))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.Msg_state = QtWidgets.QTextEdit(self.frame_6)
        self.Msg_state.setGeometry(QtCore.QRect(0, 0, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.Msg_state.setFont(font)
        self.Msg_state.setReadOnly(True)
        self.Msg_state.setObjectName("Msg_state")
        game_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(game_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 20))
        self.menubar.setObjectName("menubar")
        game_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(game_MainWindow)
        self.statusbar.setObjectName("statusbar")
        game_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(game_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(game_MainWindow)

    def retranslateUi(self, game_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        game_MainWindow.setWindowTitle(_translate("game_MainWindow", "game_MainWindow"))
        self.Start_Button.setText(_translate("game_MainWindow", "开始"))
        self.Msg_message.setHtml(_translate("game_MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Msg_state.setHtml(_translate("game_MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:22pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

