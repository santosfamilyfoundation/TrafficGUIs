from PyQt4 import QtGui, QtCore
from new_project import Ui_create_new_project
import os

class ProjectWizard(QtGui.QWizard):

    def __init__(self, parent):
        super(ProjectWizard, self).__init__(parent)
        self.ui = Ui_create_new_project()
        self.ui.setupUi(self)
        self.ui.newp_aerial_image_browse.clicked.connect(self.open_aerial_image)
        self.ui.newp_video_browse.clicked.connect(self.open_video)

        self.aerial_image_selected = False
        self.video_selected = False

        self.DEFAULT_PROJECT_DIR = os.path.join(os.getcwd(), os.pardir, "project_dir")

    def open_aerial_image(self):
        filt = "Images (*.png *.jpg *.jpeg *.bmp *.tif *.gif)"  # Select only images
        # default_dir = 
        fname = self.open_fd(dialog_text="Select aerial image", file_filter=filt)
        if fname:
            self.ui.newp_aerial_image_input.setText(fname)
            self.aerial_image_selected = True
        else:
            self.ui.newp_aerial_image_input.setText("NO FILE SELECTED")

    def open_video(self):
        filt = "Videos (*.mp4 *.avi *.mpg *mpeg)"  # Select only videos
        # default_dir = 
        fname = self.open_fd(dialog_text="Select video for analysis", file_filter=filt)
        if fname:
            self.ui.newp_video_input.setText(fname)
            self.video_selected = True
        else:
            self.ui.newp_video_input.setText("NO VIDEO SELECTED")

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
            str: Filename selected.
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, dialog_text, default_dir, file_filter)  # TODO: Filter to show only image files
        return fname
