# homography.py
from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class HomographyView(QtGui.QGraphicsView):
    """QGraphicsView used for manipulating and computing image-based homographies.
    """
    def __init__(self, parent):
        super(HomographyView, self).__init__(parent)
        self.cursor_default = QtGui.QCursor(Qt.CrossCursor)
        self.cursor_hover = QtGui.QCursor(Qt.OpenHandCursor)
        self.cursor_drag = QtGui.QCursor(Qt.ClosedHandCursor)

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
        self.point_rad = 12  # Radius, in pixels
        self.point_pen_color = QtGui.QColor(255, 74, 13, 230)  # R, G, B, A
        self.point_pen = QtGui.QPen(self.point_pen_color, 10)
        self.point_brush_color = QtGui.QColor(195, 13, 255, 20)  # R, G, B, A
        self.point_brush = QtGui.QBrush(self.point_brush_color)
        self.point_selected = False
        self.selected_point = None

    def mouseReleaseEvent(self, event):
        super(HomographyScene, self).mouseReleaseEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        if self.point_selected:
            # Re-placing moved point
            self.selected_point.setCursor(self.parent().cursor_hover)
            self.point_selected = False
            self.selected_point = None

    def mousePressEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        clicked_point, cp_index = self.find_clicked_point(loc)
        if clicked_point:
            if event.button() == Qt.RightButton:
                # Delete point
                self.removeItem(clicked_point)
                del self.points[cp_index]
                # Amend following points' indices
                need_update = self.points[cp_index:]
                offset = 0
                for point in need_update:
                    point.homography_index = cp_index + offset
                    point.childItems()[0].setText("{}".format(point.homography_index + 1))
                    offset += 1
            else:
                self.point_selected = True
                self.selected_point = clicked_point
                self.selected_point.setCursor(self.parent().cursor_drag)
        else:
            new_point = self.addEllipse(loc[0] - self.point_rad, loc[1] - self.point_rad, self.point_rad * 2, self.point_rad * 2, self.point_pen, self.point_brush)
            new_point.homography_index = len(self.points)
            # new_text = self.addText(loc[0] - self.point_rad, loc[1] - self.point_rad, "Bob", QtGui.QFont())
            new_text = QtGui.QGraphicsSimpleTextItem()
            new_text.setPos(loc[0]-10, loc[1]-10)
            new_text.setText("{}".format(new_point.homography_index + 1))  # Display number is 1-indexed, not 0-indexed
            self.addItem(new_text)
            new_text.setParentItem(new_point)
            # new_point_group = self.createItemGroup([new_point, new_text])
            new_point.setCursor(self.parent().cursor_hover)
            # new_point_group.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
            new_point.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

            self.points.append(new_point)

    def mouseMoveEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)

    def find_clicked_point(self, click_loc):
        """
        Searches placed points and returns a point if the user has clicked it.
        Else returns False.
        """
        for i, point in enumerate(self.points):
            # if self.click_is_within(point.rect(), click_loc):
            # if point.rect().contains(click_loc[0], click_loc[1]):
            if point.isUnderMouse():
                return point, i
        return False, None

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
