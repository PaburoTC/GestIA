import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from config_ui import *
from detector import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        # Set up environment
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
        # Connect application logic
        self.startButton.clicked.connect(self.startRecording)
        self.stopButton.clicked.connect(self.stopRecording)

        # Configure timer for screen recording
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_frame)

        # Get webcam object 
        self.webcam = cv2.VideoCapture(0)
        
        # GUI enable/disable logic
        self.stopButton.setEnabled(False)
        
        # Inference Model Object
        self.inferenceObject = InferenceModel()
        self.inferenceObject.initialize()

    def stopRecording(self):
        self.startButton.setEnabled(True)
        self.timer.stop()
        self.stopButton.setEnabled(False)

    def startRecording(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.timer.start(1);

    def show_frame(self):
        # Capture frame from webcam
        ret, frame = self.webcam.read()
        if not ret:
            return

        # Interference process
        label_detected = self.inferenceObject.processFrame(frame)
        self.label.setText("Detection: " + label_detected)

        # Process image to show on QtGui
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        # Show image as a pixelmap on labelCam
        self.labelCam.setPixmap(pixmap)
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
