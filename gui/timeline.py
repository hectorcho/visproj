import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import numpy as np


class timeline(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        self.createUI()

    def createUI(self):
        self.setGeometry(0, 700, 2000, 100)
        self.setWindowTitle('Colors')
        #self.show()


    def paintEvent(self, event):
        print(event.type())
        qp = QtGui.QPainter()
        qp.begin(self)
        print("error2")
        self.drawRectangles(qp)
        qp.end()



    def drawRectangles(self, qp):

        Y = 700
        for i in range(self.rows):
            randArr = np.random.randint(0, 256, size=(3,1))
            qp.fillRect(QtCore.QRect(self.tldata[i,6], Y, self.tldata[i,7], 5), QtGui.QColor(randArr[0], randArr[1], randArr[2]))















if __name__ == '__main__':

    #app = QtWidgets.QApplication(sys.argv)
    #t = timeline()
    print("error4")
    #t.show()
    #sys.exit(app.exec_())
