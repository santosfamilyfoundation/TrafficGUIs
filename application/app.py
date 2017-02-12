#!/usr/bin/env python
import sys
import shutil
import cv2
from custom.video_frame_player import VideoFramePlayer
from PyQt4 import QtGui, QtCore
from safety_main import Ui_TransportationSafety
import subprocess

from plotting.make_object_trajectories import main as db_make_objtraj

##############################################3
# testing feature objects
# import display-trajectories

###############################################

import os
from PyQt4.phonon import Phonon
import ConfigParser
from PyQt4.QtGui import *

import random
import os
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import cvutils
from app_config import get_base_project_dir, get_project_path, update_config_with_sections, get_config_with_sections, get_config_path, get_identifier
import pm
from cloud_api import api

import qt_plot

class MainGUI(QtGui.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_TransportationSafety()
        self.ui.setupUi(self)
        self.newp = pm.ProjectWizard(self)

        # Connect Menu actions
        self.ui.actionOpen_Project.triggered.connect(self.open_project)
        self.ui.actionNew_Project.triggered.connect(self.create_new_project)
        self.ui.actionFeedback.triggered.connect(self.open_feedback)
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

###########################################################################################################################################

        self.ui.roadusers_tracking_back_button.clicked.connect(self.show_prev_tab)
        self.ui.roadusers_tracking_continue_button.clicked.connect(self.show_next_tab)

##########################################################################################################################################

        # Track features page

        self.feature_tracking_video_player = VideoFramePlayer()
        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer.openVideo)
        self.ui.feature_tracking_video_layout.addWidget(self.feature_tracking_video_player)

        # config
        self.configGui_features = configGui_features()
        self.ui.feature_tracking_parameter_layout.addWidget(self.configGui_features)

        # test button
        self.ui.button_feature_tracking_test.clicked.connect(self.test_feature)

##########################################################################################################################################

        # roadusers page

        # video play
        self.roadusers_tracking_video_player = VideoFramePlayer()
        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer3.openVideo)
        self.ui.roadusers_tracking_video_layout.addWidget(self.roadusers_tracking_video_player)

        # config
        self.configGui_object = configGui_object()
        self.ui.roadusers_tracking_parameter_layout.addWidget(self.configGui_object)

        # test button
        self.ui.button_roadusers_tracking_test.clicked.connect(self.test_object)

        # run button
        self.ui.button_roadusers_tracking_run.clicked.connect(self.run)


        qt_plot.plot_results(self)
###########################################################################################################################################
        # self.ui.track_image.mousePressEvent = self.get_image_position

        ## CONFIGURE HOMOGRAPHY ##
        self.ui.homography_hslider_zoom_camera_image.zoom_target = self.ui.homography_cameraview
        self.ui.homography_hslider_zoom_aerial_image.zoom_target = self.ui.homography_aerialview
        self.ui.homography_hslider_zoom_computed_image.zoom_target = self.ui.homography_results
        self.ui.homography_cameraview.status_label = self.ui.homography_camera_status_label
        self.ui.homography_aerialview.status_label = self.ui.homography_aerial_status_label
        self.ui.homography_compute_button.clicked.connect(self.homography_compute)
        self.show()

######################################################################################################

    def test_feature(self):
        frame_start = get_config_with_sections(config_path, "config", "frame_start")
        num_frames = get_config_with_sections(config_path, "config", "num_frames")
        api.testConfig('feature',\
                            get_identifier(),\
                            frame_start = frame_start,\
                            num_frames = num_frames)

    def test_object(self):
        frame_start = get_config_with_sections(config_path, "config", "frame_start")
        num_frames = get_config_with_sections(config_path, "config", "num_frames")
        api.testConfig('object',\
                            get_identifier(),\
                            frame_start = frame_start,\
                            num_frames = num_frames)


    # for the run button
    def run(self):
        """
        Runs TrafficIntelligence trackers and support scripts.
        """
        email = get_config_with_sections(get_config_path(), 'info', 'email')
        api.analysis(get_identifier(), email=email)

