# -----------------------------------------------------------------------------
# Name:        Display
# Purpose:     Represents the base transformable display that is inherited by the Canvas
# and the AnimationDisplay
#
# Author:      Rafael Vasco
#
# Created:     31/03/2013
# Copyright:   (c) Rafael Vasco 2014
# Licence:     <your licence>
#------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QTransform
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from src.display_sprite_object import DisplaySpriteObject
from src.resources_cache import ResourcesCache
import src.utils as utils


class Display(QGraphicsView):
    def __init__(self):

        super(Display, self).__init__()

        self.setScene(QGraphicsScene())

        self._spriteObject = DisplaySpriteObject()

        self.scene().addItem(self._spriteObject)

        self._backgroundColor = None

        self._backLightOn = True

        self._lightBackgroundPixmap = ResourcesCache.get("CheckerTileLight")

        self._darkBackgroundPixmap = ResourcesCache.get("CheckerTileDark")

        self._lastFocusPoint = QPoint()

        self._zoom = 1.0

        self._fitInView = False

        self._panning = False

        self._leftMousePressed = False

        self._spacePressed = False

        self._dragPos = QPoint()

        self._storedTransform = QTransform()

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setRenderHint(QPainter.Antialiasing, False)

        self.setMouseTracking(True)

        self.setStyleSheet("border: 0px;")

    @property
    def is_panning(self):
        return self._panning

    @property
    def zoom(self):
        return self._zoom

    @property
    def background_color(self):
        return self._backgroundColor

    @background_color.setter
    def background_color(self, value):

        self._backgroundColor = value
        self._spriteObject.background_color = value

    def turn_backlight_on(self):

        self._backLightOn = True
        self._spriteObject.background_pixmap = self._lightBackgroundPixmap

    def turn_backlight_off(self):

        self._backLightOn = False
        self._spriteObject.background_pixmap = self._darkBackgroundPixmap

    def toggle_backlight(self):

        self._backLightOn = not self._backLightOn

        if self._backLightOn:
            self.turn_backlight_on()
        else:
            self.turn_backlight_off()

    def is_fit_in_view(self):
        return self._fitInView

    def reset_view(self):

        self.resetTransform()
        self._zoom = 1.0

    def toggle_view(self):

        if not self.transform().isIdentity():

            self._storedTransform = self.transform()
            self.resetTransform()

        else:

            self.setTransform(self._storedTransform)

    def set_fit_in_view(self, fit):

        if self._fitInView != fit:
            self._fitInView = fit

        self.resetTransform()

        if self._fitInView:
            # Calculate scale factor to cover view increasing the scale by multiples of 2.0
            # to keep pixel perfectness

            scale_factor_x = self.width() / self.sceneRect().width()
            scale_factor_y = self.height() / self.sceneRect().height()

            scale_factor = max(scale_factor_x, scale_factor_y)

            scale_factor = utils.snap_ceil(scale_factor, 2.0)

            self.scale(scale_factor, scale_factor)

    def toggle_fit_in_view(self):

        self.set_fit_in_view(not self._fitInView)

    def zoom_to(self, target_zoom):

        self._fitInView = False

        self._zoom *= target_zoom

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(target_zoom, target_zoom)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)

    def unload_sprite(self):

        self.reset_view()

        if not self._spriteObject.is_empty:
            self._spriteObject.unload_sprite()

        self.scene().update()

    def update_viewport(self):

        self._spriteObject.update_bounding_rect()

        w = self._spriteObject.sprite.width
        h = self._spriteObject.sprite.height

        self.setSceneRect(-w / 2, -h / 2, w, h)

        self.scene().update()

    def resizeEvent(self, e):

        w = self._spriteObject.sprite.width
        h = self._spriteObject.sprite.height

        self.setSceneRect(-w / 2, -h / 2, w, h)

        if not self._fitInView:

            self.centerOn(self._lastFocusPoint)

        else:
            self.centerOn(0, 0)

    def enterEvent(self, e):

        self.setFocus()

    def leaveEvent(self, e):

        self.clearFocus()

    def mousePressEvent(self, e):

        if e.button() == Qt.MiddleButton:

            self.setCursor(Qt.ClosedHandCursor)
            self._panning = True
            self._dragPos = e.pos()
            e.accept()
            return

        elif e.button() == Qt.LeftButton:

            self._leftMousePressed = True

            if self._spacePressed:
                self._panning = True
                self.setCursor(Qt.ClosedHandCursor)
                self._dragPos = e.pos()
                e.accept()
                return

        super(Display, self).mousePressEvent(e)

    def mouseReleaseEvent(self, e):

        if self._panning and e.button() == Qt.MiddleButton:

            self.setCursor(Qt.BlankCursor)
            self._panning = False

        elif e.button() == Qt.LeftButton:

            self._leftMousePressed = False

            if self._panning:

                self._panning = False

                if self._spacePressed:

                    self.setCursor(Qt.OpenHandCursor)

                else:

                    self.setCursor(Qt.BlankCursor)

        super(Display, self).mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        pass

    def mouseMoveEvent(self, e):

        if self._panning:
            new_pos = e.pos()
            diff = new_pos - self._dragPos
            self._dragPos = new_pos

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())

        super(Display, self).mouseMoveEvent(e)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Space and not self._leftMousePressed:
            self._spacePressed = True
            self.setCursor(Qt.OpenHandCursor)

        super(Display, self).keyPressEvent(e)

    def keyReleaseEvent(self, e):

        if e.key() == Qt.Key_Space:
            self._spacePressed = False

        if not self._spacePressed and not self._panning:
            self.setCursor(Qt.BlankCursor)

        super(Display, self).keyReleaseEvent(e)

    def wheelEvent(self, e):

        focus_point = self.mapToScene(e.pos())

        self._lastFocusPoint.setX(round(focus_point.x()))
        self._lastFocusPoint.setY(round(focus_point.y()))

        steps = e.angleDelta().y() / 120

        if steps == 0:
            e.ignore()
            return

        scale = pow(2.0, steps)

        self.zoom_to(scale)

    def paintEvent(self, e):

        super(Display, self).paintEvent(e)

        painter = QPainter(self.viewport())

        self.draw_overlay(painter)

    def draw_overlay(self, painter):
        pass