#!/usr/bin/env python
import sys
import qtawesome as qta # must be imported before any other qt imports
from custom.videographicsitem import VideoPlayer
from PyQt5 import QtGui, QtWidgets, QtCore
from views.safety_main import Ui_TransportationSafety
import subprocess
import zipfile
try:
    from PIL import Image, ImageDraw
except:
    import Image, ImageDraw

##############################################3
# testing feature objects
# import display-trajectories

###############################################

import os
import numpy as np
from app_config import get_default_project_dir, create_default_project_dir, get_project_path, update_config_with_sections, get_config_with_sections, get_config_path, get_identifier

import pm
import message_helper
import project_selector
from cloud_api import api
from cloud_api import StatusPoller
from video import save_video_frame
from utils.path_replacer import replace_path_delimiters
from utils.image_draw import draw_circle, draw_text


class MainGUI(QtWidgets.QMainWindow):
    test_feature_callback_signal = QtCore.pyqtSignal()
    test_object_callback_signal = QtCore.pyqtSignal()
    analysis_callback_signal = QtCore.pyqtSignal()
    results_callback_signal = QtCore.pyqtSignal()
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_TransportationSafety()
        self.ui.setupUi(self)
        self.newp = pm.ProjectWizard(self)
        self.pselector = project_selector.ProjectSelectionWizard(self)

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
        self.ui.homography_continue_button.clicked.connect(
            lambda: self.do_on_click(self.show_next_tab, self.open_feature_video)
            )

        # Connect callback signals
        self.test_feature_callback_signal.connect(self.get_feature_video)
        self.test_object_callback_signal.connect(self.get_object_video)
        self.analysis_callback_signal.connect(self.runResults)
        self.results_callback_signal.connect(self.retrieveResults)
        self.error_signal.connect(self.show_error)

###########################################################################################################################################

##########################################################################################################################################

        # Track features page

        self.feature_tracking_video_player = VideoPlayer()

        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer.openVideo)
        self.ui.feature_tracking_video_layout.addWidget(self.feature_tracking_video_player)

        # config
        self.configGui_features = configGui_features(self)
        self.ui.feature_tracking_parameter_layout.addWidget(self.configGui_features)

        # config prev/next buttons
        self.ui.feature_tracking_continue_button.clicked.connect(
            lambda: self.do_on_click(self.show_next_tab, self.configGui_features.saveConfig_features, self.open_object_video)
            )
        self.ui.feature_tracking_back_button.clicked.connect(
            lambda: self.do_on_click(self.show_prev_tab, self.configGui_features.saveConfig_features)
            )

        # test button
        self.ui.button_feature_tracking_test.clicked.connect(
            lambda: self.do_on_click(self.configGui_features.saveConfig_features, self.test_feature)
            )

##########################################################################################################################################

        # roadusers page

        # video play
        self.roadusers_tracking_video_player = VideoPlayer()

        # self.ui.actionOpen_Video.triggered.connect(self.videoplayer3.openVideo)
        self.ui.roadusers_tracking_video_layout.addWidget(self.roadusers_tracking_video_player)

        # config
        self.configGui_object = configGui_object(self)
        self.ui.roadusers_tracking_parameter_layout.addWidget(self.configGui_object)

        # connect prev/next buttons
        self.ui.roadusers_tracking_back_button.clicked.connect(
            lambda: self.do_on_click(self.show_prev_tab, self.configGui_object.saveConfig_objects)
            )
        self.ui.roadusers_tracking_continue_button.clicked.connect(
            lambda: self.do_on_click(self.show_next_tab, self.configGui_object.saveConfig_objects)
            )

        # test button
        self.ui.button_roadusers_tracking_test.clicked.connect(
            lambda: self.do_on_click(self.configGui_object.saveConfig_objects, self.test_object)
            )

        # runResults button
        self.ui.runAnalysisButton.clicked.connect(self.runAnalysis)


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

        # Create default project dir if it doesn't exist
        create_default_project_dir()

        self.pselector.show()

