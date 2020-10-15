import sys
import cv2
from PyQt5.QtWidgets import (
    QWidget,
    QToolTip,
    QPushButton,
    QApplication,
    QLabel,
    QDesktopWidget,
    QMainWindow,
    QAction,
    qApp,
    QMenu,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
import numpy as np


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def image(self):
        self.ret, self.frame = self.cap.read()


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        camera = Camera()
        while True:
            camera.image()
            if camera.ret:
                rgbImage = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(
                    rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888
                )
                p = convertToQtFormat.scaled(240, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class CameraPreview(QLabel):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.move(0, 0)


class QRPreview(QLabel):
    def __init__(
        self,
    ):
        super().__init__()
        self.camera = camera
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.move(100, 0)