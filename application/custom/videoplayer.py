from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon

class VideoPlayer(QtGui.QWidget):

    def __init__(self, parent = None):


        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)

        self.player = Phonon.VideoPlayer(Phonon.VideoCategory,self)

        self.pause = QtGui.QPushButton('Play/Pause',self)
        self.pause.clicked.connect(self.playPause)


        self.slider = Phonon.SeekSlider(self.player.mediaObject() , self)

        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        
        topLayout = QtGui.QVBoxLayout(self)
        topLayout.addWidget(self.player)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.pause)
        layout.addWidget(self.slider)
        topLayout.addLayout(layout)
        self.setLayout(topLayout)

    def playPause(self):
    # allows the video to load through whenever a new file is chosen 
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

    def gettingTime(self):
        startMinutes = int(self.minutes.text())
        startSeconds = int(self.seconds.text())
        endMinutes = int(self.endMinutes.text())
        endSeconds = int(self.endSeconds.text())
        startTime = (startMinutes*60+startSeconds)
        endTime = (endMinutes*60+endSeconds)
        self.player.seek(startTime*1000)


    def loadVideo(self,filename):
        self.player.load(Phonon.MediaSource(filename))
        self.player.mediaObject().setTickInterval(100)
        self.player.mediaObject().tick.connect(self.tock)
        self.player.play()
        self.player.pause()