######################################################################################################

    def test_feature(self):
        frame_start = get_config_with_sections(get_config_path(), "config", "frame_start")
        num_frames = get_config_with_sections(get_config_path(), "config", "num_frames")

        success, error_message = api.testConfig(get_identifier(),\
                            'feature',\
                            frame_start = frame_start,\
                            num_frames = num_frames)

        if success:
            StatusPoller(get_identifier(), 'feature_test', 5, self.test_feature_callback).start()
            self.show_message('Your test of feature tracking has begun. When it has completed, a video will be shown in the window on the left. Please wait, this will only take about a minute.')
        else:
            self.show_error(error_message)

    def test_feature_callback(self, error_message):
        # Emitting the signal will call get_feature_video on the main thread
        if error_message is None:
            self.test_feature_callback_signal.emit()
        else:
            self.error_signal.emit(error_message)

    def open_feature_video(self):
        project_path = get_project_path()
        if project_path != '':
            video_path = os.path.join(project_path, 'feature_video', 'feature_video.mp4')
            if os.path.exists(video_path):
                self.feature_tracking_video_player.openFile(video_path)

    def get_feature_video(self):
        success, err = api.getTestConfig(get_identifier(), 'feature', os.path.join(get_project_path(), 'feature_video'))
        if success:
            self.open_feature_video()
        else:
            self.show_error(err)

    def test_object(self):
        frame_start = get_config_with_sections(get_config_path(), "config", "frame_start")
        num_frames = get_config_with_sections(get_config_path(), "config", "num_frames")
        success, err = api.testConfig(get_identifier(),\
                            'object',\
                            frame_start = frame_start,\
                            num_frames = num_frames)

        if success:
            StatusPoller(get_identifier(), 'object_test', 5, self.test_object_callback).start()

            self.show_message('Your test of object tracking has begun. When it has completed, a video will be shown in the window on the left. Please wait, this will only take about a minute.')
        else:
            self.show_error(err)

    def test_object_callback(self, error_message):
        # Emitting the signal will call get_object_video on the main thread
        if error_message is None:
            self.test_object_callback_signal.emit()
        else:
            self.error_signal.emit(error_message)

    def open_object_video(self):
        project_path = get_project_path()
        if project_path != '':
            video_path = os.path.join(project_path, 'object_video', 'object_video.mp4')
            if os.path.exists(video_path):
                self.roadusers_tracking_video_player.openFile(video_path)

    def get_object_video(self):
        success, err = api.getTestConfig(get_identifier(), 'object', os.path.join(get_project_path(), 'object_video'))
        if success:
            self.open_object_video()
        else:
            self.show_error(err)

    # for the runAnalysis button
    def runAnalysis(self):
        """
        Runs TrafficIntelligence trackers and support scripts.
        """
        email = get_config_with_sections(get_config_path(), 'info', 'email')
        success, err = api.analysis(get_identifier(), email=email)

        if success:
            StatusPoller(get_identifier(), 'safety_analysis', 15, self.analysisCallback).start()
            self.show_message('Object tracking and safety analysis is now running. This will take a few minutes. After it is done, creating a safety report will run, which will take some additional time. \n\nPlease keep the application open during analysis. If it is closed, a safety report will not be generated.\n\nIf you entered an email on the first screen, you will be notified when each step has been completed.')
        else:
            self.show_error(err)

    def analysisCallback(self, error_message):
        # Emitting this signal will call self.runResults on the main thread
        if error_message is None:
            self.analysis_callback_signal.emit()
        else:
            self.error_signal.emit(error_message)

    def runResults(self):
        """Runs server methods that generate safety metric results and visualizations"""
        identifier = get_identifier()
        results_dir = os.path.join(get_project_path(), 'results')
        ttc_threshold = self.ui.timeToCollisionLineEdit.text()
        vehicle_only = self.ui.vehiclesOnlyCheckBox.isChecked()
        speed_limit = self.ui.speedLimitLineEdit.text()
        success, err = api.results(identifier, results_dir, ttc_threshold, vehicle_only, speed_limit)

        if success:
            StatusPoller(identifier, 'highlight_video', 15, self.resultsCallback).start()
            self.show_message('Creating a safety report now. This will take around five minutes.\n\nPlease keep the application open during this. If you close the application, your results will not be automatically downloaded')
        else:
            self.show_error(err)

    def resultsCallback(self, error_message):
        # Emitting this signal will call self.runResults on the main thread
        if error_message is None:
            self.results_callback_signal.emit()
        else:
            self.error_signal.emit(error_message)

    def retrieveResults(self):
        results_dir = os.path.join(get_project_path(), 'results')
        success, err = api.retrieveResults(get_identifier(), results_dir)

        if not success:
            self.show_error(err)
            return

        with zipfile.ZipFile(os.path.join(results_dir, "results.zip"), "r") as zip_file:
            zip_file.extractall(results_dir)

        self.show_message('Results have been retrieved! This program will now open the folder containing the results.')

        # Open the file location
        if sys.platform == 'darwin':
            subprocess.Popen(['open', '--', results_dir])
        elif sys.platform == 'linux2':
            subprocess.Popen(['xdg-open', results_dir])
        elif sys.platform == 'win32':
            subprocess.Popen(['explorer', results_dir])


