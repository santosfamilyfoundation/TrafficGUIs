#!/usr/bin/env python
import sys
import shutil
from custom.videoplayer import VideoPlayer
from PyQt4 import QtGui, QtCore
from safety_main import Ui_TransportationSafety
from subprocess import call 

##############################################3
# testing feature objects 
# import display-trajectories

###############################################

import os 
from PyQt4.phonon import Phonon
import ConfigParser
from PyQt4.QtGui import *

import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from app_config import AppConfig as ac
import pm

from plotting import visualization


class Organizer(object):  # TODO: Phase out.
    def __init__(self):
        super(Organizer, self).__init__()


class MainGUI(QtGui.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_TransportationSafety()
        self.ui.setupUi(self)
        self.newp = pm.ProjectWizard(self)
        
        # Experimenting with organizational objects
        self.homography = Organizer()
        self.feature_tracking = Organizer()
        self.results = Organizer()

        # Connect Menu actions
        self.ui.actionOpen_Project.triggered.connect(self.open_project)
        self.ui.actionNew_Project.triggered.connect(self.create_new_project)
        # self.ui.actionLoad_Image.triggered.connect(self.open_image)
        self.ui.actionAdd_Replace_Aerial_Image.triggered.connect(self.homography_open_image_aerial)  # TODO: New method. Check which tab is open. Move to homography tab if not already there. Then call open_image_aerial.
        self.ui.actionAdd_Replace_Aerial_Image.triggered.connect(self.homography_open_image_camera)
        self.ui.main_tab_widget.setCurrentIndex(0)  # Start on the first tab

        # Connect button actions
        self.ui.homography_button_open_aerial_image.clicked.connect(self.homography_open_image_aerial)
        self.ui.homography_button_open_camera_image.clicked.connect(self.homography_open_image_camera)

        # Connect back + continue buttons
        self.ui.homography_continue_button.clicked.connect(self.show_next_tab)
        self.ui.feature_tracking_continue_button.clicked.connect(self.show_next_tab)
        self.ui.feature_tracking_back_button.clicked.connect(self.show_prev_tab)

##############################################################################################################################################     

        # back button for track roadusers 
        self.ui.roadusers_tracking_back_button.clicked.connect(self.show_prev_tab) 
        self.ui.roadusers_tracking_continue_button.clicked.connect(self.show_next_tab) 

##########################################################################################################################################

        # Track features page


        self.videoplayer = VideoPlayer()
        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer.openVideo)
        self.ui.feature_tracking_video_layout.addWidget(self.videoplayer)
        self.videoplayer.loadVideo("/home/reggert/Documents/easthall/3.mp4")

    
        # config 
        self.configGui_features = configGui_features()
        self.ui.actionOpen_Config.triggered.connect(self.configGui_features.openConfig)
        self.ui.feature_tracking_parameter_layout.addWidget(self.configGui_features)

        # test button 
        self.ui.button_feature_tracking_test.clicked.connect(self.test_feature)

##########################################################################################################################################

        # roadusers page 

        # video play 
        self.videoplayer3 = VideoPlayer() 
        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer3.openVideo)
        self.ui.roadusers_tracking_video_layout.addWidget(self.videoplayer3)
        self.videoplayer3.loadVideo("/home/reggert/Documents/easthall/3.mp4")


        # config 
        self.configGui_object = configGui_object()
        self.ui.actionOpen_Config.triggered.connect(self.configGui_object.openConfig)
        self.ui.roadusers_tracking_parameter_layout.addWidget(self.configGui_object)

        # test button 
        self.ui.button_roadusers_tracking_test.clicked.connect(self.test_object)


###########################################################################################################################################
        # self.ui.track_image.mousePressEvent = self.get_image_position

        ## CONFIGURE HOMOGRAPHY ##
        self.ui.homography_hslider_zoom_camera_image.zoom_target = self.ui.homography_cameraview
        self.ui.homography_hslider_zoom_aerial_image.zoom_target = self.ui.homography_aerialview
        self.ui.homography_hslider_zoom_computed_image.zoom_target = self.ui.homography_results
        self.ui.homography_cameraview.status_label = self.ui.homography_camera_status_label
        self.ui.homography_aerialview.status_label = self.ui.homography_aerial_status_label
        self.show()

