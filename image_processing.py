import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from interface import Ui_MainWindow

class ImageProcessor(QMainWindow):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def main():
    app = QApplication([])
    window = ImageProcessor()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()