################################################################################################

    def show_next_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        new_i = curr_i + 1
        self.ui.main_tab_widget.setCurrentIndex(new_i)

    def show_prev_tab(self):
        curr_i = self.ui.main_tab_widget.currentIndex()
        self.ui.main_tab_widget.setCurrentIndex(curr_i - 1)

    def do_on_click(self, *methods):
        for method in methods:
            method()

    def show_error(self, error):
        self.show_message(error, error=True)

    def show_message(self, message, error=False):
        title = None
        if error:
            title = "Error"
        helper = message_helper.MessageHelper(self)
        helper.show_message(message, title=title)

    def open_project(self):
        fname = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Open Existing Project Folder...", get_default_project_dir()))
        fname = replace_path_delimiters(fname)
        # TODO: Instead of select folder, perhaps select config file?
        if fname:
            pm.load_project(fname, self)
        else:
            pass  # If no folder selected, don't load anything.

    def open_feedback(self):
        url = QtCore.QUrl('https://docs.google.com/forms/d/e/1FAIpQLSeTRwZlMUwNrbv9Nw-BddsOBGrCQjR5YXHbloPirRzB3-QoFA/viewform')
        if not QtWidgets.QDesktopServices.openUrl(url):
            QtWidgets.QMessageBox.warning(self, 'Connecting to Feedback', 'Could not open feedback form')

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
        fname = QtWidgets.QFileDialog.getOpenFileName(self, dialog_text, default_folder)  # TODO: Filter to show only image files
        if fname:
            image = QtGui.QImage(fname[0])
        else:
            image = None
        return image

    def homography_compute(self):
        #TODO: display error message if points are < 4
        px_text = self.ui.unit_px_input.text()
        self.unitPixRatio = float(unicode(px_text))

        homography_path = os.path.join(get_project_path(), "homography")

        self.unscaled_world_pts = (np.array(self.ui.homography_aerialview.list_points()))
        self.worldPts = self.unitPixRatio * self.unscaled_world_pts
        self.videoPts = np.array(self.ui.homography_cameraview.list_points())

        if len(self.worldPts) != len(self.videoPts):
            self.show_error('To compute the homography, please make sure you choose the same number of points on each image.')
            return
        elif len(self.worldPts) < 4:
            self.show_error('To compute the homography, please choose at least 4 points on each image.')
            return

        update_config_with_sections(get_config_path(), "homography", "unitpixelratio", str(self.unitPixRatio))
        homography_path = os.path.join(get_project_path(), "homography")

        # Finally, upload to server
        success, err = api.configHomography(\
            get_identifier(),\
            self.unitPixRatio,\
            self.ui.homography_aerialview.list_points(),\
            self.ui.homography_cameraview.list_points())

        if not success:
            self.show_error(err)
            return

        # Finally, upload to server
        success, err = api.configHomography(\
            get_identifier(),\
            self.unitPixRatio,\
            self.ui.homography_aerialview.list_points(),\
            self.ui.homography_cameraview.list_points())

        if not success:
            self.show_error(err)

        success, err, homography = api.getHomography(\
            get_identifier(),\
            homography_path)

        if not success:
            self.show_error(err)

        self.homography = np.array(homography)

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
        blue = (213,94,0)
        red = (0,114,178)
        white = (255,255,255)
        black = (0,0,0)
        radius = 12
        thickness = 6

        homography_path = os.path.join(get_project_path(), "homography")
        worldImg = Image.open(os.path.join(homography_path, "aerial.png"))
        videoImg = Image.open(os.path.join(homography_path, "camera.png"))

        invHomography = np.linalg.inv(self.homography)

        projectedWorldPts = projectArray(invHomography, self.worldPts.T).T
        projectedVideoPts = projectArray(self.homography, self.videoPts.T).T

        # TODO: Nicer formatting for computed goodness images
        for i in range(self.worldPts.shape[0]):
            # world image
            worldDraw = ImageDraw.Draw(worldImg)

            x, y = tuple(np.int32(np.round(self.worldPts[i] / self.unitPixRatio)))
            draw_circle(worldDraw, x, y, blue, radius, thickness=thickness)

            x, y = tuple(np.int32(np.round(projectedVideoPts[i] / self.unitPixRatio)))
            draw_circle(worldDraw, x, y, red, radius, thickness=thickness)

            x, y = tuple(np.int32(np.round(self.worldPts[i]/self.unitPixRatio)) + 5)
            draw_text(worldDraw, str(i+1), x, y, white, border_color=black, border_thickness=2, font_size=48)

            # video image
            videoDraw = ImageDraw.Draw(videoImg)

            x, y = tuple(np.int32(np.round(self.videoPts[i])))
            draw_circle(videoDraw, x, y, blue, radius, thickness=thickness)

            x, y = tuple(np.int32(np.round(projectedWorldPts[i])))
            draw_circle(videoDraw, x, y, red, radius, thickness=thickness)

            x, y = tuple(np.int32(np.round(self.videoPts[i]) + 5))
            draw_text(videoDraw, str(i+1), x, y, white, border_color=white, border_thickness=2, font_size=48)

        aerial_goodness_path = os.path.join(homography_path, "homography_goodness_aerial.png")
        camera_goodness_path = os.path.join(homography_path, "homography_goodness_camera.png")

        worldImg.save(aerial_goodness_path)  # Save aerial goodness image
        videoImg.save(camera_goodness_path)  # Save camera goodness image

        self.ui.homography_results.load_image(QtGui.QImage(aerial_goodness_path))  # Load aerial goodness image into gui

