from PyQt5.QtWidgets import QApplication, QMainWindow
from text import *
import cv2 as cv

img = cv.imread('img/p1.jpg')


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openimage)

    def openimage(self):
        self.label.setPixmap(QPixmap("C:\\Users\\Planet\\Desktop\\幼儿园.jpg"))
        self.label.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyClass()
    myWin.show()
    sys.exit(app.exec_())