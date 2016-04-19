from PyQt4 import QtGui, QtCore
import matplotlib

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import visualization
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

    plot0 = main_window.ui.results_plot0
    visualization.road_user_traj(plot0.getFigure(), 'stmarc.sqlite', 30, 'homography.txt', 'stmarc_image.png')
    plot0.draw()