##########################################################################################################################

class configGuiWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        """ parent is an instance of MainGUI """
        super(configGuiWidget, self).__init__()
        self.parent = parent

    def gridRowHelper(self, label_txt, info_txt=None):
        """Helper to construct the widgets that make up the config UI
        grid rows.
        Returns (label, info, line_edit) elements.
        """
        label = QtWidgets.QLabel(label_txt)
        if info_txt:
            info = QtWidgets.QToolButton()
            info.setIcon(qta.icon('fa.question'))
            info.clicked.connect(lambda: self.parent.show_message(info_txt))
        else:
            info = None
        line_edit = QtWidgets.QLineEdit()
        return label, info, line_edit

class configGui_features(configGuiWidget):

    def __init__(self, parent):
        """ parent is an instance of MainGUI """
        super(configGui_features, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.label1, _, self.input1 = self.gridRowHelper("first frame to process")

        self.label2, _, self.input2 = self.gridRowHelper("number of frames to process")

        self.label3, self.info3, self.input3 = self.gridRowHelper("Max number of features added at each frame",
                "The maximum number of features added at each frame. Recommended range: 1000+. Note if that there are many moving objects in each frame, and those objects take up a large portion of the frame, this number may be higher. If you find that not enough features are being tracked, increase this parameter.")

        self.label4 = QtWidgets.QLabel("Number of deplacement to test")
        self.label5, self.info5, self.input5 = self.gridRowHelper("minimum feature motion",
                "Number of displacement to test minimum feature motion. Recommended range: 2 - 15. Determines how long features will be tracked. Increase this parameter if you find that your features are disappearing very quickly (i.e., after a few frames)")

        self.label6, self.info6, self.input6 = self.gridRowHelper("Minimum displacement to keep features (px)",
                "Minimum displacement to keep features. Recommended range: 0.0001 -  0.1. Describes the minimum required displacement to keep a feature (in pixels). If you have lots of slow-moving (or far-away) objects in your video, and find that not enough features are being tracked, decrease this parameter. On the other hand, if too many non-road- user features are being tracked (i.e., trees swaying in the wind) it may be useful to increase this parameter to capture the faster-moving features, which are more likely to belong to road users.")

        self.label7 = QtWidgets.QLabel("Max number of iterations")

        self.label8, self.info8, self.input8 = self.gridRowHelper("to stop feature tracking",
                "Max number of iterations to stop feature tracking. Recommended range: 10 - 1000. Changes how long after a feature continues to persist after the feature stops moving. If your video features many slow-moving objects, or objects that start and stop frequently, you may want to increase this parameter.")

        self.label9 = QtWidgets.QLabel("Minimum number of frames to consider")

        self.label10, self.info10, self.input10 = self.gridRowHelper("a feature for grouping",
                "Minimum number of frames to consider a feature for grouping. Recommended range: 10 - 25. The minimum amount of time (in video frames) for which a feature must persist before it is considered in the next steps of the tracking process. You may want to keep this parameter value fairly high to filter out some of the shorter-lived features (which often belong to non-road-user objects, such as moving plants in the video).")

        self.loadConfig_features()

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.label1, 2, 0)
        grid.addWidget(self.input1, 2, 2)

        grid.addWidget(self.label2, 3, 0)
        grid.addWidget(self.input2, 3, 2)

        grid.addWidget(self.label3, 4, 0)
        grid.addWidget(self.info3, 4, 1)
        grid.addWidget(self.input3, 4, 2)

        grid.addWidget(self.label4, 5, 0)

        grid.addWidget(self.label5, 6, 0)
        grid.addWidget(self.info5, 6, 1)
        grid.addWidget(self.input5, 6, 2)

        grid.addWidget(self.label6, 7, 0)
        grid.addWidget(self.info6, 7, 1)
        grid.addWidget(self.input6, 7, 2)

        grid.addWidget(self.label7, 8, 0)

        grid.addWidget(self.label8, 9, 0)
        grid.addWidget(self.info8, 9, 1)
        grid.addWidget(self.input8, 9, 2)

        grid.addWidget(self.label9, 10, 0)

        grid.addWidget(self.label10, 11, 0)
        grid.addWidget(self.info10, 11, 1)
        grid.addWidget(self.input10, 11, 2)

        self.setLayout(grid)

        self.setWindowTitle('Input config')

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


        success, err = api.configFiles(get_identifier(),\
                     max_features_per_frame = max_features_per_frame,\
                     num_displacement_frames = num_displacement_frames,\
                     min_feature_displacement = min_feature_displacement,\
                     max_iterations_to_persist = max_iterations_to_persist,\
                     min_feature_frames = min_feature_frames)

        if not success:
            self.show_error(err)

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

