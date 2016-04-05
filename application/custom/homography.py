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
        # im = QtGui.QImage(filename)
        # im = QtGui.QImage("stmarc_image.png")
        new_scene = HomographyScene(self)
        new_scene.addPixmap(QtGui.QPixmap().fromImage(image))
        # this.drawBackground = draw_image
        self.setScene(new_scene)
        self.show()


class HomographyScene(QtGui.QGraphicsScene):
    """QGraphicsScene derivative displayed in HomographyViews.

    Displays image. Places points on image on click.
    """
    def __init__(self, parent):
        super(HomographyScene, self).__init__(parent)
        self.points = []

    def mouseReleaseEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)
        print(event.scenePos().x(), event.scenePos().y())