################################################################################################

    def show_next_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        new_i = curr_i + 1
        self.ui.main_tab_widget.setCurrentIndex(new_i)
        if new_i is 3:  # If we are moving to the plots page
           qt_plot.plot_results(self)


    def show_prev_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        self.ui.main_tab_widget.setCurrentIndex(curr_i - 1)

    def open_project(self):
        fname = str(QtGui.QFileDialog.getExistingDirectory(self, "Open Existing Project Folder...", get_base_project_dir()))
        # TODO: Instead of select folder, perhaps select config file?
        if fname:
            project_name = os.path.basename(fname)
            pm.load_project(project_name, self)
        else:
            pass  # If no folder selected, don't load anything.

    def open_feedback(self):
        url = QtCore.QUrl('https://docs.google.com/forms/d/e/1FAIpQLSeTRwZlMUwNrbv9Nw-BddsOBGrCQjR5YXHbloPirRzB3-QoFA/viewform')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Connecting to Feedback', 'Could not open feedback form')

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

    def open_image_fd(self, dialog_text="Open Image", default_folder=""):
        """Opens a file dialog, allowing user to select an image file.

        Creates a QImage object from the filename selected by the user in the
        popup file dialog menu.

        Args:
            dialog_text [Optional(str.)]: Text to prompt user with in open file
                dialog. Defaults to "Open Image".
            default_folder [Optional(str.)]: Path of the default directory to open
                the file dialog box to. Defaults to "".

        Returns:
            QImage: Image object created from selected image file.
            None: Returns None if no file was selected in the dialog box.
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, dialog_text, default_folder)  # TODO: Filter to show only image files
        if fname:
            image = QtGui.QImage(fname)
        else:
            image = None
        return image

    def homography_compute(self):
        #TODO: display error message if points are < 4
        px_text = self.ui.unit_px_input.text()
        self.unitPixRatio = float(unicode(px_text))

        homography_path = os.path.join(get_project_path(), "homography")
        api.configHomography(\
            get_identifier(),\
            self.unitPixRatio,\
            self.ui.homography_aerialview.list_points(),\
            self.ui.homography_cameraview.list_points())

        self.unscaled_world_pts = (np.array(self.ui.homography_aerialview.list_points()))
        self.worldPts = self.unitPixRatio * self.unscaled_world_pts
        self.videoPts = np.array(self.ui.homography_cameraview.list_points())

        if len(self.worldPts) >= 4:
            if len(self.worldPts) == len(self.videoPts):
                self.homography, self.mask = cv2.findHomography(self.videoPts, self.worldPts)
            else:
                error = QtGui.QErrorMessage()
                error.showMessage('''\
                To compute the homography, please make sure you choose the same
                number of points on each image.''')
                error.exec_()
                return

        else:
            error = QtGui.QErrorMessage()
            error.showMessage('''\
            To compute the homography, please choose at least 4 points on
            each image.''')
            error.exec_()
            return

        if self.homography is None:
            return

        update_config_with_sections(get_config_path(), "homography", "unitpixelratio", str(self.unitPixRatio))
        homography_path = os.path.join(get_project_path(), "homography")

        if self.homography.size > 0:
            txt_path = os.path.join(homography_path, "homography.txt")
            np.savetxt(txt_path, self.homography)  # Save computed homography.

        corr_path = os.path.join(homography_path, "point-correspondences.txt")
        points_path = os.path.join(homography_path, "image-points.txt")

        f = open(corr_path, 'w') #save points to be loaded later
        np.savetxt(f, self.worldPts.T)
        np.savetxt(f, self.videoPts.T)
        f.close()

        with open(points_path, 'w') as pp:
            np.savetxt(pp, self.unscaled_world_pts.T)
            np.savetxt(pp, self.videoPts.T)

        self.homography_display_results()

    def homography_display_results(self):
        homography_path = os.path.join(get_project_path(), "homography")
        worldImg = cv2.imread(os.path.join(homography_path, "aerial.png"))
        videoImg = cv2.imread(os.path.join(homography_path, "camera.png"))

        invHomography = np.linalg.inv(self.homography)

        projectedWorldPts = cvutils.projectArray(invHomography, self.worldPts.T).T
        projectedVideoPts = cvutils.projectArray(self.homography, self.videoPts.T).T

        # TODO: Nicer formatting for computed goodness images
        for i in range(self.worldPts.shape[0]):
            # world image
            cv2.circle(worldImg, tuple(np.int32(np.round(self.worldPts[i] / self.unitPixRatio))), 2, cvutils.cvBlue)
            cv2.circle(worldImg, tuple(np.int32(np.round(projectedVideoPts[i] / self.unitPixRatio))), 2, cvutils.cvRed)
            cv2.putText(worldImg, str(i+1), tuple(np.int32(np.round(self.worldPts[i]/self.unitPixRatio)) + 5), cv2.FONT_HERSHEY_PLAIN, 2., cvutils.cvBlue, 2)
            # video image
            cv2.circle(videoImg, tuple(np.int32(np.round(self.videoPts[i]))), 2, cvutils.cvBlue)
            cv2.circle(videoImg, tuple(np.int32(np.round(projectedWorldPts[i]))), 2, cvutils.cvRed)
            cv2.putText(videoImg, str(i+1), tuple(np.int32(np.round(self.videoPts[i]) + 5)), cv2.FONT_HERSHEY_PLAIN, 2., cvutils.cvBlue, 2)
        aerial_goodness_path = os.path.join(homography_path, "homography_goodness_aerial.png")
        camera_goodness_path = os.path.join(homography_path, "homography_goodness_camera.png")

        cv2.imwrite(aerial_goodness_path, worldImg)  # Save aerial goodness image
        cv2.imwrite(camera_goodness_path, videoImg)  # Save camera goodness image

        self.ui.homography_results.load_image(QtGui.QImage(aerial_goodness_path))  # Load aerial goodness image into gui

##########################################################################################################################

class configGui_features(QtGui.QWidget):

    def __init__(self):
        super(configGui_features, self).__init__()
        self.initUI()

    def initUI(self):
        # lbl1.move(15, 10)

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.saveConfig_features)

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

        self.loadConfig_features()

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

        self.setWindowTitle('Input config')
        # self.show()

    def saveConfig_features(self):
        """
        Save configuration
        """
        config_path = get_config_path()

        frame_start = str(self.input1.text())
        if frame_start != "":
            update_config_with_sections(config_path, "config", "frame_start", frame_start)

        num_frames = str(self.input2.text())
        if num_frames != "":
            update_config_with_sections(config_path, "config", "num_frames", num_frames)

        max_features_per_frame = str(self.input3.text())
        if max_features_per_frame != "":
            update_config_with_sections(config_path, "config", "max_features_per_frame", max_features_per_frame)
        else: max_features_per_frame = None

        num_displacement_frames = str(self.input5.text())
        if num_displacement_frames != "":
            update_config_with_sections(config_path, "config", "num_displacement_frames", num_displacement_frames)
        else: num_displacement_frames = None

        min_feature_displacement = str(self.input6.text())
        if min_feature_displacement != "":
            update_config_with_sections(config_path, "config", "min_feature_displacement", min_feature_displacement)
        else: min_feature_displacement = None

        max_iterations_to_persist = str(self.input8.text())
        if max_iterations_to_persist != "":
            update_config_with_sections(config_path, "config", "max_iterations_to_persist", max_iterations_to_persist)
        else: max_iterations_to_persist = None

        min_feature_frames = str(self.input10.text())
        if min_feature_frames != "":
            update_config_with_sections(config_path, "config", "min_feature_frames", min_feature_frames)
        else: min_feature_frames = None


        api.configFiles(get_identifier(),\
                     max_features_per_frame = max_features_per_frame,\
                     num_displacement_frames = num_displacement_frames,\
                     min_feature_displacement = min_feature_displacement,\
                     max_iterations_to_persist = max_iterations_to_persist,\
                     min_feature_frames = min_feature_frames)

    def loadConfig_features(self):
        config_path = get_config_path()

        frame_start = get_config_with_sections(config_path, "config", "frame_start")
        num_frames = get_config_with_sections(config_path, "config", "num_frames")
        max_features_per_frame = get_config_with_sections(config_path, "config", "max_features_per_frame")
        num_displacement_frames = get_config_with_sections(config_path, "config", "num_displacement_frames")
        min_feature_displacement = get_config_with_sections(config_path, "config", "min_feature_displacement")
        max_iterations_to_persist = get_config_with_sections(config_path, "config", "max_iterations_to_persist")
        min_feature_frames = get_config_with_sections(config_path, "config", "min_feature_frames")

        if frame_start != None:
            self.input1.setText(frame_start)
        if num_frames != None:
            self.input2.setText(num_frames)
        if max_features_per_frame != None:
            self.input3.setText(max_features_per_frame)
        if num_displacement_frames != None:
            self.input5.setText(num_displacement_frames)
        if min_feature_displacement != None:
            self.input6.setText(min_feature_displacement)
        if max_iterations_to_persist != None:
            self.input8.setText(max_iterations_to_persist)
        if min_feature_frames != None:
            self.input10.setText(min_feature_frames)


##########################################################################################################################

class configGui_object(QtGui.QWidget):

    def __init__(self):
        super(configGui_object, self).__init__()
        self.initUI()

    def initUI(self):
        # lbl1.move(15, 10)

        self.btn = QtGui.QPushButton('Set Config', self)
        # self.btn.move(20, 20)
        self.btn.clicked.connect(self.saveConfig_objects)


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

        self.loadConfig_objects()

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

    def saveConfig_objects(self):
        """
        Save configuration
        """
        config_path = get_config_path()

        frame_start = str(self.input1.text())
        if frame_start != "":
            update_config_with_sections(config_path, "config", "frame_start", frame_start)

        num_frames = str(self.input2.text())
        if num_frames != "":
            update_config_with_sections(config_path, "config", "num_frames", num_frames)

        max_connection_distance = str(self.input3.text())
        if max_connection_distance != "":
            update_config_with_sections(config_path, "config", "max_connection_distance", max_connection_distance)
        else: max_connection_distance = None

        max_segmentation_distance = str(self.input4.text())
        if max_segmentation_distance != "":
            update_config_with_sections(config_path, "config", "max_segmentation_distance", max_segmentation_distance)
        else: max_segmentation_distance = None

        api.configFiles(get_identifier(),\
                     max_connection_distance = max_connection_distance,\
                     max_segmentation_distance = max_segmentation_distance)

    def loadConfig_objects(self):
        config_path = get_config_path()

        frame_start = get_config_with_sections(config_path, "config", "frame_start")
        num_frames = get_config_with_sections(config_path, "config", "num_frames")
        max_connection_distance = get_config_with_sections(config_path, "config", "max_connection_distance")
        max_segmentation_distance = get_config_with_sections(config_path, "config", "max_segmentation_distance")

        if frame_start != None:
            self.input1.setText(frame_start)
        if num_frames != None:
            self.input2.setText(num_frames)
        if max_connection_distance != None:
            self.input3.setText(max_connection_distance)
        if max_segmentation_distance != None:
            self.input4.setText(max_segmentation_distance)

##########################################################################################################################

def main():
    app.exec_()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(main())
