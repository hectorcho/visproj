import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import pyqtgraph as pg
import numpy as np
import math
import video_eye_tracking
import eeg_widget
# pyqtgraph.examples.run()
# comment



try:
    _fromUtf8 = str
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.time = 0
        self.eeg = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setGeometry(0, 0, 1920, 1100)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.video_widget = video_eye_tracking.eyeTrackingWidget(self.centralWidget)
        self.video_widget.setGeometry(QtCore.QRect(5, 5, 1192, 750))
        self.video_widget.setObjectName(_fromUtf8("eyeTrackingWidget"))

        #self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.centralWidget)
        #self.slider.setGeometry(QtCore.QRect(20,500,500,60))

        self.eegWidget = eeg_widget.eegWidget(self.centralWidget)
        self.eegWidget.setGeometry(QtCore.QRect(5, 750, 1192, 300))
        self.eegWidget.setObjectName(_fromUtf8("graphicsView"))

        self.video_widget.positionSlider.rangeChanged.connect(self.syncEggRange)
        self.video_widget.positionSlider.valueChanged.connect(self.SyncScroll)
        self.eegWidget.positionSlider.sliderMoved.connect(self.updateScroll)

        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def syncEggRange(self):
        self.eegWidget.positionSlider.setRange(0, self.video_widget.positionSlider.maximum())

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

    def SyncScroll(self,position):
        self.eegWidget.positionSlider.setValue(position)

    def updateScroll(self,position):
        self.video_widget.player.pause()
        self.video_widget.positionSlider.setValue(position)
        self.video_widget.player.setPosition(position)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.resize(1920, 1100)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.drawCurve(eeg)
    # ui.cal_content()
    # t = QtCore.QTimer()
    # t.timeout.connect(ui.updateData)
    # t.start(100)
    sys.exit(app.exec_())
