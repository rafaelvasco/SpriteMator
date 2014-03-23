#-----------------------------------------------------------------------------------------------------------------------
# Name:        Display
# Purpose:     Represents a generic transformable display
#
# Author:      Rafael Vasco
#
# Created:     31/03/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------


from PyQt5.QtCore import QPointF, QPoint, Qt, QSize
from PyQt5.QtGui import QPainter, QTransform, QColor
from PyQt5.QtWidgets import QWidget

import src.utils as utils

from src.resources_cache import ResourcesCache


class Display(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self._viewportTransform = QTransform()
        self._translationTransform = QTransform()
        self._scaleTransform = QTransform()
        self._combinedTransform = QTransform()
        self._invertedCombinedTransform = QTransform()
        self._backgroundColor = QColor(15, 15, 15)
        self._fitInView = False
        self._maintainAspectRatio = True
        self._panning = False
        self._zoom = 1.0
        self._globalMousePos = QPointF()
        self._lastPanPoint = QPointF()
        self._currentFocusPoint = QPointF()
        self._keyTranslationVector = QPoint()
        self._currentObjectSize = QSize()

        self._checkerTileLight = ResourcesCache.get("CheckerTileLight")
        self._checkerTileDark = ResourcesCache.get("CheckerTileDark")

        self._lights_on = True

        self.setMouseTracking(True)
        self.reset_origin()

    def is_panning(self):

        return self._panning

    def zoom_value(self):

        return self._zoom

    def global_mouse_pos(self):
        return self._globalMousePos

    def object_mouse_pos(self):
        return self._invertedCombinedTransform.map(self._globalMousePos)

    def view_mouse_pos(self):

        object_mouse_pos = self.object_mouse_pos()
        obj_size = self._currentObjectSize
        return QPointF(object_mouse_pos.x() - obj_size.width() // 2,
                       object_mouse_pos.y() - obj_size.height() // 2)

    def is_fit_in_view(self):
        return self._fitInView

    def set_fit_in_view(self, fit):
        if self._fitInView != fit:
            self._fitInView = fit
            self._translationTransform.reset()
            self._scaleTransform.reset()
            self.update()

    def current_object_size(self):

        return self._currentObjectSize

    def set_object_size(self, width, height):

        self._currentObjectSize.setWidth(width)
        self._currentObjectSize.setHeight(height)

    def reset_view(self):

        self._fitInView = False
        self._zoom = 1.0
        self.reset_origin()
        self._translationTransform.reset()
        self._scaleTransform.reset()
        self.update()

    def toggle_fit_in_view(self):

        self.set_fit_in_view(not self._fitInView)

    def reset_origin(self):
        self._currentFocusPoint.setX(self.rect().center().x())
        self._currentFocusPoint.setY(self.rect().center().y())

    def maintain_aspect_ratio_enabled(self):
        return self._maintainAspectRatio

    def set_maintain_aspect_ratio(self, maintain):
        if self._maintainAspectRatio != maintain:
            self._maintainAspectRatio = maintain
            self.update()

    def zoom(self, factor, origin):

        self._zoom *= factor

        if self._fitInView:
            self._fitInView = False
            self.update()

        if self._zoom < 1.0:
            self._zoom = 1.0
            return

        if self._zoom > 32.0:
            self._zoom = 32.0
            return

        x, y = origin.x(), origin.y()

        scale_transform = QTransform()

        scale_transform.translate(x, y)
        scale_transform.scale(factor, factor)

        scale_transform.translate(-x, -y)

        #utils.multiply_matrix(self._scaleTransform, scale_transform)
        self._scaleTransform *= scale_transform

        self.update()

    def zoom_to(self, target_zoom):

        self.reset_view()

        self._zoom = target_zoom

        if self._zoom < 0.0:
            self._zoom = 0.0

        ox, oy = self._currentFocusPoint.x(), self._currentFocusPoint.y()

        self._scaleTransform.translate(ox, oy)
        self._scaleTransform.scale(self._zoom, self._zoom)
        self._scaleTransform.translate(-ox, -oy)

        self.update()

    def pan(self, dx, dy):

        if self._fitInView:
            self._fitInView = False

        self._translationTransform.translate(dx, dy)
        self.update()

    def pan_to(self, x, y):

        if self._fitInView:
            self._fitInView = False

        self._translationTransform.reset()
        self._translationTransform.translate(x, y)
        self.update()

    def toggle_back_luminosity(self):

        self._lights_on = not self._lights_on
        self.update()

    def lights_on(self):

        self._lights_on = True
        self.update()

    def lights_off(self):

        self._lights_on = False
        self.update()

    def on_draw_object(self, event, painter):
        return

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), self._backgroundColor)

        if not self._currentObjectSize.isValid():
            return

        view_width = self.width()
        view_height = self.height()

        object_width = self._currentObjectSize.width()
        object_height = self._currentObjectSize.height()

        self._viewportTransform.reset()

        if not self._fitInView:

            center_translate_x = round(view_width / 2 - object_width / 2)
            center_translate_y = round(view_height / 2 - object_height / 2)

            self._viewportTransform.translate(center_translate_x, center_translate_y)

        else:
            final_scale_x = view_width / object_width
            final_scale_y = view_height / object_height

            if self._maintainAspectRatio:

                final_scale = (min(final_scale_x, final_scale_y))

                if final_scale_x > final_scale_y:
                    center_translate_x = round(view_width / 2 - (object_width * final_scale) / 2)
                    self._viewportTransform.translate(center_translate_x, 0)

                elif final_scale_x < final_scale_y:
                    center_translate_y = round(view_height / 2 - (object_height * final_scale) / 2)
                    self._viewportTransform.translate(0, center_translate_y)

                final_scale_x = final_scale_y = final_scale

            self._viewportTransform.scale(final_scale_x, final_scale_y)

        self._combinedTransform = self._viewportTransform * self._translationTransform * self._scaleTransform
        self._invertedCombinedTransform = self._combinedTransform.inverted()[0]

        painter.setTransform(self._combinedTransform)

        if self._lights_on:

            painter.drawTiledPixmap(0, 0, object_width, object_height, self._checkerTileLight)

        else:

            painter.drawTiledPixmap(0, 0, object_width, object_height, self._checkerTileDark)

        self.on_draw_object(event, painter)

    def mousePressEvent(self, e):

        if self.current_object_size().isEmpty():
            return

        if e.button() == Qt.MiddleButton:
            self._panning = True
            self._lastPanPoint = e.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, e):

        if self.current_object_size().isEmpty():
            return

        if e.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, e):

        if self.current_object_size().isEmpty():
            return

        self._globalMousePos.setX(e.pos().x())
        self._globalMousePos.setY(e.pos().y())

        if not self._panning:
            return

        delta = (e.pos() - self._lastPanPoint)

        if self._zoom != 1.0:
            self.pan((delta.x() / self._zoom), (delta.y() / self._zoom))
        else:
            self.pan(delta.x(), delta.y())

        self._lastPanPoint = e.pos()

    def wheelEvent(self, e):

        if self.current_object_size().isEmpty():
            return

        if e.modifiers() & (Qt.ControlModifier | Qt.AltModifier):
            return
        if e.angleDelta().y() > 0:
            self.zoom(2.0, self._globalMousePos)
        else:
            self.zoom(0.5, self._globalMousePos)

    def keyPressEvent(self, e):

        if self.current_object_size().isEmpty():
            return

        if e.key() == Qt.Key_Left:

            self.pan(round(-1), 0)

        elif e.key() == Qt.Key_Right:

            self.pan(round(1), 0)

        elif e.key() == Qt.Key_Up:

            self.pan(0, round(-1))

        elif e.key() == Qt.Key_Down:

            self.pan(0, round(1))

        elif e.key() == Qt.Key_F:

            self.toggle_fit_in_view()

        elif e.key() == Qt.Key_A:

            self.set_maintain_aspect_ratio(not self._maintainAspectRatio)

        elif e.key() == Qt.Key_R:

            self.reset_view()

        elif e.key() == Qt.Key_1:

            self.zoom_to(1.0)

        elif e.key() == Qt.Key_2:

            self.zoom_to(2.0)

        elif e.key() == Qt.Key_3:

            self.zoom_to(3.0)

        elif e.key() == Qt.Key_4:

            self.zoom_to(4.0)

        elif e.key() == Qt.Key_5:

            self.zoom_to(5.0)
