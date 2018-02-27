__author__ = "Hector Cho"
__version__ = "0.0.1"

import sys
import vlc
from PyQt4 import QtCore, QtGui

class Ui_Menubar(QtGui.QMenuBar):
    def __init__(self, parent=None):
        super(Ui_Menubar, self).__init__(parent)
        self.load_video = QtGui.QAction('&Load Video', self)
        self.load_EEG = QtGui.QAction('&Load EEG', self)
        self.load_gesture = QtGui.QAction('&Load Gesture', self)
        self.exit_action = QtGui.QAction('&Exit', self)

    def setupUi(self, Ui_Menubar):
        self.ui_menubar = QtGui.QMenuBar()

        #Instantiate File Menu as a component of MenuBar
        self.file_menu = self.ui_menubar.addMenu('&File')

        #Add File Menu actions
        self.file_menu.addAction(self.load_video)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.load_EEG)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.load_gesture)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