class configGui_object(configGuiWidget):

    def __init__(self, parent):
        """ parent is an instance of MainGUI """
        super(configGui_object, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.label1, _, self.input1 = self.gridRowHelper("first frame to process")
        self.label2, _, self.input2 = self.gridRowHelper("number of frames to process")
        self.label3, self.info3, self.input3 = self.gridRowHelper("Max Connection Distance",
            "Maximum connection distance for feature-grouping. Connection-distance is a threshold; it is the maximum world distance at which two features can be connected to the same object. Note that in this example, this does not mean that the maximum size of an object is 1 meter! Rather, this means that a feature greater than 1 meter away from this object cannot be considered a part of this object.")

        self.label4, self.info4, self.input4 = self.gridRowHelper("Max Segmentation Distance",
            "Maximum segmentation distance. Segmentation-distance is a threshold; it is the maximum world distance at which two features that are moving relative to each other can be connected to the same object. Again, note that this does not relate to the maximum size of an object! Rather, this means that two features that are moving at different speeds cannot be connected to the same object if they are more than 0.7 meters away from each other.")

        self.loadConfig_objects()

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.label1, 2, 0)
        grid.addWidget(self.input1, 2, 2)

        grid.addWidget(self.label2, 3, 0)
        grid.addWidget(self.input2, 3, 2)

        grid.addWidget(self.label3, 4, 0)
        grid.addWidget(self.info3, 4, 1)
        grid.addWidget(self.input3, 4, 2)

        grid.addWidget(self.label4, 5, 0)
        grid.addWidget(self.info4, 5, 1)
        grid.addWidget(self.input4, 5, 2)

        self.setLayout(grid)

        self.setWindowTitle('Input config')

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

        success, err = api.configFiles(get_identifier(),\
                     max_connection_distance = max_connection_distance,\
                     max_segmentation_distance = max_segmentation_distance)

        if not success:
            self.show_error(err)

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
def projectArray(homography, points):
    '''Returns the coordinates of the projected points through homography
    (format: array 2xN points)
    '''
    if points.shape[0] != 2:
        raise Exception('points of dimension {0} {1}'.format(points.shape[0], points.shape[1]))

    if (homography is not None) and homography.size>0:
        augmentedPoints = np.append(points,[[1]*points.shape[1]], 0)
        prod = np.dot(homography, augmentedPoints)
        return prod[0:2]/prod[2]
    else:
        return points

##########################################################################################################################
def main():
    app.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(main())
