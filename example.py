import sys
import os
import user
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import numpy as np
import math
import pandas

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.layout = QVBoxLayout(self)
        self.mo = Phonon.MediaObject()
        self.vw = Phonon.VideoWidget()
        self.vw.setGeometry(QRect(0,0,1280,720))
        self.vw.AspectRatio16_9
        self.vw.FitInView
        Phonon.createPath(self.mo, self.vw)
        self.ao = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mo, self.ao)

        #####################       eye tracking        #####################
        self.audience_eye_tracking_dic = {}
        self.eye_track_dic = {}
        self.eye_track_frame_rate = 5
        self.trial_lapse = 2000
        #####################       eye tracking        #####################

        # self.open_file()
        self.mo.setTickInterval(self.eye_track_frame_rate)
        self.mo.tick.connect(self.draw_eye_tracking)


        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)

        self.layout.addWidget(self.view)
        self.createUI()

        self.proxy = self.scene.addWidget(self.vw)
        # or
        # proxy = QGraphicsProxyWidget()
        # scene.addItem(proxy)

        #####################       eye tracking        #####################
        self.lines = [];
        self.dot = None;
        #  initially item should not be seen by user
        # self.item2 = self.scene.addEllipse(QRectF(0,0,20,20), QPen(Qt.green), QBrush(Qt.green))
        # self.item2.setParentItem(self.proxy)
        #####################       eye tracking        #####################

    def createUI(self):

        # video position slider
        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setMaximum(1000)
        self.connect(self.positionSlider,
                     SIGNAL("sliderMoved(int)"), self.setPosition)

        # play button
        self.hbuttonbox = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.connect(self.playbutton, SIGNAL("clicked()"), self.play_pause)

        self.openbutton = QPushButton("Open")
        self.hbuttonbox.addWidget(self.openbutton)
        self.connect(self.openbutton, SIGNAL("clicked()"), self.open_file)

        self.openbutton2 = QPushButton("Open EYE")
        self.hbuttonbox.addWidget(self.openbutton2)
        self.connect(self.openbutton2, SIGNAL("clicked()"), self.open_eye)


        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.setLayout(self.layout)



    def open_file(self, filename = None):

        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Open File", user.home)
        if not filename:
            return
        media = Phonon.MediaSource(filename)
        self.mo.setCurrentSource(media)

    def open_eye(self, filename = None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Open EYE", user.home)
        if not filename:
            return
        self.create_eye_tracking_reference_dict(pandas.read_excel(str(filename)))

    def play_pause(self):

        if self.mo.state() == 1 :
            self.mo.play()
            self.playbutton.setText("Pause")

        elif self.mo.state() == 2 :
            self.mo.pause()
            self.playbutton.setText("Play")

        elif self.mo.state() == 4 :
            self.mo.play()
            self.playbutton.setText("Pause")

    def setPosition(self, position):
        self.mo.pause()
        self.mo.seek(self.mo.totalTime() / 1000 * position)

    def updateUI(self):
        self.positionSlider.setValue(self.mo.currentTime() * 1000 / self.mo.totalTime())

    # def resizeEvent(self, event):
    #    if event.oldSize().isValid():
    #        print(self.view.scene().sceneRect())
    #        self.view.fitInView(self.view.scene().sceneRect(), Qt.KeepAspectRatio)
    #    QWidget.resizeEvent(self, event)

    #####################       eye tracking        #####################

    def draw_dot_line(self, v):
        if self.mo.state() == 2:
            pos = v['pos']
            # print v
            self.updateUI()
            if self.dot is not None:
                self.dot.setPos(QPoint(pos[0],pos[1]))
            else:
                self.dot = self.scene.addEllipse(QRectF(0, 0, 20, 20), QPen(Qt.red), QBrush(Qt.red))
                self.dot.setParentItem(self.proxy)
            j = 0
            for i in range(len(v['lines'])):
                j = i
                if i >= len(self.lines):
                    self.lines.append(self.scene.addLine(QLineF(v['lines'][i][0][0],v['lines'][i][0][1],
                                                                v['lines'][i][1][0], v['lines'][i][1][1]),
                                                         QPen(Qt.red)))
                    self.lines[-1].setParentItem(self.proxy)
                else:
                    self.lines[i].setLine(QLineF(v['lines'][i][0][0],v['lines'][i][0][1],
                                                                v['lines'][i][1][0], v['lines'][i][1][1]))
            if len(self.lines) > j:
                del self.lines[j:-1]
            # self.item.setPos(QPoint())
            # self.item2.setPos(QPoint(640,360))
            # print self.mo.currentTime()
            # print self.mo.state()
            # print pos


    def create_eye_tracking_reference_dict(self, excel):
        self.audience_eye_tracking_dic['an1'] = {'pos': [], 'lines': []}
        self.eye_track_window = 1000 / self.eye_track_frame_rate
        self.eye_track_dic = {}
        self.eye_track_dic['an1'] = []
        last_one = int(excel['CURRENT_FIX_START'][521] / self.eye_track_window)
        head = 0
        for i in range(last_one):
            start_time = i * self.eye_track_window
            updated_flag=False
            while head < len(excel['CURRENT_FIX_START'].index):
                if excel['CURRENT_FIX_START'][head] > start_time:
                    break
                if excel['CURRENT_FIX_START'][head] <= start_time and start_time <= excel['CURRENT_FIX_END'][head]:
                    self.eye_track_dic['an1'].append([excel['CURRENT_FIX_X'][head], excel['CURRENT_FIX_Y'][head]])
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
        if len(self.eye_track_dic.keys()) == 0 or self.mo.state() != 2:
            return
        media_time = self.mo.currentTime()
        for k,v in self.audience_eye_tracking_dic.iteritems():
            eye_tracking_window_index = int(media_time / self.eye_track_window)
            v['pos'] = self.eye_track_dic[k][eye_tracking_window_index]
            v['lines'] = []
            if len(v['pos']) == 2:
                for line_num in range(int(self.trial_lapse / self.eye_track_window)):
                    if eye_tracking_window_index - line_num -1 >= 0 and len(self.eye_track_dic[k][eye_tracking_window_index - line_num - 1]) == 2:
                        v['lines'].append([self.eye_track_dic[k][eye_tracking_window_index - line_num - 1], self.eye_track_dic[k][eye_tracking_window_index - line_num]])
                self.draw_dot_line(v)

#####################       eye tracking        #####################


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
