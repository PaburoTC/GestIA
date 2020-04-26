import sys
import cv2
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from config import *
from detector import *
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        # Set up environment
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Connect application logic
        self.startButton.clicked.connect(self.startRecording)
        self.stopButton.clicked.connect(self.stopRecording)
        self.assignFist.clicked.connect(self.update_actions)

        # Configure timer for screen recording
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_frame)

        # Get webcam object 
        self.webcam = cv2.VideoCapture(0)
        ret, self.frame = self.webcam.read()
        # GUI enable/disable logic
        self.stopButton.setEnabled(False)

        # Inference Model Object
        self.inferenceObject = InferenceModel()
        self.inferenceObject.initialize()

        self.actions = None
        self.__load_actions()
        self.__set_labels()

    def stopRecording(self):
        self.startButton.setEnabled(True)
        self.timer.stop()
        self.stopButton.setEnabled(False)

    def startRecording(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.timer.start(1)

    def show_frame(self):
        # Capture frame from webcam
        ret, self.frame = self.webcam.read()
        if not ret:
            return

        # Interference process
        label_detected = self.inferenceObject.processFrame(self.frame)
        self.label.setText("Detection: " + label_detected)

        # Process image to show on QtGui
        image = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                             self.frame.shape[1] * self.frame.shape[2],
                             QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        # Show image as a pixelmap on labelCam
        self.labelCam.setPixmap(pixmap)

    def update_actions(self):
        action = keyboard.read_key()
        if len(action) == 0:
            return
        gesture = self.inferenceObject.processFrame(self.frame)
        print(gesture)
        if gesture != 'nothing':
            self.actions[gesture] = action
            self.__save_actions()

    def __load_actions(self):
        with open('data/actions.json', 'r') as f:
            self.actions = json.load(f)

    def __save_actions(self):
        with open('data/actions.json', 'w') as f:
            json.dump(self.actions, f)

    def __set_labels(self):
        self.actionThumbsD.setText(self.actions['thumbs_down'])
        self.actionThumbsU.setText(self.actions['thumbs_up'])
        self.actionFist.setText(self.actions['fist'])
        self.actionPalmO.setText(self.actions['palm_open'])
        self.actionPalmC.setText(self.actions['palm_close'])
        self.actionDaddyF.setText(self.actions['daddy_finger'])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
