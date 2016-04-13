"""
Project management classes and functions
"""

from PyQt4 import QtGui, QtCore
from new_project import Ui_create_new_project
import os
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import time
import datetime
from shutil import copy
import cv2
import Image

from app_config import AppConfig as ac


class ProjectWizard(QtGui.QWizard):

    def __init__(self, parent):
        super(ProjectWizard, self).__init__(parent)
        self.ui = Ui_create_new_project()
        self.ui.setupUi(self)
        self.ui.newp_aerial_image_browse.clicked.connect(self.open_aerial_image)
        self.ui.newp_video_browse.clicked.connect(self.open_video)
        self.aerial_image_selected = False
        self.video_selected = False

        # self.DEFAULT_PROJECT_DIR = os.path.join(os.getcwd(), os.pardir, "project_dir")
        self.DEFAULT_PROJECT_DIR = ac.PROJECT_DIR

        self.ui.newp_start_creation.clicked.connect(self.start_create_project)
        self.config_parser = SafeConfigParser()

        self.creating_project = False

        self.ui.newp_p1.registerField("project_name*", self.ui.newp_projectname_input)

        self.ui.newp_p2.registerField("video_path*", self.ui.newp_video_input)
        self.ui.newp_p2.registerField("video_start_datetime", self.ui.newp_video_start_time_input)
        self.ui.newp_p2.registerField("video_fps*", self.ui.newp_video_fps_input)

        self.ui.newp_p2.registerField("aerial_image*", self.ui.newp_aerial_image_input)

        self.ui.newp_p3.registerField("create_project", self.ui.newp_start_creation)

    def open_aerial_image(self):
        filt = "Images (*.png *.jpg *.jpeg *.bmp *.tif *.gif)"  # Select only images
        # default_dir =
        fname = self.open_fd(dialog_text="Select aerial image", file_filter=filt)
        if fname:
            self.ui.newp_aerial_image_input.setText(fname)
            self.aerial_image_selected = True
            self.aerialpath = fname
        else:
            self.ui.newp_aerial_image_input.setText("NO FILE SELECTED")

    def open_video(self):
        filt = "Videos (*.mp4 *.avi *.mpg *mpeg)"  # Select only videos
        # default_dir =
        fname = self.open_fd(dialog_text="Select video for analysis", file_filter=filt)
        if fname:
            self.ui.newp_video_input.setText(fname)
            self.video_selected = True
            self.videopath = fname
        else:
            self.ui.newp_video_input.setText("NO VIDEO SELECTED")

    # def move_video
    def open_fd(self, dialog_text="Open", file_filter="", default_dir=""):
        """Opens a file dialog, allowing user to select a file.

        Returns the selected filename. If the user presses cancel, this returns
        a null string ("").

        Args:
            dialog_text [Optional(str.)]: Text to prompt user with in open file
                dialog. Defaults to "Open".
            file_filter [Optional(str.)]: String used to filter selectable file
                types. Defaults to "".
            default_dir [Optional(str.)]: Path of the default directory to open
                the file dialog box to. Defaults to "".

        Returns:
            str: Filename selected. Null string ("") if no file selected.
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, dialog_text, default_dir, file_filter)  # TODO: Filter to show only image files
        return str(fname)

    def start_create_project(self):
        if not self.creating_project:
            self.creating_project = True
            self.create_project_dir()

    def create_project_dir(self):
        self.project_name = str(self.ui.newp_projectname_input.text())
        progress_bar = self.ui.newp_creation_progress
        progress_msg = self.ui.newp_creation_status
        directory_names = ["homography", ".temp", "run", "results"]
        pr_path = os.path.join(self.DEFAULT_PROJECT_DIR, self.project_name)
        if not os.path.exists(pr_path):
            self.PROJECT_PATH = pr_path
            progress_msg.setText("Creating project directories...")
            for new_dir in directory_names:
                progress_bar.setValue(progress_bar.value() + 5)
                os.makedirs(os.path.join(pr_path, new_dir))

            progress_bar.setValue(progress_bar.value() + 5)
            progress_msg.setText("Writing configuration files...")
            self._write_to_project_config()
            copy("default/tracking.cfg", os.path.join(pr_path, "tracking.cfg"))

            progress_msg.setText("Copying object classification files...")
            svms = ["modelBV.xml", "modelPB.xml", "modelPBV.xml", "modelPV.xml"]
            for svm in svms:
                copy("default/{}".format(svm), os.path.join(pr_path, svm))
                progress_bar.setValue(progress_bar.value() + 5)

            progress_msg.setText("Copying video file...")
            video_dest = os.path.join(pr_path, os.path.basename(self.videopath))
            copy(self.videopath, video_dest)
            progress_bar.setValue(80)

            progress_msg.setText("Extracting camera image...")
            vidcap = cv2.VideoCapture(video_dest)
            vidcap.set(cv2.cv.CV_CAP_PROP_FRAME_COUNT, 1000)
            success, image = vidcap.read()
            progress_bar.setValue(85)
            if success:
                cv2.imwrite(os.path.join(pr_path, "homography", "camera.png"), image)
            else:
                print("ERR: No camera image extracted.")
            progress_bar.setValue(90)

            progress_msg.setText("Copying aerial image...")
            im = Image.open(self.aerialpath)
            aerial_dest = os.path.join(pr_path, "homography", "aerial.png")
            im.save(aerial_dest)
            progress_bar.setValue(100)
            progress_msg.setText("Complete.")

        else:
            print("Project exists. No new project created.")

    def _write_to_project_config(self):
        ts = time.time()
        vid_ts = self.ui.newp_video_start_time_input.dateTime().toPyDateTime()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S %Z')
        video_timestamp = vid_ts.strftime('%d-%m-%Y %H:%M:%S %Z')
        self.config_parser.add_section("info")
        self.config_parser.set("info", "project_name", self.project_name)
        self.config_parser.set("info", "creation_date", timestamp)
        self.config_parser.add_section("video")
        self.config_parser.set("video", "path", self.videopath)
        self.config_parser.set("video", "framerate", str(self.ui.newp_video_fps_input.text()))
        self.config_parser.set("video", "start", video_timestamp)

        with open(os.path.join(self.PROJECT_PATH, "{}.cfg".format(self.project_name)), 'wb') as configfile:
            self.config_parser.write(configfile)


def load_project(folder_path, main_window):
    path = os.path.normpath(folder_path)  # Clean path. May not be necessary.
    project_name = os.path.basename(path)
    project_cfg = os.path.join(path, "{}.cfg".format(project_name))
    ac.CURRENT_PROJECT_PATH = path  # Set application-level variables indicating the currently open project
    ac.CURRENT_PROJECT_NAME = project_name
    ac.CURRENT_PROJECT_CONFIG = project_cfg

    config_parser = SafeConfigParser()
    config_parser.read(project_cfg)  # Read project config file.

    load_homography(main_window)
    load_feature_tracking(main_window)
    load_roadusers_tracking(main_window)


def load_homography(main_window):
    """
    Loads homography information into the specified main window.
    """
    path = ac.CURRENT_PROJECT_PATH
    aerial_path = os.path.join(path, "homography", "aerial.png")
    camera_path = os.path.join(path, "homography", "camera.png")
    # TODO: Handle if above two paths do not exist

    gui = main_window.ui
    # Load images
    gui.homography_aerialview.load_image_from_path(aerial_path)
    gui.homography_cameraview.load_image_from_path(camera_path)

    # Has a homography been previously computed?


def load_feature_tracking(main_window):
    video_path_exists, video_path = check_project_cfg_option("video", "path")
    if video_path_exists:
        if os.path.exists(video_path):
            main_window.feature_tracking_video_player.loadVideo(video_path)
        else:
            # Path specified in config file no longer exists
            print("ERR: Video not found at \"{}\".".format(video_path))
    else:
        # No video specified in project config file
        print("ERR: No video specified in project configuration file. Invalid project.")


def load_roadusers_tracking(main_window):
    video_path_exists, video_path = check_project_cfg_option("video", "path")
    if video_path_exists:
        if os.path.exists(video_path):
            main_window.roadusers_tracking_video_player.loadVideo(video_path)
        else:
            # Path specified in config file no longer exists
            print("ERR: Video not found at \"{}\".".format(video_path))
    else:
        # No video specified in project config file
        print("ERR: No video specified in project configuration file. Invalid project.")


def update_project_cfg(section, option, value):
    """
    Updates a single value in the current open project's configuration file.
    Writes nothing and returns -1 if no project currently open.

    Args:
        section (str): Name of the section to write new option-value pair to write.
        option (str): Name of the option to write/update.
        value (str): Value to write/update assocaited with the specified option.
    """
    cfp = SafeConfigParser()
    cfp.read(ac.CURRENT_PROJECT_CONFIG)
    cfp.set(section, option, value)
    with open(ac.CURRENT_PROJECT_CONFIG, "wb") as cfg_file:
        cfp.write(cfg_file)


def check_project_cfg_option(section, option):
    """
    Checks the currently open project's configuration file for the specified option
    in the specified section. If it exists, this returns (True, <value>). If it does not
    exist, this returns (False, None).

    Args:
        section (str): Name of the section to check for option.
        option (str): Name of the option check/return.
    """
    cfp = SafeConfigParser()
    cfp.read(ac.CURRENT_PROJECT_CONFIG)
    try:
        value = cfp.get(section, option)
    except NoSectionError:
        print("ERR [check_project_cfg_option()]: Section {} is not available in {}.".format(section, ac.CURRENT_PROJECT_CONFIG))
        return (False, None)
    except NoOptionError:
        print("Option {} is not available in {}.".format(option, ac.CURRENT_PROJECT_CONFIG))
        return (False, None)
    else:
        return (True, value)


def check_project_cfg_section(section):
    """
    Checks the currently open project's configuration file for the section. If it exists,
    this returns True. If it does not exist, this returns False.

    Args:
        section (str): Name of the section to check existance of.
    """
    cfp = SafeConfigParser()
    cfp.read(ac.CURRENT_PROJECT_CONFIG)
    if section in cfp.sections():  # If the given section exists,
        return True                # then return True.
    else:                          # Otherwise,
        return False               # then return False
