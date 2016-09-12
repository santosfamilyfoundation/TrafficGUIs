from PyQt4 import QtGui, QtCore
import matplotlib
import os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# # from application_config import AppConfig as ac
# import application

from app_config import AppConfig as ac
from app_config import check_project_cfg_option
# from .. import pm 
# from .. import app_config
# ac = app_config.AppConfig
from plotting import visualization
import random


class QTPLT(object):
    """Matplotlib"""
    def __init__(self):
        super(QTPLT, self).__init__()
        self.fig = Figure()  # figsize=(5, 4))
        self._canvas = FigureCanvas(self.fig)

    def add_to_widget(self, widget):
        """
        Adds the figure's canvas to a QT widget (QWidget).
        """
        widget.addWidget(self._canvas)

    def show(self):
        """
        Refreshes figure by drawing it to its canvas embedded in a widget.
        Call this after updating the figure (e.g., ax.plot(...)).
        """
        self._canvas.draw()


def example():
    a_plot = QTPLT()
    a_plot.add_to_widget(somewidget)
    ax = a_plot.fig.add_subplot(111)
    data = [random.random() for i in range(10)]
    # discards the old graph
    ax.hold(False)
    # plot data
    ax.plot(data, '*-')
    a_plot.show()


class MatplotlibWidget(QtGui.QWidget):
    """
    Implements a Matplotlib figure inside a QWidget.
    Use getFigure() and draw() to interact with matplotlib.

    Example::

        mw = MatplotlibWidget()
        subplot = mw.getFigure().add_subplot(111)
        subplot.plot(x,y)
        mw.draw()
    """
    def __init__(self, parent, size=(5.0, 4.0), dpi=100):
        super(MatplotlibWidget, self).__init__(parent)
        self.fig = Figure(size, dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.toolbar)
        self.vbox.addWidget(self.canvas)

        self.setLayout(self.vbox)

    def getFigure(self):
        return self.fig

    def draw(self):
        self.canvas.draw()


def plot_results(main_window):
    if ac.CURRENT_PROJECT_PATH:
        database_filename = os.path.join(ac.CURRENT_PROJECT_PATH, "run", "results.sqlite")
        homography_filename = os.path.join(ac.CURRENT_PROJECT_PATH, "homography", "homography.txt")
        camera_image = os.path.join(ac.CURRENT_PROJECT_PATH, "homography", "camera.png")
        fps_exists, video_fps = check_project_cfg_option("video", "framerate")
        video_fps = float(video_fps)

        plot0 = main_window.ui.results_plot0
        fig0 = plot0.getFigure()
        fig0.clf()
        visualization.road_user_traj(fig0, database_filename, video_fps, homography_filename, camera_image)
        plot0.draw()

        plot1 = main_window.ui.results_plot1
        fig1 = plot1.getFigure()
        fig1.clf()
        visualization.vel_histograms(fig1, database_filename, video_fps, "overall")
        plot1.draw()

        plot2 = main_window.ui.results_plot2
        fig2 = plot2.getFigure()
        fig2.clf()
        visualization.road_user_vels(fig2, database_filename, video_fps)
        plot2.draw()

        plot3 = main_window.ui.results_plot3
        fig3 = plot3.getFigure()
        fig3.clf()
        visualization.road_user_chart(fig3, database_filename)
        plot3.draw()
