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

        self.image_loaded = False

        self.status_label = None

    def load_image(self, image):
        """
        Call this to load a new image from the provide QImage into
        this HomographyView's scene. The image's top left corner will
        be placed at (0,0) in the scene.
        """
        self.scene_image = image
        new_scene = HomographyScene(self)
        pmap = new_scene.addPixmap(QtGui.QPixmap().fromImage(image))
        new_scene.register_pixmap(pmap)
        new_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.setScene(new_scene)
        self.show()
        self.image_loaded = True

    def load_image_from_path(self, path):
        im = QtGui.QImage(path)
        self.load_image(im)

    def list_points(self):
        """
        Returns a list of all points (x, y) selected within this view's scene.
        """
        out_points = []
        raw_points = self.scene().points  # List of point objects
        for pt in raw_points:
            qptf = pt.scenePos()
            point = qptf.x(), qptf.y()
            out_points.append(point)
        return out_points

    def update_point_count_status(self, point_list):
        if self.status_label is None:
            return
        self.status_label.setText("{} points selected.".format(len(point_list)))


class HomographyResultView(QtGui.QGraphicsView):
    """QGraphicsView used for viewing the result of image-based homographies.
    """
    def __init__(self, parent):
        super(HomographyResultView, self).__init__(parent)
        self.cursor_default = QtGui.QCursor(Qt.CrossCursor)
        self.image_loaded = False

        new_scene = QtGui.QGraphicsScene(self)
        new_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(124, 124, 124)))
        txt = QtGui.QGraphicsSimpleTextItem("Compute homography to see results here.")
        new_scene.addItem(txt)
        self.setScene(new_scene)
        self.show()

    def load_image(self, image):
        """
        Call this to load a new image from the provide QImage into
        this HomographyView's scene. The image's top left corner will
        be placed at (0,0) in the scene.
        """
        self.scene_image = image
        new_scene = QtGui.QGraphicsScene(self)
        pmap = new_scene.addPixmap(QtGui.QPixmap().fromImage(image))
        new_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.setScene(new_scene)
        self.show()
        self.image_loaded = True

    def load_image_from_path(self, path):
        im = QtGui.QImage(path)
        self.load_image(im)

    def clear_image(self):
        """
        Call this to clear the image from this HomographyView's scene.
        The scene will be filled with a placeholder grey background and message.
        """
        new_scene = QtGui.QGraphicsScene(self)
        new_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(124, 124, 124)))
        txt = QtGui.QGraphicsSimpleTextItem("Compute homography to see results here.")
        new_scene.addItem(txt)
        self.setScene(new_scene)
        self.show()


