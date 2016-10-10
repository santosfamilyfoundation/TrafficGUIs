from PyQt4 import QtGui, QtCore
import os

print(os.getcwd() + "/image.png")

class VideoFramePlayer(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)

        self.label = QtGui.QLabel(self)
        self.setImage("custom/image.png")

        self.pause = QtGui.QPushButton('Play/Pause',self)
        self.pause.clicked.connect(self.playPause)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.sliderChanged)

        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        # Sets the image frames for this player to display
        self.frames = []

        topLayout = QtGui.QVBoxLayout(self)
        topLayout.addWidget(self.label)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.pause)
        layout.addWidget(self.slider)
        topLayout.addLayout(layout)
        self.setLayout(topLayout)

        self.reconfigure_player()

    def setImage(self, imageFilename):
        scaledImage = QtGui.QPixmap(os.path.join(os.getcwd(), imageFilename)).scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaledImage)

    def playPause(self):
        print('playPause')

    def sliderChanged(self):
        '''
        This method will be called when the slider is dragged by the user. The value() of the slider ranges from 1-99
        '''
        size = self.slider.value()
        print('hi'+str(size))

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

    def loadFrames(self, directory):
        '''
        This function takes a directory that holds a set of images, named 'image-001.png', 'image-002.png', etc.
        and loads them into the frame player
        '''
        frames = []
        for file in os.listdir(directory):
            if file[0:6] == 'image-' and file[-4:] == '.png':
                frames.append(os.path.join(directory, file))
        self.frames = frames
        self.reconfigure_player()

    def reconfigure_player(self):
        num_frames = len(self.frames)
        self.slider.minimum = 0
        self.slider.maximum = num_frames
        self.slider.setValue(0)
        if num_frames > 0:
            self.setImage(self.frames[0])

    def loadVideo(self, filename):
        print('heklo')