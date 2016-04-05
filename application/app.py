#!/usr/bin/env python
import sys
from PyQt4 import QtGui, QtCore
from safety_main import Ui_TransportationSafety

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import random



from plotting import visualization

class Organizer(object):
    def __init__(self):
        super(Organizer, self).__init__()


class DisplayImage(object):
    def __init__(self, image, pixmap):
        self._image = None
        self.image = image
        self.pixmap = pixmap
        self.scale_factor = 0  # If 512x512 img and 256x256 pixmap, this is 0.5
        self.compute_scale_factor()

    # @property
    # def image(self):
    #     return self._image

    # @image.setter
    # def image(self, new_image):
    #     try:
    #         self.image_size = (new_image.height(), new_image.width())
    #     except TypeError, e:
    #         print("ERR: Invalid image passed to DisplayImage. Must be QImage.")
    #     else:
    #         self._image = image

    # @image.deleter
    # def image(self):
    #     self._image = None
    #     self.image_size = (None, None)

    def compute_scale_factor(self):
        pix_width = float(self.pixmap.width())
        pix_height = float(self.pixmap.height())
        img_width = float(self.image.width())
        img_height = float(self.image.height())
        print(img_width / pix_width)
        print(img_height / pix_height)
        self.scale_factor = img_width / pix_width

    def tf_pixmap_to_image(self, x_coord, y_coord):
        """
        MapsTransforms pixmap coordinates to unscaled image coordinates. Rounds
        to nearest integer value using Python's built-in round() function.

        EX: If scale_factor = 0.5 and input (44, 21), returns (88, 42)
        """
        sf = float(self.scale_factor)
        x_scaled = round(x_coord / sf)
        y_scaled = round(y_coord / sf)
        return x_scaled, y_scaled

    def tf_image_to_pixmap(self, x_coord, y_coord):
        """
        Transforms image coordinates to scaled pixmap coordinates.

        EX: If scale_factor = 0.5 and input (44, 21), returns (22, 11)
        """
        x_scaled = round(x_coord * self.scale_factor)
        y_scaled = round(y_coord * self.scale_factor)
        return x_scaled, y_scaled


class MainGUI(QtGui.QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.ui = Ui_TransportationSafety()
        self.ui.setupUi(self)

        # Experimenting with organizational objects
        self.homography = Organizer()
        self.feature_tracking = Organizer()
        self.results = Organizer()
        # self.this

        # Connect Menu actions
        self.ui.actionOpen_Project.triggered.connect(self.open_project)
        # self.ui.actionLoad_Image.triggered.connect(self.open_image)
        self.ui.actionAdd_Replace_Aerial_Image.triggered.connect(self.homography_open_image_aerial)
        self.ui.actionAdd_Replace_Aerial_Image.triggered.connect(self.homography_open_image_camera)
        self.ui.main_tab_widget.setCurrentIndex(0)  # Start on the first tab

        # Connect button actions
        self.ui.homography_button_open_aerial_image.clicked.connect(self.homography_open_image_aerial)  # TODO: New method. Check which tab is open. Move to homography tab if not already there. Then call open_image_aerial.
        self.ui.homography_button_open_camera_image.clicked.connect(self.homography_open_image_camera)

        # Connect back + continue buttons
        self.ui.homography_continue_button.clicked.connect(self.show_next_tab)
        self.ui.feature_tracking_continue_button.clicked.connect(self.show_next_tab)
        self.ui.feature_tracking_back_button.clicked.connect(self.show_prev_tab)

        # Results plotting
        # self.figure1 = Figure()
        # self.canvas1 = FigureCanvas(self.figure1)
        # self.ui.results_plot_layout1.addWidget(self.canvas1)
        # self.results_plot_plot1()
        aplot = visualization.road_user_traj('stmarc.sqlite', 30, 'homography.txt', 'stmarc_image.png')
        aplot.add_to_widget(self.ui.results_plot_layout1)
        aplot.show()

        # self.figure2 = Figure()
        # self.canvas2 = FigureCanvas(self.figure2)
        # self.ui.results_plot_layout2.addWidget(self.canvas2)
        # self.results_plot_plot2()
        # self.ui.track_image.mousePressEvent = self.get_image_position
        
        ## CONFIGURE HOMOGRAPHY ##
        self.ui.homography_hslider_zoom_camera_image.zoom_target = self.ui.homography_cameraview

        self.show()

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
        fname = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Project', '/home')
        print(fname)

    def homography_open_image_camera(self):
        """Opens a file dialog, allowing user to select an camera image file.

        Creates a QImage object and QPixmap from the filename of an camera image
        selected by the user in a popup file dialog menu.
        """
        qi = self.open_image_fd(dialog_text="Select camera image...")
        self.ui.homography_cameraview.load_image(qi)
        # Do other stuff
        # self.homography_show_image('aerial'), etc. ?

    def homography_open_image_aerial(self):
        """Opens a file dialog, allowing user to select an aerial image file.

        Creates a QImage object and QPixmap from the filename of an aerial image
        selected by the user in a popup file dialog menu.
        """
        qi = self.open_image_fd(dialog_text="Select aerial image...")
        self.homography.image_aerial = qi
        self.homography.pixmap_aerial = QtGui.QPixmap.fromImage(qi)
        self.homography.aerial_image_label.setPixmap(self.homography.pixmap_aerial)
        # Do other stuff
        # self.homography_show_image('aerial'), etc. ?

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
        """
        fname = QtGui.QFileDialog.getOpenFileName(self, dialog_text, default_dir)  # TODO: Filter to show only image files
        image = QtGui.QImage(fname)
        return image

    # def open_image(self):
    #     fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Project', '')
    #     print(fname)
    #     tracking_image = QtGui.QImage(fname)
    #     pixmap = QtGui.QPixmap.fromImage(tracking_image)
    #     pixmap = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio)
    #     self._tracking_image = DisplayImage(tracking_image, pixmap)
    #     self.ui.track_image.setPixmap(pixmap)

    def get_image_position(self, event):
        print(event.pos())
        print(self._tracking_image.image.pixel(event.x(), event.y()))


def main():
    app.exec_()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainGUI()
    # print(dir(ex.ui))  # Uncomment to show structure of ui object
    sys.exit(main())
