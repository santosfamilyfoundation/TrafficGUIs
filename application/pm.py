"""
Project management classes and functions
"""

from PyQt5 import QtWidgets, QtCore
from views.new_project import Ui_create_new_project
import os
import re
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import time
import datetime
from shutil import copy
import cv2
try:
    from PIL import Image
except:
    import Image
import numpy as np

from app_config import AppConfig as ac
from app_config import get_default_project_dir, get_project_path, get_config_path, config_section_exists, get_config_with_sections, update_config_with_sections
from cloud_api import api

class ProjectWizard(QtWidgets.QWizard):

    def __init__(self, parent):
        super(ProjectWizard, self).__init__(parent)
        self.ui = Ui_create_new_project()
        self.ui.setupUi(self)
        self.ui.newp_aerial_image_browse.clicked.connect(self.open_aerial_image)
        self.ui.newp_video_browse.clicked.connect(self.open_video)
        self.aerial_image_selected = False
        self.video_selected = False

        # Remove '?' icon
        flags = self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(flags)

        self.ui.newp_start_creation.clicked.connect(self.start_create_project)
        self.config_parser = SafeConfigParser()

        self.creating_project = False

        self.ui.newp_p1.registerField("project_name*", self.ui.newp_projectname_input)

        self.ui.newp_p2.registerField("video_path*", self.ui.newp_video_input)
        self.ui.newp_p2.registerField("video_start_datetime", self.ui.newp_video_start_time_input)
        self.ui.newp_p2.registerField("video_server_input*", self.ui.newp_video_server_input)
        self.ui.newp_p2.registerField("video_email", self.ui.newp_video_email_input)

        # Set default server
        self.ui.newp_video_server_input.setText("http://localhost:8088")

        self.ui.newp_p2_5.registerField("aerial_image*", self.ui.newp_aerial_image_input)
        self.ui.newp_p3.registerField("create_project", self.ui.newp_start_creation)

    def open_aerial_image(self):
        filt = "Images (*.png *.jpg *.jpeg *.bmp *.tif *.gif)"  # Select only images
        documents_folder = os.path.realpath(os.path.join(os.path.expanduser('~'), "Documents"))
        fname = self.open_fd(dialog_text="Select aerial image", file_filter=filt, default_dir=documents_folder)
        if fname:
            filepath = self.get_filepath(fname)
            self.ui.newp_aerial_image_input.setText(filepath)
            self.aerialpath = filepath
            self.aerial_image_selected = True
        else:
            self.ui.newp_aerial_image_input.setText("NO FILE SELECTED")

    def open_video(self):
        filt = "Videos (*.mp4 *.avi *.mpg *.mpeg *.mov *.ogg *.wmv *.m4v *.m4p *.mp2 *.mpe *.mpv *.m2v)"  # Select only videos
        documents_folder = os.path.realpath(os.path.join(os.path.expanduser('~'), "Documents"))
        fname = self.open_fd(dialog_text="Select video for analysis", file_filter=filt, default_dir=documents_folder)
        if fname:
            filepath = self.get_filepath(fname)
            self.ui.newp_video_input.setText(filepath)
            self.video_selected = True
            self.videopath = filepath
        else:
            self.ui.newp_video_input.setText("NO VIDEO SELECTED")

    def get_filepath(self, filepath):
        """Cleans the filepath to only include the path, not file options.

        Returns the selected filepath only, found between the ''.

        Args:
            filepath: uncleaned filename and file types.

        Returns:
            str: Cleaned string of only the location of video/image file.
        """
        return re.findall(r"'(.*?)'", filepath, re.DOTALL)[0]


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
        fname = QtWidgets.QFileDialog.getOpenFileName(self, dialog_text, default_dir, file_filter)  # TODO: Filter to show only image files
        return str(fname)

    def start_create_project(self):
        if not self.creating_project:
            self.creating_project = True
            self.create_project_dir()

    def create_project_dir(self):
        project_name = str(self.ui.newp_projectname_input.text())
        ac.CURRENT_PROJECT_PATH = os.path.join(get_default_project_dir(), project_name)
        progress_bar = self.ui.newp_creation_progress
        progress_bar.setHidden(False)
        progress_msg = self.ui.newp_creation_status
        progress_msg.setHidden(False)
        creation_button = self.ui.newp_start_creation
        creation_button.setHidden(True)
        directory_names = ["homography", "results"]
        pr_path = get_project_path()
        if not os.path.exists(pr_path):
            # Set URL to use before doing anything
            server = str(self.ui.newp_video_server_input.text())
            update_api(server)

            progress_msg.setText("Creating project directories...")
            progress_bar.show()
            for new_dir in directory_names:
                progress_bar.setValue(progress_bar.value() + 5)
                os.makedirs(os.path.join(pr_path, new_dir))

            progress_bar.setValue(progress_bar.value() + 5)
            progress_msg.setText("Writing configuration files...")
            self._write_to_project_config()

            progress_msg.setText("Copying video file...")
            video_extension = self.videopath.split('.')[-1]
            video_dest = os.path.join(pr_path, 'video.' + video_extension)
            copy(self.videopath, video_dest)

            progress_msg.setText("Uploading video file...")
            try:
                identifier = api.uploadVideo(self.videopath)
                update_config_with_sections(get_config_path(), 'info', 'identifier', identifier)
            except Exception as e:
                print("Failed to upload the Video")
                print(str(e))
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
            progress_bar.setValue(95)
            progress_msg.setText("Complete.")

            progress_msg.setText("Opening {} project...".format(project_name))
            self.load_new_project()
            progress_bar.setValue(100)
            progress_msg.setText("Complete.")

        else:
            print("Project exists. No new project created.")

    def _write_to_project_config(self):
        ts = time.time()
        vid_ts = self.ui.newp_video_start_time_input.dateTime().toPyDateTime()
        email = str(self.ui.newp_video_email_input.text())
        server = str(self.ui.newp_video_server_input.text())

        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S %Z')
        video_timestamp = vid_ts.strftime('%d-%m-%Y %H:%M:%S %Z')
        self.config_parser.add_section("info")
        self.config_parser.set("info", "project_name", os.path.basename(ac.CURRENT_PROJECT_PATH))
        self.config_parser.set("info", "creation_date", timestamp)
        self.config_parser.set("info", "server", server)
        self.config_parser.set("info", "email", email)
        self.config_parser.add_section("video")
        video_extension = self.videopath.split('.')[-1]
        self.config_parser.set("video", "name", 'video.'+video_extension)
        self.config_parser.set("video", "source", self.videopath)
        self.config_parser.set("video", "start", video_timestamp)

        self.config_parser.add_section("config")
        try:
            config = api.defaultConfig()
            for (key, value) in config.iteritems():
                self.config_parser.set("config", key, str(value))
        except Exception as e:
            print("Failed to get default configuration")
            print(str(e))

        with open(os.path.join(get_config_path()), 'wb') as configfile:
            self.config_parser.write(configfile)

    def load_new_project(self):
        load_project(ac.CURRENT_PROJECT_PATH, self.parent())

