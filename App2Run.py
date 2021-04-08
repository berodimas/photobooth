from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import necessary module
import sys
import cv2
import datetime
import os
import imutils
import numpy as np

from App2 import *

class MainWindow(QWidget):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.color = True
        self.setWindowTitle('PyQt5 - Photo Booth App')
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cap = cv2.VideoCapture(1)
        # start timer
        timer = QTimer(self)
        timer.setInterval(int(1000/30))
        timer.timeout.connect(self.viewCam)
        timer.start()
        # save path
        self.outputPath = "output"
        # set button callback clicked  function
        self.ui.button_snapshot.clicked.connect(self.showPopup)
        self.ui.button_color.clicked.connect(self.colorSet)
        self.ui.button_menu.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page1))
        self.ui.button_gallery.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page2))
        self.ui.button_credits.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page3))

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, self.image = self.cap.read()
        self.image = imutils.resize(self.image, height=1024)
        # set image for snapshot
        self.imageSnap = self.image
        # convert image to RGB format
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
        qImg = QImage(self.image.data, width, height,
                      step, QImage.Format_RGB888)
        # show image in label_image
        if self.color == False:
            self.ui.label_camera.setPixmap(QPixmap.fromImage(
                qImg.convertToFormat(QtGui.QImage.Format_Grayscale8)))
        else:
            self.ui.label_camera.setPixmap(QPixmap.fromImage(
                qImg.convertToFormat(QtGui.QImage.Format_RGB888)))

    # set color boolean
    def colorSet(self):
        if self.color == True:
            self.color = False
        else:
            self.color = True

    # pop-up function
    def showPopup(self):
        self.takeSnapeshot()
        msg = QMessageBox()
        msg.setWindowTitle("PyQt5 - Photo Booth App")
        msg.setText("Image have been taken!")
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText("Image saved at Output folder.")
        msg.exec_()

    # snapshot function
    def takeSnapeshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))
        if self.color == False:
            self.imageSnap = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            self.imageSnap = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(p, self.imageSnap)
        self.ui.label_image.setPixmap(QtGui.QPixmap(p))

# start and show main window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
