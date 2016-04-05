# homography.py
from PyQt4 import QtGui


class HomographyView(QtGui.QGraphicsView):
    """QGraphicsView used for manipulating and computing image-based homographies.
    """
    def __init__(self, parent):
        super(HomographyView, self).__init__(parent)

    def load_image(self, image):
        """
        Call this to load a new image from the provide QImage into
        this HomographyView's scene. The image's top left corner will
        be placed at (0,0) in the scene.
        """
        new_scene = HomographyScene(self)
        new_scene.addPixmap(QtGui.QPixmap().fromImage(image))
        self.setScene(new_scene)
        self.show()


class HomographyScene(QtGui.QGraphicsScene):
    """QGraphicsScene derivative displayed in HomographyViews.

    Displays image. Places points on image on click.
    """
    def __init__(self, parent):
        super(HomographyScene, self).__init__(parent)
        self.points = []

        # Point configuration
        self.point_rad = 5
        self.point_pen = QtGui.QPen()
        self.point_brush_color = QtGui.QColor(255, 25, 23)
        self.point_brush = QtGui.QBrush(self.point_brush_color)

    def mouseReleaseEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        print(event.scenePos().x(), event.scenePos().y())
        new_point = self.addEllipse(loc[0], loc[1], self.point_rad * 2, self.point_rad * 2, self.point_pen, self.point_brush)
        self.points.append(new_point)