def load_project(project_path, main_window):
    ac.CURRENT_PROJECT_PATH = project_path

    load_homography(main_window)

    # Reload the URL for the project
    addr = get_config_with_sections(get_config_path(), "info", "server")
    update_api(addr)

    load_config(main_window)

def loadPointCorrespondences(filename):
    '''Loads and returns the corresponding points in world (first 2 lines) and image spaces (last 2 lines)'''
    points = np.loadtxt(filename, dtype=np.float32)
    return  (points[:2,:].T, points[2:,:].T) # (world points, image points)

def load_homography(main_window):
    """
    Loads homography information into the specified main window.
    """
    path = get_project_path()
    aerial_path = os.path.join(path, "homography", "aerial.png")
    camera_path = os.path.join(path, "homography", "camera.png")
    # TODO: Handle if above two paths do not exist
    load_from = 'image_pts'  # "image_pts" or "pt_corrs"
    gui = main_window.ui
    # Load images
    gui.homography_aerialview.load_image_from_path(aerial_path)
    gui.homography_cameraview.load_image_from_path(camera_path)

    goodness_path = os.path.join(path, "homography", "homography_goodness_aerial.png")
    image_pts_path = os.path.join(path, "homography", "image-points.txt")
    pt_corrs_path = os.path.join(path, "homography", "point-correspondences.txt")
    homo_path = os.path.join(path, "homography", "homography.txt")

    if load_from is "image_pts":
        corr_path = image_pts_path
    else:
        corr_path = pt_corrs_path

    # Has a homography been previously computed?
    if config_section_exists(get_config_path(), "homography"):  # If we can load homography unit-pix ratio load it
        # load unit-pixel ratio
        upr = get_config_with_sections(get_config_path(), "homography", "unitpixelratio")
        if upr:
            gui.unit_px_input.setText(upr)
    if os.path.exists(corr_path):  # If points have been previously selected
        worldPts, videoPts = loadPointCorrespondences(corr_path)
        main_window.homography = np.loadtxt(homo_path)
        if load_from is "image_pts":
            for point in worldPts:
                main_window.ui.homography_aerialview.scene().add_point(point)
        elif load_from is "pt_corrs":
            for point in worldPts:
                main_window.ui.homography_aerialview.scene().add_point(point/float(upr))
        else:
            print("ERR: Invalid point source {} specified. Points not loaded".format(load_from))
        for point in videoPts:
            main_window.ui.homography_cameraview.scene().add_point(point)
        gui.homography_results.load_image_from_path(goodness_path)
    else:
        print ("{} does not exist. No points loaded.".format(corr_path))

def update_api(addr):
    if addr:
        api.set_url(addr)
    else:
        print("No server, resorting to localhost")
        api.set_url('localhost')

def load_config(main_window):
    main_window.configGui_features.loadConfig_features()
    main_window.configGui_object.loadConfig_objects()
