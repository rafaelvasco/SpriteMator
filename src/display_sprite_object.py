# ------------------------------------------------------------------------------
# Name:        DisplaySpriteItem
# Purpose:     Represents a Sprite inside a Display, either a Canvas or an AnimationDisplay
#              Reponsible to displaying the sprite and controlling it's state on screen.
#
#
# Author:      Rafael Vasco
#
# Created:     09/08/2014
# Copyright:   (c) Rafael Vasco 2014
# Licence:     <your licence>
#------------------------------------------------------------------------------

from PyQt5.QtCore import QRectF, QRect
from PyQt5.QtWidgets import QGraphicsItem


class DisplaySpriteObject(QGraphicsItem):
    def __init__(self):

        super(DisplaySpriteObject, self).__init__()

        self._sprite = None

        self._displayFrameIndex = -1

        self.prepareGeometryChange()

        self._boundingRect = QRectF()

        self._backgroundColor = None

        self._backgroundPixmap = None

        self._enableOnionSkin = True

    @property
    def sprite(self):
        return self._sprite

    @property
    def active_surface(self):
        return self._sprite.active_surface

    @property
    def active_surface_pixel_data(self):
        return self._sprite.active_surface_pixel_data

    @property
    def display_frame_index(self):
        return self._displayFrameIndex

    @display_frame_index.setter
    def display_frame_index(self, value):
        self._displayFrameIndex = value

    @property
    def background_color(self):
        return self._backgroundColor

    @background_color.setter
    def background_color(self, value):
        self._backgroundColor = value

    @property
    def background_pixmap(self):
        return self._backgroundPixmap

    @property
    def is_empty(self):
        return self._sprite is None

    @background_pixmap.setter
    def background_pixmap(self, value):
        self._backgroundPixmap = value

    def boundingRect(self):
        return self._boundingRect

    @property
    def bounding_rect_i(self):
        return QRect(self._boundingRect.left(),
                     self._boundingRect.top(),
                     self._boundingRect.width(),
                     self._boundingRect.height())

    @property
    def area_rect(self):
        return QRect(0, 0, self._boundingRect.width(), self._boundingRect.height())

    @property
    def width(self):
        return self.boundingRect().width()

    @property
    def height(self):
        return self.boundingRect().height()

    def set_sprite(self, sprite):

        self._sprite = sprite

        self.update_bounding_rect()

    def update_bounding_rect(self):

        if self._boundingRect.size != self._sprite.size:
            self.prepareGeometryChange()
            self._boundingRect = QRectF(-self._sprite.width / 2, -self._sprite.height / 2,
                                        self._sprite.width, self._sprite.height)

    def unload_sprite(self):

        self._sprite = None
        self._displayFrameIndex = -1
        self.prepareGeometryChange()
        self._boundingRect = QRectF()

    def paint(self, painter, option, widget=None):

        painter.setClipRect(option.exposedRect)

        if self._backgroundColor is not None:
            painter.fillRect(option.rect, self._backgroundColor)

        if self._backgroundPixmap is not None:
            painter.drawTiledPixmap(option.rect, self._backgroundPixmap)

        if self._sprite is not None:

            frame_index = self._displayFrameIndex \
                if self._displayFrameIndex != -1 \
                else self._sprite.current_animation.current_frame_index

            if self._enableOnionSkin:

                last_frame_index = frame_index - 1

                if last_frame_index >= 0:

                    last_frame_layers = self._sprite.current_animation. \
                        frame_at(last_frame_index).surfaces

                    painter.setOpacity(0.4)

                    for layer in last_frame_layers:
                        painter.drawImage(option.rect, layer.image)

                    painter.setOpacity(1.0)

            layers = self._sprite.current_animation.frame_at(frame_index).surfaces

            for layer in layers:
                painter.drawImage(option.rect, layer.image)
