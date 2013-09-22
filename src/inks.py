#--------------------------------------------------
# Purpose:          Represents the ink of a Tool. An ink control how a tool modifies the canvas. Like solid painting,
#                   erasing, etc.
#
# Author:           Rafael Vasco
# Date:             28/04/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPainter




class Ink(object):

    def __init__(self):

        self._name = ''
        self._color = None

    def color(self):
        return self._color

    def setColor(self, c):
        self._color = c


    def prepare(self, painter):
        return

    def blit(self, x, y, w, h, painter):
        return

    def finish(self, painter):
        return


class Solid(Ink):

    def __init__(self):
        Ink.__init__(self)

    def blit(self, x, y, w, h, painter):
        painter.fillRect(x, y, w, h, self._color)

class Eraser(Ink):

    def __init__(self):
        Ink.__init__(self)

    def blit(self, x, y, w, h, painter):

        if painter.compositionMode() != QPainter.CompositionMode_Clear:
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(x, y, w, h, Qt.white)




