import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.phonon import Phonon
import io
import ConfigParser
from PyQt4.QtGui import *
 


###################################################################################### 

class configGui(QtGui.QWidget):

    
    def __init__(self):
        super(configGui, self).__init__()
        
        self.initUI()
        

    def initUI(self): 

     
        # lbl1.move(15, 10)

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.createConfig)

      
        self.label1 = QtGui.QLabel("first frame to process")
        # input box 
        self.input1 = QtGui.QLineEdit()

        self.label2 = QtGui.QLabel("number of frames to process")
        # self.label1.move(130, 22)
        self.input2 = QtGui.QLineEdit()
        # self.le.move(150, 22)

        self.label3 = QtGui.QLabel("maximum connection-distance")
        self.input3 = QtGui.QLineEdit()

        self.label4 = QtGui.QLabel("maximum segmentation-distance")
        self.input4 = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        grid.setSpacing(1)
        

        grid.addWidget(self.label1, 2, 0)
        grid.addWidget(self.input1, 2, 1)

        grid.addWidget(self.label2, 3, 0)
        grid.addWidget(self.input2, 3, 1)

        grid.addWidget(self.label3, 4, 0)
        grid.addWidget(self.input3, 4, 1)

        grid.addWidget(self.label4, 5, 0)
        grid.addWidget(self.input4, 5, 1)

        grid.addWidget(self.btn, 6, 0)

        # path1 = "3"

        self.setLayout(grid) 

        # size gets fixed
        self.setFixedSize(450,350)
        
        # window box location and size 
        self.setGeometry(500, 100, 150, 20)

        self.setWindowTitle('Input config')
        # self.show()
        
       
    def createConfig(self,path):
        """
        Create a config file
        """
        config = ConfigParser.ConfigParser()

        # add new content to config file 
        config.add_section("added")
        config.set("added", "frame1", self.input1.text())
        config.set("added", "nframes", self.input2.text())
        config.set("added", "mm-connection-distance", self.input3.text())
        config.set("added", "mm-segmentation-distance", self.input4.text())

        try:
            path1
        except NameError:
          # self.player.load(Phonon.MediaSource(""))
            print "no config chosen"
        else:
            with open(path1,"a") as config_file:
                config.write(config_file)

            # to remove the section header from config file  

            #opens the file to read      
            f = open(path1,"r")
            lines = f.readlines()
            f.close()
            #opens the file to write 
            f = open(path1,"w")
            for line in lines:
                #removes the section header 
                if line!="[added]"+"\n":
                    f.write(line)
            f.close()

        # self.path1 = "dash"     
        # grid = QtGui.QGridLayout()
        # self.lbl1 = QtGui.QLabel(self.path1)
        # grid.addWidget(lbl1, 1, 0)
        # self.setLayout(grid) 


######################################################################################3
 
class VideoPlayer(QtGui.QWidget):
    def __init__(self, parent = None):


        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
            QtGui.QSizePolicy.Preferred)
        # filename = 1
        # self.filename = filename
        # print filename
        self.player = Phonon.VideoPlayer(Phonon.VideoCategory,self)

        self.play_pause = QtGui.QPushButton('Load Video',self)
        self.play_pause.clicked.connect(self.playClicked)

        self.pause = QtGui.QPushButton('Play/Pause',self)
        self.pause.clicked.connect(self.playPause)


        self.slider = Phonon.SeekSlider(self.player.mediaObject() , self)
        # self.minutes = QtGui.QLineEdit('min',self)
        # self.seconds = QtGui.QLineEdit('sec',self)
        # self.endMinutes = QtGui.QLineEdit('End Min',self)
        # self.endSeconds = QtGui.QLineEdit('End Sec',self)
        # self.getTime = QtGui.QPushButton('set time period', self)
        # self.getTime.clicked.connect(self.gettingTime)


        self.status = QtGui.QLabel(self)
        self.status.setAlignment(QtCore.Qt.AlignRight |
            QtCore.Qt.AlignVCenter)

        
        topLayout = QtGui.QVBoxLayout(self)
        topLayout.addWidget(self.player)
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(self.play_pause)
        layout.addWidget(self.pause)
        layout.addWidget(self.slider)
        # layout.addWidget(self.minutes)
        # layout.addWidget(self.seconds)
        # layout.addWidget(self.endMinutes)
        # layout.addWidget(self.endSeconds)
        # layout.addWidget(self.getTime)
        topLayout.addLayout(layout)
        self.setLayout(topLayout)

    def playClicked(self):
        # allows the video to load through whenever a new file is chosen 

        # try is needed incase no file is chosen by the user 

        try:
            filename
        except NameError:
            self.player.load(Phonon.MediaSource(""))

        else:
            self.player.load(Phonon.MediaSource(filename))
            self.player.mediaObject().setTickInterval(100)
            self.player.mediaObject().tick.connect(self.tock)
            self.player.play()



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

###############################################################################

# combines the two features to be displayed in the main window 
 
class Combine(QtGui.QWidget):
    
    def __init__(self):
        super(Combine, self).__init__()        
        self.initUI()
        
    def initUI(self):
        self.configGui = configGui()
        self.videoplayer = VideoPlayer()
   
        title = QtGui.QLabel('Title')
 
        titleEdit = QtGui.QLineEdit()
        grid = QtGui.QGridLayout()
        grid.setSpacing(70)

        grid.addWidget(self.videoplayer, 1, 0)
        grid.addWidget(self.configGui, 1, 1)  
        self.setLayout(grid) 
        # self.show()

############################################################################### 

class Mainwindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.initUI()

# central content
        self.combine = Combine()
        self.setCentralWidget(self.combine)


# menu bar 
    def initUI(self):  

    # Open Config File 
        openconfigFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open Config', self)
        openconfigFile.setStatusTip('Open new Config file')
        openconfigFile.triggered.connect(self.openConfig)

    # Open Video File 
        openvideoFile = QtGui.QAction(QtGui.QIcon('open2.png'), 'Open Video', self)
        openvideoFile.setStatusTip('Open new Video file')
        openvideoFile.triggered.connect(self.openVideo)


    # Exit             
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openvideoFile)
        fileMenu.addAction(openconfigFile)
        fileMenu.addAction(exitAction)
        
        self.setGeometry(1000, 0, 2100, 700)
        self.setWindowTitle('Traffic Metrics')    
        self.show()

    # opens a video file 
    def openVideo(self):        
        # filevideo = 
        global filename 
        filename = str(QtGui.QFileDialog.getOpenFileName(self,'Open File', os.getenv('HOME')))
        # print filename
    

    # opens a cofig file 
    def openConfig(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', '/') 
        global path1
        path1= str(path)


###########################################################################################


def main():
    app = QtGui.QApplication(sys.argv)
    ex2= Mainwindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()