from PyQt4 import QtGui, QtCore
import os, threading, time


class VideoFramePlayer(QtGui.QWidget):
    redraw_signal = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)

        self.label = QtGui.QLabel(self)

        self.pause = QtGui.QPushButton('Play/Pause',self)
        self.pause.clicked.connect(self.playPause)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.sliderChanged)

        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        # Sets the image frames for this player to display
        self.max_frame_rate = 5.0
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

    def setImage(self, image_path):
        scaledImage = QtGui.QPixmap(image_path).scaled(self.label.size(), QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(scaledImage)

    def playPause(self):
        if self.timer:
            # Calling the timer function stops the timer.
            self.timer()
            self.timer = None
            return

        # If no timer was set, we were paused. Now, we should check if we're already at the end
        # and restart from the beginning
        if self.currentFrame >= len(self.frames):
            self.currentFrame = 0

        event = threading.Event()

        def stepForward():
            while not event.wait(1/self.max_frame_rate):
                self.currentFrame += int(self.frame_rate/self.max_frame_rate)

                if self.currentFrame >= len(self.frames):
                    self.timer()
                    self.timer = None
                    return

                sliderPosition = int(self.currentFrame / float(len(self.frames)) * 100)
                self.slider.setValue(sliderPosition)

                # We have to use a signal to redraw so that the redraw happens on the main thread
                self.redraw_signal.emit()

        threading.Thread(target=stepForward).start()
        self.timer = event.set

    def updateImage(self):
        if len(self.frames) > 0 and self.currentFrame < len(self.frames):
            self.setImage(self.frames[self.currentFrame])

    def sliderChanged(self):
        '''
        This method will be called when the slider is dragged by the user. The value() of the slider ranges from 1-99
        '''
        size = self.slider.value()
        frame = int(size/99.0*(len(self.frames)-1))
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

    def loadFrames(self, directory, frame_rate, prefix='image-', extension='png'):
        '''
        This function takes a directory that holds a set of images, named 'image-001.png', 'image-002.png', etc.
        and loads them into the frame player
        '''
        self.frame_rate = frame_rate
        frames = []
        count = 0
        success = True
        while success:
            if '.' in extension:
                format_string = "%d"
            else:
                format_string = "%d."
            filename = prefix + format_string + extension
            path = os.path.join(directory, filename % count)

            if os.path.exists(path):
                frames.append(path)
            else:
                success = False

            count += 1

        self.frames = frames
        self.reconfigurePlayer()

    def reconfigurePlayer(self):
        num_frames = len(self.frames)
        self.slider.minimum = 0
        self.slider.maximum = num_frames
        self.slider.setValue(0)
        self.currentFrame = 0
        self.updateImage()