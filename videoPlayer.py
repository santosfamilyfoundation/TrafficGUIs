import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.phonon import Phonon
#from moviepy.editor import *

class VideoPlayer(QtGui.QWidget):
    def __init__(self, parent = None):


        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)
        self.fileName = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME')))

        self.player = Phonon.VideoPlayer(Phonon.VideoCategory,self)
        self.player.load(Phonon.MediaSource(self.fileName))
        self.player.mediaObject().setTickInterval(100)
        self.player.mediaObject().tick.connect(self.tock)

        self.play_pause = QtGui.QPushButton('play/pause',self)
        self.play_pause.clicked.connect(self.playClicked)


        self.slider = Phonon.SeekSlider(self.player.mediaObject() , self)
        self.minutes = QtGui.QLineEdit('min',self)
        self.seconds = QtGui.QLineEdit('sec',self)
        self.endMinutes = QtGui.QLineEdit('End Min',self)
        self.endSeconds = QtGui.QLineEdit('End Sec',self)
        self.getTime = QtGui.QPushButton('set time period', self)
        self.getTime.clicked.connect(self.gettingTime)


        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        
        topLayout = QtGui.QVBoxLayout(self)
        topLayout.addWidget(self.player)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.play_pause)
        layout.addWidget(self.slider)
        layout.addWidget(self.minutes)
        layout.addWidget(self.seconds)
        layout.addWidget(self.endMinutes)
        layout.addWidget(self.endSeconds)
        layout.addWidget(self.getTime)
        topLayout.addLayout(layout)
        self.setLayout(topLayout)

    def playClicked(self):
        if self.player.mediaObject().state() == Phonon.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def tock(self, time):
        time = time/1000
        h = time/3600
        m = (time-3600*h) / 60
        s = (time-3600*h-m*60)
        self.status.setText('%02d:%02d:%02d'%(h,m,s))

    # def cutVideoClip(self,startTime,endTime,fps = 25):
    #     print os.path.split(self.fileName)[1]
    #     video = VideoFileClip(os.path.split(self.fileName)[1]).subclip(startTime,endTime)
    #     result = CompositeVideoClip([video])
    #     result.write_videofile("temp.mp4",fps)

    def gettingTime(self):
        startMinutes = int(self.minutes.text())
        startSeconds = int(self.seconds.text())
        endMinutes = int(self.endMinutes.text())
        endSeconds = int(self.endSeconds.text())
        startTime = (startMinutes*60+startSeconds)
        endTime = (endMinutes*60+endSeconds)
        self.player.seek(startTime*1000)
        #self.cutVideoClip(startTime,endTime)


def main():
    app = QtGui.QApplication(sys.argv)
    window=VideoPlayer()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()