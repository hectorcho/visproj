import sys
from PyQt4 import QtCore, QtGui, Qt
import PyQt4
import pyqtgraph as pg
import numpy as np
import pyqtgraph.examples
import math
# pyqtgraph.examples.run()

from vlc_widget import VLCPlayerWidget
from ui_menubar import Ui_Menubar


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.time = 0
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.vlcWidget = QtGui.QWidget(self.centralWidget)
        self.vlcWidget.setGeometry(QtCore.QRect(20, 10, 1280, 720))
        self.vlcWidget.setObjectName(_fromUtf8("vlcWidget"))

        self.l = QtGui.QVBoxLayout()
        self.vlcWidget.setLayout(self.l)

        self.vlcplayer = VLCPlayerWidget()
        self.l.addWidget(self.vlcplayer)

        #self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.centralWidget)
        #self.slider.setGeometry(QtCore.QRect(20,500,500,60))

        self.graphicsView = pg.PlotWidget(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 750, 1280, 270))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))


        self.eegScroll = QtGui.QScrollBar(QtCore.Qt.Horizontal, MainWindow)
        self.eegScroll.setGeometry(QtCore.QRect(20, 1050, 1280, 10))
        self.eegScroll.setMaximum(1000)

        self.vlcslider = self.vlcplayer.positionSlider

        QtCore.QObject.connect(self.vlcslider, QtCore.SIGNAL("actionTriggered(int)"), self.SyncScroll)


        #refer to drawCurve() method below


        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))

        #self.eeg_menu = self.menuBar.addMenu('&File')


        #self.load_file = QtGui.QAction("&Load File", self)
        #self.load_file.triggered.connect(self.openEEG)




        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # utility function for
    def lowestGreaterThan(self, arr, threshold):
        print(arr.shape)
        low = 0
        high = len(arr)
        while low < high:
            mid = int(math.floor((low + high) / 2))
            # print("low = ", low, " mid = ", mid, " high = ", high)
            if arr[mid] == threshold:
                return mid
            elif arr[mid] < threshold and mid != low:
                low = mid
            elif arr[mid] > threshold and mid != high:
                high = mid
            else:
                # terminate with index pointing to the first element greater than low
                high = low = low + 1
        return low

    def GreatestLowerThan(self, arr, threshold):
        print(arr.shape)
        low = 0
        high = len(arr)
        while low < high:
            mid = int(math.floor((low + high) / 2))
            # print("low = ", low, " mid = ", mid, " high = ", high)
            if arr[mid] == threshold:
                return mid
            elif arr[mid] < threshold and mid != low:
                low = mid
            elif arr[mid] > threshold and mid != high:
                high = mid
            else:
                # terminate with index pointing to the first element greater than low
                high = low
        return high

    def drawCurve(self, egg):
        self.egg = egg;
        self.time = 0
        start_time = self.time - 2000
        end_time = self.time + 2000
        max = np.max(eeg[1, :])
        min = np.min(eeg[1, :])
        self.y, self.x = self.cal_content(start_time=start_time, end_time=end_time)
        self.graphicsView.setYRange(min, max)
        self.view_plot = self.graphicsView.plot(self.x, self.y, pen=(0,1))

    def cal_content(self, start_time=-2000, end_time=2000):
        low = self.lowestGreaterThan(self.egg[0, :], start_time)
        high = self.GreatestLowerThan(self.egg[0, :], end_time)
        # limit the index in case out of array bound
        low = min(self.egg.shape[1] - 1,max(0,low))
        high = max(0,min(self.egg.shape[1] - 1, high))
        print(start_time, end_time, self.egg[0, low], self.egg[0, high], low, high)
        return self.egg[1,low:high + 1], self.egg[0,low:high + 1]

    def updateData(self):
        self.time = self.time + 100
        start_time = self.time - 2000
        end_time = self.time + 2000
        yd, xd = self.cal_content(start_time=start_time,end_time=end_time)
        self.graphicsView.setLabel('left', 'EEG Value', units='V')
        self.graphicsView.setLabel('bottom', 'Time', units='ms')
        self.graphicsView.setXRange(start_time, end_time)
        self.view_plot.setData(y=yd, x=xd)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))


    def openEEG(self, filename = None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", user.home)
        if not filename:
            return
        self.eeg = np.loadtxt(filename,delimiter=",")

    def SyncScroll(self):
        sliderValue = self.vlcslider.value()
        self.eegScroll.setValue(sliderValue)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    MainWindow.resize(1920, 1080)
    #eeg = openEEG("AZZ1_v2_Carol_30sec.txt")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #ui.drawCurve(eeg)
    # ui.cal_content()
    MainWindow.show()
    # t = QtCore.QTimer()
    # t.timeout.connect(ui.updateData)
    # t.start(100)
    sys.exit(app.exec_())
