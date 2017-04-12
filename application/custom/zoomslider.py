# zoomslider.py
from PyQt5 import QtWidgets


class ZoomSlider(QtWidgets.QSlider):
    """Slider used for zooming a HomographyView or a HomographyResultView.
    """
    slider_start = 50.
    def __init__(self, parent):
        super(ZoomSlider, self).__init__(parent)
        self.zoom_target = None  # QGraphicsView
        self.zoom_increment = .02
        self.valueChanged.connect(self.valueChanged_handler)
        self.prev_value = self.value()
        self.zoom_percentage = 1

    def valueChanged_handler(self):
        if self.zoom_target is None:
            self.resetSliderPosition()  # If no target set, do not manipulate slider.
            return
        elif not self.zoom_target.image_loaded:
            self.resetSliderPosition()
            return
        slider_val = self.value()
        desired_percentage = slider_val / self.slider_start 
        scale = desired_percentage / self.zoom_percentage
        self.zoom_percentage = desired_percentage
        self.zoom_target.scale(scale, scale)

    def resetSliderPosition(self):
        self.setValue(self.slider_start)
