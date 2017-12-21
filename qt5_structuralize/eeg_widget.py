import sys
import os
import user
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import PyQt5.QtMultimedia as QM
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as np
import math
import pandas
import pyqtgraph

class eegWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.time = 0
        self.eeg = None

        self.view = pyqtgraph.PlotWidget()
        self.view.setGeometry(QtCore.QRect(20, 520, 860, 380))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.view)
        self.createUI()


    def createUI(self):

        # video position slider
        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        self.positionSlider.valueChanged.connect(self.update_eeg_graph)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.openbutton = QtWidgets.QPushButton("Open EEG")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)

        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.setLayout(self.layout)

    def update_eeg_graph(self):
        if(self.eeg is not None and self.eeg.shape[0] != 0):
            self.updateData(self.eeg[0][-1] * self.positionSlider.value() / 1000)

    def lowestGreaterThan(self, arr, threshold):
        # print(arr.shape)
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
        # print(arr.shape)
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

    def drawCurve(self, eeg):
        self.eeg = eeg
        self.time = 0
        start_time = self.time - 2000
        end_time = self.time + 2000
        max = np.max(eeg[1, :])
        min = np.min(eeg[1, :])
        self.y, self.x = self.cal_content(start_time=start_time, end_time=end_time)
        self.view.setYRange(min, max)
        self.view_plot = self.view.plot(self.x, self.y, pen=(0,1))

    def cal_content(self, start_time=-2000, end_time=2000):
        low = self.lowestGreaterThan(self.eeg[0, :], start_time)
        high = self.GreatestLowerThan(self.eeg[0, :], end_time)
        # limit the index in case out of array bound
        low = min(self.eeg.shape[1] - 1,max(0,low))
        high = max(0,min(self.eeg.shape[1] - 1, high))
        # print(start_time, end_time, self.eeg[0, low], self.eeg[0, high], low, high)
        return self.eeg[1,low:high + 1], self.eeg[0,low:high + 1]

    def updateData(self, time):
        self.time = time
        start_time = self.time - 2000
        end_time = self.time + 2000
        yd, xd = self.cal_content(start_time=start_time,end_time=end_time)
        self.view.setLabel('left', 'EEG Value', units='V')
        self.view.setLabel('bottom', 'Time', units='ms')
        self.view.setXRange(start_time, end_time)
        self.view_plot.setData(y=yd, x=xd)

    def open_file(self, filename=None):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open EYE", user.home)
        if not filename:
            return
        self.drawCurve(np.loadtxt(str(filename), delimiter=",")[0:2, :])

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = eegWidget()
    w.show()
    sys.exit(app.exec_())