######################################################################################################

    def test_feature(self):
        # self.features = configGui_features() 
         # self.btn.clicked.connect(self.createConfig_features)

        # self.features.createConfig_features
        
        call(["feature-based-tracking","tracking.cfg","--tf","--database-filename","test1.sqlite"])
        call(["display-trajectories.py","-i","7.mp4","-d","test1.sqlite","-o","homography.txt","-t","feature"])


    def test_object(self):
        call(["feature-based-tracking","tracking.cfg","--tf","--database-filename","test1.sqlite"])
        call(["feature-based-tracking","tracking.cfg","--gf","--database-filename","test1.sqlite"])
        call(["display-trajectories.py","-i","7.mp4","-d","test1.sqlite","-o","homography.txt","-t","object"])
                   
################################################################################################33
    def homography_load_aerial_image(self):
        pass

    def show_next_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        self.ui.main_tab_widget.setCurrentIndex(curr_i + 1)

    def show_prev_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        self.ui.main_tab_widget.setCurrentIndex(curr_i - 1)

    def results_plot_plot1(self):
        data = [random.random() for i in range(10)]
        # create an axis
        ax = self.figure1.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas1.draw()

    def results_plot_plot2(self):
        data1 = [random.random() for i in range(50)]
        # create an axis
        ax = self.figure2.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(data1, '*-')
        # refresh canvas
        self.canvas2.draw()

    def open_project(self):
        fname = QtGui.QFileDialog.getExistingDirectory()
        #     self, 'Open Project', '/home')
        # print(fname)
        pass

    def create_new_project(self):
        self.newp.restart()
        self.newp.show()

    def homography_open_image_camera(self):
        """Opens a file dialog, allowing user to select an camera image file.

        Creates a QImage object from the filename of an camera image
        selected by the user in a popup file dialog menu.
        """
        qi = self.open_image_fd(dialog_text="Select camera image...")
        if qi:
            self.ui.homography_cameraview.load_image(qi)

    def homography_open_image_aerial(self):
        """Opens a file dialog, allowing user to select an aerial image file.

        Creates a QImage object from the filename of an aerial image
        selected by the user in a popup file dialog menu.
        """
        qi = self.open_image_fd(dialog_text="Select aerial image...")
        if qi:
            self.ui.homography_aerialview.load_image(qi)

    def open_image_fd(self, dialog_text="Open Image", default_dir=""):
        """Opens a file dialog, allowing user to select an image file.

        Creates a QImage object from the filename selected by the user in the
        popup file dialog menu.

        Args:
            dialog_text [Optional(str.)]: Text to prompt user with in open file
                dialog. Defaults to "Open Image".
            default_dir [Optional(str.)]: Path of the default directory to open
                the file dialog box to. Defaults to "".

        Returns:
            QImage: Image object created from selected image file.
            None: Returns None if no file was selected in the dialog box.
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, dialog_text, default_dir)  # TODO: Filter to show only image files
        if fname:
            image = QtGui.QImage(fname)
        else:
            image = None
        return image

    def get_image_position(self, event):
        print(event.pos())
        print(self._tracking_image.image.pixel(event.x(), event.y()))


##########################################################################################################################

class configGui_features(QtGui.QWidget):

    
    def __init__(self):
        super(configGui_features, self).__init__()
        
        self.initUI()
        

    def initUI(self): 

     
        # lbl1.move(15, 10)

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.createConfig_features)

      
        self.label1 = QtGui.QLabel("first frame to process")
        # input box 
        self.input1 = QtGui.QLineEdit()
        # self.input1.setMaximumWidth(10)

        self.label2 = QtGui.QLabel("number of frames to process")
        # self.label1.move(130, 22)
        self.input2 = QtGui.QLineEdit()
        # self.le.move(150, 22)

        self.label3 = QtGui.QLabel("Max number of features added at each frame")
        self.input3 = QtGui.QLineEdit()

        self.label4 = QtGui.QLabel("Number of deplacement to test")
        # self.input4 = QtGui.QLineEdit()

        self.label5 = QtGui.QLabel("minimum feature motion")
        self.input5 = QtGui.QLineEdit()

        self.label6 = QtGui.QLabel("Minimum displacement to keep features (px)")
        self.input6 = QtGui.QLineEdit()

        self.label7 = QtGui.QLabel("Max number of iterations")
        # self.input7 = QtGui.QLineEdit()

        self.label8 = QtGui.QLabel("to stop feature tracking")
        self.input8 = QtGui.QLineEdit()

        self.label9 = QtGui.QLabel("Minimum number of frames to consider")
        # self.input7 = QtGui.QLineEdit()

        self.label10 = QtGui.QLabel("a feature for grouping")
        self.input10 = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.label1, 2, 0)
        grid.addWidget(self.input1, 2, 1)

        grid.addWidget(self.label2, 3, 0)
        grid.addWidget(self.input2, 3, 1)

        grid.addWidget(self.label3, 4, 0)
        grid.addWidget(self.input3, 4, 1)

        grid.addWidget(self.label4, 5, 0)
       
        grid.addWidget(self.label5, 6, 0)
        grid.addWidget(self.input5, 6, 1)

        grid.addWidget(self.label6, 7, 0)
        grid.addWidget(self.input6, 7, 1)

        grid.addWidget(self.label7, 8, 0)

        grid.addWidget(self.label8, 9, 0)
        grid.addWidget(self.input8, 9, 1)

        grid.addWidget(self.label9, 10, 0)

        grid.addWidget(self.label10, 11, 0)
        grid.addWidget(self.input10, 11, 1)

        grid.addWidget(self.btn, 12, 0)

        self.setLayout(grid) 

        # size gets fixed
        # self.setFixedSize(450,350)
        
        # window box location and size 
        # self.setGeometry(500, 100, 150, 20)

        self.setWindowTitle('Input config')
        # self.show()

        # opens a cofig file 
    def openConfig(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', '/') 
        global path1
        path1= str(path)

        # path1 = "../project_dir/test1"
        
       
    def createConfig_features(self,path):
        """
        Create a config file
        """

        global path1
        # path1= str(path)

        # update test1 name with project chosen 

        # path1 = "../project_dir/test1/tracking.cfg"
        
        config = ConfigParser.ConfigParser()

        # # if not os.path.exists("../project_dir/test1"):
        # #     os.mkdir("../project_dir/test1")
        # if os.path.exists("../project_dir/test1/feature_tracking.cfg"):
        #     os.remove("../project_dir/test1/feature_tracking.cfg")
        # shutil.copyfile("feature_tracking.cfg","../project_dir/test1/tracking.cfg")

        # add new content to config file 
        config.add_section("added")
        config.set("added", "frame1", self.input1.text())
        config.set("added", "nframes", self.input2.text())
        config.set("added", "max-nfeatures", self.input3.text())
        config.set("added", "ndisplacements", self.input5.text())
        config.set("added", "min-feature-displacement", self.input6.text())
        config.set("added", "max-number-iterations", self.input8.text())
        config.set("added", "min-feature-time", self.input10.text())


        try:
            path1
        except NameError:
          # self.player.load(Phonon.MediaSource(""))
            error = QtGui.QErrorMessage()
            error.showMessage('''\
            no config files chosen''')
            error.exec_()
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


##########################################################################################################################

class configGui_object(QtGui.QWidget):

    
    def __init__(self):
        super(configGui_object, self).__init__()
        
        self.initUI()
        

    def initUI(self): 

     
        # lbl1.move(15, 10)

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.createConfig_objects)

      
        self.label1 = QtGui.QLabel("first frame to process")
        # input box 
        self.input1 = QtGui.QLineEdit()
        # self.input1.setMaximumWidth(10)

        self.label2 = QtGui.QLabel("number of frames to process")
        # self.label1.move(130, 22)
        self.input2 = QtGui.QLineEdit()
        # self.le.move(150, 22)

        self.label3 = QtGui.QLabel("maximum connection-distance")
        self.input3 = QtGui.QLineEdit()

        self.label4 = QtGui.QLabel("maximum segmentation-distance")
        self.input4 = QtGui.QLineEdit()


        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        

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

        self.setWindowTitle('Input config')
        # self.show()

        # opens a cofig file 
    def openConfig(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', '/') 
        # global path1
        path1= str(path)
        
       
    def createConfig_objects(self,path):
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
            error = QtGui.QErrorMessage()
            error.showMessage('''\
            no config files chosen''')
            error.exec_()
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


##########################################################################################################################

def main():
    app.exec_()

if __name__ == '__main__':
    ac.load_application_config()
    app = QtGui.QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(main())
