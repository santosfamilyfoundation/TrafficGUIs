from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class QTPLT(object):
    """Matplotlib"""
    def __init__(self):
        super(QTPLT, self).__init__()
        self.fig = Figure()
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
    a_plot.add_to_widget(some.)
    ax = a_plot.figure.add_subplot(111)
    data = [random.random() for i in range(10)]
    # discards the old graph
    ax.hold(False)
    # plot data
    ax.plot(data, '*-')
    a_plot.show()