#-----------------------------------------------------------------------------------------------------------------------
# Name:        Inks
# Purpose:     Inks module used by Canvas. An Ink is a visual representation of a tool acting on the Canvas
#
# Author:      Rafael Vasco
#
# Created:     28/04/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class Ink(object):

    def __init__(self):

        self._name = ''

    @property
    def name(self):
        return self._name

    def blit(self, x, y, w, h, color, painter):
        return


class Solid(Ink):

    def __init__(self):
        
        super(Solid, self).__init__()
        self._name = 'Solid'

    def blit(self, x, y, w, h, color, painter):
        painter.fillRect(x, y, w, h, color)


class Eraser(Ink):

    def __init__(self):
        super(Eraser, self).__init__()
        self._name = 'Eraser'

    def blit(self, x, y, w, h, color, painter):

        if painter.compositionMode() != QPainter.CompositionMode_Clear:
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(x, y, w, h, Qt.white)



