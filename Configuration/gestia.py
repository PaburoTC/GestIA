import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from config_ui import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.startButton.clicked.connect(self.startRecording)
        self.stopButton.clicked.connect(self.stopRecording)
        # Configure timer for screen recording
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_frame)
        self.stopButton.setEnabled(False);
        # Get webcam object 
        self.webcam = cv2.VideoCapture(0)
        
    def stopRecording(self):
        self.startButton.setEnabled(True);
        self.timer.stop()
        self.stopButton.setEnabled(False);


    def startRecording(self):
        self.startButton.setEnabled(False);
        self.stopButton.setEnabled(True);
        
        self.timer.start(1);

    def show_frame(self):
        
        ret, frame = self.webcam.read()
        if not ret:
            return
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.labelCam.setPixmap(pixmap)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
