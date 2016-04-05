# homography.py
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class HomographyView(QtGui.QGraphicsView):
    """QGraphicsView used for manipulating and computing image-based homographies.
    """
    def __init__(self, parent):
        super(HomographyView, self).__init__(parent)
        self.cursor_default = QtGui.QCursor(Qt.CrossCursor)
        self.cursor_hover = QtGui.QCursor(Qt.PointingHandCursor)

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
        self.point_rad = 5  # Radius, in pixels
        self.point_pen = QtGui.QPen()
        self.point_brush_color = QtGui.QColor(255, 25, 23)  # R, G, B
        self.point_brush = QtGui.QBrush(self.point_brush_color)
        self.point_selected = False
        self.selected_point = None

    def mouseReleaseEvent(self, event):
        super(HomographyScene, self).mouseReleaseEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        print(event.scenePos().x(), event.scenePos().y())
        if self.point_selected:
            print self.selected_point
            self.point_selected = False
            self.selected_point = None
        else:
            new_point = self.addEllipse(loc[0] - self.point_rad, loc[1] - self.point_rad, self.point_rad * 2, self.point_rad * 2, self.point_pen, self.point_brush)
            self.points.append(new_point)

    def mousePressEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        clicked_point = self.find_clicked_point(loc)
        if clicked_point:
            self.point_selected = True
            self.selected_point = clicked_point

    def mouseMoveEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        clicked_point = self.find_clicked_point(loc)
        if clicked_point:
            self.parent().viewport().setCursor(self.parent().cursor_hover)
        else:
            self.parent().viewport().setCursor(self.parent().cursor_default)


    def find_clicked_point(self, click_loc):
        """
        Searches placed points and returns a point if the user has clicked it.
        Else returns False.
        """
        for point in self.points:
            # if self.click_is_within(point.rect(), click_loc):
            if point.rect().contains(click_loc[0], click_loc[1]):
                return point
        return False

    @staticmethod
    def click_is_within(ellipse_rect, click):
        """
        Returns True if click (x, y) is within the rectange of a drawn ellipse.
        Else returns False. Use this if we need to manually specify a selection radius.
        """
        min_x, min_y, max_x, max_y = ellipse_rect.getCoords()  # Coordinates of bounding rectangle.
        if click[0] > min_x and click[0] < max_x:  # If click within x-bounds
            if click[1] > min_y and click[1] < max_y:  # and click within y-bounds
                return True
            else:
                return False
        else:
            return False