class HomographyScene(QtGui.QGraphicsScene):
    """QGraphicsScene derivative displayed in HomographyViews.

    Displays image. Places points on image on click.
    """
    def __init__(self, parent):
        super(HomographyScene, self).__init__(parent)
        self.points = []
        self.main_pixmap_item = None  # Either None or a QGraphicsPixmapItem representing the loaded image

        # Point configuration
        self.point_rad = 4  # Radius, in pixels
        self.point_pen_color = QtGui.QColor(255, 74, 13, 230)  # R, G, B, A
        self.point_pen = QtGui.QPen(self.point_pen_color, 2)
        self.point_brush_color = QtGui.QColor(195, 13, 255, 20)  # R, G, B, A
        self.point_brush = QtGui.QBrush(self.point_brush_color)
        self.point_selected = False
        self.selected_point = None

        font = QtGui.QFont()
        font.setPixelSize(12)
        font.setBold(False)
        self.label_font = font
        self.label_pen_color = QtGui.QColor(0, 0, 0)  # R, G, B
        self.label_pen = QtGui.QPen(self.label_pen_color, .1)
        self.label_brush_color = QtGui.QColor(255, 255, 255)  # R, G, B
        self.label_brush = QtGui.QBrush(self.label_brush_color)

    def add_point(self, loc):
        """
        Adds a point (QEllipseItem) with a child QSimpleTextItem displaying a numerical index to the
        scene at the location specified by the (x, y) tuple loc. The new_point (QEllipseItem) is appended to
        self.points. The numerical index displayed in the text label corresponds to 1 + this point's index in
        self.points. This point and it's label are styled using attributes configured in this object's __init__().
        """
        new_point = self.addEllipse(0, 0, self.point_rad * 2, self.point_rad * 2, self.point_pen, self.point_brush)
        new_point.setPos(loc[0] - self.point_rad, loc[1] - self.point_rad)
        new_point.homography_index = len(self.points)

        new_text = QtGui.QGraphicsSimpleTextItem()
        new_text.setPos(-10, -10)
        new_text.setFont(self.label_font)
        new_text.setBrush(self.label_brush)
        new_text.setPen(self.label_pen)
        new_text.setText("{}".format(new_point.homography_index + 1))  # Display number is 1-indexed, not 0-indexed

        self.addItem(new_text)
        new_text.setParentItem(new_point)
        new_point.setCursor(self.parent().cursor_hover)
        new_point.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        self.points.append(new_point)
        self.update_point_list_status()

    def delete_point(self, point, index):
        """
        Given a point (QEllipseItem) with a child QSimpleTextItem and it's index in
        self.points, removes it from the screen, re-indexes following points, and redraws
        following points with new labels.
        """
        self.removeItem(point)
        del self.points[index]
        # Amend following points' indices
        need_update = self.points[index:]
        offset = 0
        for pt in need_update:
            pt.homography_index = index + offset
            text_box = pt.childI tems()[0]
            redraw_box = text_box.boundingRect()
            pt.childItems()[0].setText("{}".format(pt.homography_index + 1))
            self.update(redraw_box)  # Get rid of text artifacts. These can occur when changing from 10 to 9, for example.
            offset += 1
        self.update_point_list_status()

    def mouseReleaseEvent(self, event):
        """
        PyQt has several built in event handlers that you can re-implement.
        This is one of them. If the mouse is released, it stops dragging one of
        the homography points.
        """
        super(HomographyScene, self).mouseReleaseEvent(event)
        if self.point_selected:
            # Note that we are no longer moving a point.
            self.selected_point.setCursor(self.parent().cursor_hover)
            self.point_selected = False
            self.selected_point = None

    def mousePressEvent(self, event ):
        """
        Another event handler. If the mouse is clicked, it checks to see if the
        point is one of the existing points. It then allows the user to drag it
        if it is selected. Adds a new point if there is not already a point.
        """
        super(HomographyScene, self).mousePressEvent(event)
        loc = (event.scenePos().x(), event.scenePos().y())
        clicked_point, cp_index = self.find_clicked_point(loc)
        if clicked_point:
            if event.button() == Qt.RightButton:  # Right click to delete points
                self.delete_point(clicked_point, cp_index)
            else:  # Note that we are currently moving a point
                self.point_selected = True
                self.selected_point = clicked_point
                self.selected_point.setCursor(self.parent().cursor_drag)
        else:  # Otherwise add a new point
            if self.main_pixmap_item.isUnderMouse():  # Check to make sure we're in the image.
                self.add_point(loc)

    def mouseMoveEvent(self, event):
        super(HomographyScene, self).mousePressEvent(event)

    def find_clicked_point(self, click_loc):
        """
        Searches placed points and returns a point if the user has clicked it.
        Else returns False.
        """
        for i, point in enumerate(self.points):
            if point.isUnderMouse():
                return point, i
        return False, None

    def update_point_list_status(self):
        """
        Updates the status bar above the image.
        """
        point_list = self.parent().list_points()
        self.parent().update_point_count_status(point_list)

    def register_pixmap(self, pixmap):
        self.main_pixmap_item = pixmap

    @staticmethod
    def click_is_within(ellipse_rect, click):
        """
        Returns True if click (x, y) is within the rectange of a drawn ellipse.
        Else returns False. Use this if we need to manually specify a selection radius.
        Before using this, check QT docs to evaluate configuring larger bounding boxes around
        objects and letting QT handle item selection.
        """
        min_x, min_y, max_x, max_y = ellipse_rect.getCoords()  # Coordinates of bounding rectangle.
        if click[0] > min_x and click[0] < max_x:  # If click within x-bounds
            if click[1] > min_y and click[1] < max_y:  # and click within y-bounds
                return True
            else:
                return False
        else:
            return False
