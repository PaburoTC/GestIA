# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(687, 432)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 40, 391, 311))
        self.frame.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(4)
        self.frame.setObjectName("frame")
        self.labelCam = QtWidgets.QLabel(self.frame)
        self.labelCam.setGeometry(QtCore.QRect(0, 0, 391, 311))
        self.labelCam.setText("")
        self.labelCam.setScaledContents(True)
        self.labelCam.setObjectName("labelCam")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(50, 360, 131, 51))
        self.startButton.setObjectName("startButton")
        self.detectionCapture = QtWidgets.QGraphicsView(self.centralwidget)
        self.detectionCapture.setGeometry(QtCore.QRect(440, 60, 221, 181))
        self.detectionCapture.setObjectName("detectionCapture")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(440, 30, 151, 20))
        self.label.setObjectName("label")
        self.assignButton = QtWidgets.QPushButton(self.centralwidget)
        self.assignButton.setGeometry(QtCore.QRect(470, 260, 71, 31))
        self.assignButton.setObjectName("assignButton")
        self.ketTextbox = QtWidgets.QTextEdit(self.centralwidget)
        self.ketTextbox.setGeometry(QtCore.QRect(550, 260, 81, 31))
        self.ketTextbox.setObjectName("ketTextbox")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(200, 360, 131, 51))
        self.stopButton.setObjectName("stopButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gestia"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "Detection: Nothing"))
        self.assignButton.setText(_translate("MainWindow", "Assign key"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
