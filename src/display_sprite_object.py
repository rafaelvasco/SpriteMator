#-----------------------------------------------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------------------------------------------

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


    @property
    def sprite(self):
        return self._sprite

    @property
    def activeSurface(self):
        return self._sprite.activeSurface

    @property
    def activeSurfacePixelData(self):
        return self._sprite.activeSurfacePixelData

    @property
    def displayFrameIndex(self):
        return self._displayFrameIndex

    @displayFrameIndex.setter
    def displayFrameIndex(self, value):
        self._displayFrameIndex = value

    @property
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, value):
        self._backgroundColor = value

    @property
    def backgroundPixmap(self):
        return self._backgroundPixmap

    @backgroundPixmap.setter
    def backgroundPixmap(self, value):
        self._backgroundPixmap = value

    def boundingRect(self):
        return self._boundingRect

    @property
    def areaRect(self):
        return QRect(0, 0, self._boundingRect.width(), self._boundingRect.height())

    def setSprite(self, sprite):

        self._sprite = sprite

        self.updateBoundingRect()

    def updateBoundingRect(self):

        if self._boundingRect.size != self._sprite.size:
            self.prepareGeometryChange()
            self._boundingRect = QRectF(-self._sprite.width/2, -self._sprite.height/2, self._sprite.width, self._sprite.height)

    def unloadSprite(self):

        self._sprite = None
        self._displayFrameIndex = -1
        self.prepareGeometryChange()
        self._boundingRect = QRectF()
        self._frameIndex = 0


    def paint(self, painter, option , widget=None):

        painter.setClipRect(option.exposedRect)

        if self._backgroundColor is not None:

            painter.fillRect(option.rect, self._backgroundColor)

        if self._backgroundPixmap is not None:

            painter.drawTiledPixmap(option.rect, self._backgroundPixmap)

        if self._sprite is not None:

            if self._displayFrameIndex == -1:

                layers = self._sprite.currentAnimation.currentFrame.surfaces

            else:

                layers = self._sprite.currentAnimation.frameAt(self._displayFrameIndex).surfaces

            for layer in layers:

                painter.drawImage(option.rect, layer.image)
