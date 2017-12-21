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

class eyeTrackingWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        #####################       eye tracking        #####################
        self.audience_eye_tracking_dic = {}
        self.eye_track_dic = {}
        self.eye_track_frame_rate = 5
        self.trial_lapse = 2000
        self.lines = [];
        self.dot = None;
        self.eye_tracking_width = 1024
        self.eye_tracking_height = 768
        self.view_width=854
        self.view_height=480
        #####################       eye tracking        #####################

        self.layout = QtWidgets.QVBoxLayout(self)
        self.player = QM.QMediaPlayer()

        # self.qv = QVideoWidget()
        # self.scene = QGraphicsScene()
        # self.scene.setSceneRect(0, 0, self.view_width, self.view_height);
        # self.player.setVideoOutput(self.qv)
        # self.proxy = self.scene.addWidget(self.qv)
        # self.view = QGraphicsView(self.scene, self)

        self.videoItem = QGraphicsVideoItem()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.player.setVideoOutput(self.videoItem)
        self.scene.addItem(self.videoItem)

        self.view.setGeometry(0, 0, self.view_width, self.view_height)
        self.scene.setSceneRect(0, 0, self.view_width, self.view_height)
        self.videoItem.setSize(QtCore.QSizeF(self.view_width, self.view_height))
        self.videoItem.setPos(0, 0)
        self.layout.addWidget(self.view)
        self.createUI()
        self.view.show()


        # player.setInterval(self.eye_track_frame_rate)
        # timer.timeout.connect(self.draw_eye_tracking)

    def createUI(self):

        # video position slider
        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        self.positionSlider.valueChanged.connect(self.setPosition)

        # play button
        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)

        self.openbutton = QtWidgets.QPushButton("Open")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)

        self.openbutton2 = QtWidgets.QPushButton("Open EYE")
        self.hbuttonbox.addWidget(self.openbutton2)
        self.openbutton2.clicked.connect(self.open_eye)

        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.player.setNotifyInterval(1000/self.eye_track_frame_rate)
        self.player.positionChanged.connect(self.updateUI)
        self.player.positionChanged.connect(self.updateEyeTracking)
        self.player.durationChanged.connect(self.setRange)
        self.player.stateChanged.connect(self.setButtonCaption)

        self.setLayout(self.layout)

    def setButtonCaption(self,state):
        if self.player.state() == QM.QMediaPlayer.PlayingState:
            self.playbutton.setText("Pause")
        else:
            self.playbutton.setText("Play")

    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", user.home)
        if not filename:
            return
        url = QtCore.QUrl.fromLocalFile(filename)
        content = QM.QMediaContent(url)
        self.player.setMedia(content)
        self.playbutton.setText("Play")

    def open_eye(self):
        filename,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Open EYE", user.home)
        if not filename:
            return
        self.create_eye_tracking_reference_dict(pandas.read_excel(str(filename)))

    def play_pause(self):
        self.videoItem.setSize(QtCore.QSizeF(self.view_width, self.view_height))
        if self.player.state() == QM.QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def setPosition(self, position):
        self.player.setPosition(position)

    def setRange(self, duration):
        self.positionSlider.setRange(0, self.player.duration())

    def updateUI(self, position):
        self.positionSlider.setValue(position)

    def updateEyeTracking(self,position):
        if len(self.eye_track_dic.keys()) == 0:# or self.player.state() != 2:
            return
        self.draw_eye_tracking()
    # def resizeEvent(self, event):
    #    if event.oldSize().isValid():
    #        print(self.view.scene().sceneRect())
    #        self.view.fitInView(self.view.scene().sceneRect(), Qt.KeepAspectRatio)
    #    QWidget.resizeEvent(self, event)

    #####################       eye tracking        #####################

    def draw_dot_line(self, v):
        pos = v['pos']
        rad = v['rad']
        if self.dot is not None:
            self.dot.setRect(QtCore.QRectF(0, 0, rad, rad))
            self.dot.setPos(QtCore.QPoint(pos[0]-rad/2, pos[1]-rad/2))
        else:
            self.dot = self.scene.addEllipse(QtCore.QRectF(0, 0, rad, rad), QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))
            # self.dot.setParentItem(self.scene)
        j = 0
        for i in range(len(v['lines'])):
            j = i
            if i >= len(self.lines):
                self.lines.append(self.scene.addLine(QtCore.QLineF(v['lines'][i][0][0], v['lines'][i][0][1],
                                                            v['lines'][i][1][0], v['lines'][i][1][1]),
                                                     QtGui.QPen(QtCore.Qt.red)))
                # self.lines[-1].setParentItem(self.scene)
            else:
                self.lines[i].setLine(QtCore.QLineF(v['lines'][i][0][0], v['lines'][i][0][1],
                                             v['lines'][i][1][0], v['lines'][i][1][1]))
        if len(self.lines) > j:
            del self.lines[j+1:-1]

    def resolution_transfer(self, x, y, duration):
        return [x / self.eye_tracking_width * self.view_width,\
               y / self.eye_tracking_height * self.view_height, \
               3 + duration / 20.0]

    def create_eye_tracking_reference_dict(self, excel):
        self.audience_eye_tracking_dic['an1'] = {'pos': [], 'rad':0,'lines': []}
        self.eye_track_window = 1000 / self.eye_track_frame_rate
        self.eye_track_dic = {}
        self.eye_track_dic['an1'] = []
        last_one = int(excel['CURRENT_FIX_START'][521] / self.eye_track_window)
        head = 0
        for i in range(last_one):
            start_time = i * self.eye_track_window
            updated_flag = False
            while head < len(excel['CURRENT_FIX_START'].index):
                if excel['CURRENT_FIX_START'][head] > start_time:
                    break
                if excel['CURRENT_FIX_START'][head] <= start_time and start_time <= excel['CURRENT_FIX_END'][head]:
                    self.eye_track_dic['an1'].append(self.resolution_transfer(excel['CURRENT_FIX_X'][head], excel['CURRENT_FIX_Y'][head], excel['CURRENT_FIX_DURATION'][head]))
                    updated_flag = True
                    break
                head += 1
            if not updated_flag:
                if len(self.eye_track_dic['an1']) > 0:
                    self.eye_track_dic['an1'].append(self.eye_track_dic['an1'][-1])
                else:
                    self.eye_track_dic['an1'].append([])
                    # print "no positions!"
        print self.eye_track_dic

    def draw_eye_tracking(self, clean_flag=False):
        media_time = self.player.position()
        for k, v in self.audience_eye_tracking_dic.iteritems():
            eye_tracking_window_index = int(media_time / self.eye_track_window)
            if eye_tracking_window_index >= len(self.eye_track_dic[k]) \
                    or len(self.eye_track_dic[k][eye_tracking_window_index]) < 3:
                continue
            v['pos'] = self.eye_track_dic[k][eye_tracking_window_index][0:2]
            v['rad'] = self.eye_track_dic[k][eye_tracking_window_index][2]
            v['lines'] = []
            if len(v['pos']) == 2:
                for line_num in range(int(self.trial_lapse / self.eye_track_window)):
                    if eye_tracking_window_index - line_num - 1 >= 0 and len(
                            self.eye_track_dic[k][eye_tracking_window_index - line_num - 1]) == 3:
                        v['lines'].append([self.eye_track_dic[k][eye_tracking_window_index - line_num - 1],
                                           self.eye_track_dic[k][eye_tracking_window_index - line_num]])
                self.draw_dot_line(v)

                #####################       eye tracking        #####################

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = eyeTrackingWidget()
    w.show()
    sys.exit(app.exec_())