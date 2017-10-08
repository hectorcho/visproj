__author__ = "Hector Yong Hyun Cho"
__version__ = "0.0.1"

import sys
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np

from ui_menubar import Ui_Menubar
from vlc_widget import VLCPlayerWidget

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
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1920, 1080)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.vlcWidget = QtGui.QWidget(self.centralWidget)
        self.vlcWidget.setGeometry(QtCore.QRect(20, 10, 1280, 720))
        self.vlcWidget.setObjectName(_fromUtf8("vlcWidget"))
        self.l = QtGui.QVBoxLayout()
        self.vlcWidget.setLayout(self.l)

        self.vlcplayer = VLCPlayerWidget()
        self.l.addWidget(self.vlcplayer)




        self.graphicsView = PlotWidget(self.centralWidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 750, 1280, 270))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

        #refer to drawCurve() method below
        self.drawCurve()


        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def drawCurve(self):
        self.x = np.arange(1000)
        self.y = np.random.normal(size=(3,1000))
        for i in range(3):
            self.graphicsView.plot(self.x, self.y[i], pen=(i,3))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
