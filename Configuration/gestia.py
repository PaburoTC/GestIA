import sys
import time

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

        self.assignFist.clicked.connect(self.updateFist)
        self.assignDaddyF.clicked.connect(self.updateDaddyF)
        self.assignPalmO.clicked.connect(self.updatePalmO)
        self.assignPalmC.clicked.connect(self.updatePalmC)
        self.assignThumbsU.clicked.connect(self.updateThumbsU)
        self.assignThumbsD.clicked.connect(self.updateThumbsD)
        self.buttonPressed = False

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

    def updateFist(self):
        action = self.__update_actions('fist')
        self.actionFist.setText(action)

    def updateDaddyF(self):
        self.actionDaddyF.setText("PRESS ANY KEY")
        self.actionDaddyF.setText(self.__update_actions('daddy_finger'))

    def updatePalmC(self):
        self.actionPalmC.setText("PRESS ANY KEY")
        self.actionPalmC.setText(self.__update_actions('palm_close'))

    def updatePalmO(self):
        self.actionPalmO.setText("PRESS ANY KEY")
        self.actionPalmO.setText(self.__update_actions('palm_open'))

    def updateThumbsU(self):
        self.actionThumbsU.setText("PRESS ANY KEY")
        self.actionThumbsU.setText(self.__update_actions('thumbs_up'))

    def updateThumbsD(self):
        self.actionThumbsD.setText("PRESS ANY KEY")
        self.actionThumbsD.setText(self.__update_actions('thumbs_down'))

    def __update_actions(self, gesture):
        if self.buttonPressed:
            return self.actions[gesture].upper()
        self.buttonPressed = True
        action = keyboard.read_key()
        if len(action) == 0:
            return self.actions[gesture].upper()

        self.actions[gesture] = action
        self.__save_actions()
        self.buttonPressed = False
        return action.upper()

    def __load_actions(self):
        with open('data/actions.json', 'r') as f:
            self.actions = json.load(f)

    def __save_actions(self):
        with open('data/actions.json', 'w') as f:
            json.dump(self.actions, f)

    def __set_labels(self):
        self.actionThumbsD.setText(self.actions['thumbs_down'].upper())
        self.actionThumbsU.setText(self.actions['thumbs_up'].upper())
        self.actionFist.setText(self.actions['fist'].upper())
        self.actionPalmO.setText(self.actions['palm_open'].upper())
        self.actionPalmC.setText(self.actions['palm_close'].upper())
        self.actionDaddyF.setText(self.actions['daddy_finger'].upper())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
