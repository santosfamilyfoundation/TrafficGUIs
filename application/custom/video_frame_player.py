from PyQt4 import QtGui, QtCore
import os, threading, time


class VideoFramePlayer(QtGui.QWidget):
    redraw_signal = QtCore.pyqtSignal()

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
        self.max_frame_rate = 10.0
        self.currentFrame = 0
        self.frames = []
        self.timer = None

        self.redraw_signal.connect(self.updateImage)

        topLayout = QtGui.QVBoxLayout(self)
        topLayout.addWidget(self.label)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.pause)
        layout.addWidget(self.slider)
        topLayout.addLayout(layout)
        self.setLayout(topLayout)

        self.reconfigurePlayer()

    def setImage(self, imageFilename):
        scaledImage = QtGui.QPixmap(os.path.join(os.getcwd(), imageFilename)).scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaledImage)

    def playPause(self):
        if self.timer:
            # Calling the timer function stops the timer.
            self.timer()
            self.timer = None
            print(self.timer)
            return

        event = threading.Event()

        def stepForward():
            while not event.wait(1/self.max_frame_rate):
                print(time.time())
                self.currentFrame += int(self.frame_rate/self.max_frame_rate)
                print(self.timer)
                if self.currentFrame >= len(self.frames):
                    self.timer()
                    self.timer = None
                    return
                print(self.currentFrame)
                self.redraw_signal.emit()

        threading.Thread(target=stepForward).start()    
        self.timer = event.set
        print("set timer")
        print(self.timer)


    def updateImage(self):
        if len(self.frames) > 0 and self.currentFrame < len(self.frames):
            self.setImage(self.frames[self.currentFrame])

    def sliderChanged(self):
        '''
        This method will be called when the slider is dragged by the user. The value() of the slider ranges from 1-99
        '''
        size = self.slider.value()
        frame = int(size/99.0*(len(self.frames)-1))
        print(size)
        print(frame)
        self.currentFrame = frame
        self.updateImage()

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

    def loadFrames(self, directory, frame_rate):
        '''
        This function takes a directory that holds a set of images, named 'image-001.png', 'image-002.png', etc.
        and loads them into the frame player
        '''
        self.frame_rate = frame_rate
        frames = []
        for file in os.listdir(directory):
            if file[0:6] == 'image-' and file[-4:] == '.png':
                frames.append(os.path.join(directory, file))
        self.frames = sorted(frames)
        self.reconfigurePlayer()

    def reconfigurePlayer(self):
        num_frames = len(self.frames)
        self.slider.minimum = 0
        self.slider.maximum = num_frames
        self.slider.setValue(0)
        self.currentFrame = 0
        self.updateImage()