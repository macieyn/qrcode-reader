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
    QFrame,
    QSplitter,
)
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt

from gui.camera_preview import CameraPreview, QRPreview, Camera


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 340, 310)
        self.setWindowTitle("QR")
        self.setWindowIcon(QIcon("qr_icon.png"))
        self.center()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        hbox = QHBoxLayout(self)

        camera = Camera()

        cameraPreview = CameraPreview(camera)
        qrPreview = QRPreview(camera)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(cameraPreview)
        splitter1.addWidget(qrPreview)

        hbox.addWidget(splitter1)
        centralWidget.setLayout(hbox)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()