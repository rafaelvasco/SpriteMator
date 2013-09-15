#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import QPoint, Qt
from PyQt4.QtGui import QColor

import src.drawing as drawing
import src.utils
from src.color_picker import ColorPicker

class Tool():


    def __init__(self):

        self._name = ''
        self._active = False


    def isActive(self):
        return self._active

    def setActive(self, active):
        self._active = active

    def onMousePress(self, canvas, pos, button):
        return

    def onMouseMove(self, canvas, pos, buttons):
        return

    def onMouseRelease(self, canvas, pos, button):
        return

    def name(self):
        return self._name

    def draw(self, canvas):
        return



# ======================================================================================================================

class Picker(Tool):

    def __init__(self):
        Tool.__init__(self)

    def onMousePress(self, canvas, pos, button):

        pickedColor = QColor(canvas._currentDrawingSurface.pixel(pos))
        ColorPicker.Instance.setColor(pickedColor)

# ======================================================================================================================

class Pen(Tool):

    def __init__(self):

        Tool.__init__(self)
        self._name = 'Pen'

        self._currentPos = QPoint(0, 0)
        self._lastPos = QPoint(0, 0)
        self._size = 16


    def draw(self, canvas):

        halfSize = self._size / 2

        canvas._painter.drawRect(self._currentPos.x() - halfSize,
                         self._currentPos.y() - halfSize,
                         self._size,
                         self._size, Qt.black)


    def onMousePress(self, canvas, pos, button):

        self._active = True

        painter = canvas._painter

        ink = canvas._primaryInk if button == Qt.LeftButton else canvas._secondaryInk

        self._active = True

        if self._size > 1:
            src.utils.snapPoint(pos, self._size)

        self._currentPos.setX(pos.x())
        self._currentPos.setY(pos.y())

        self._lastPos.setX(self._currentPos.x())
        self._lastPos.setY(self._currentPos.y())

        ink.prepare(painter)

        ink.blit(pos.x(), pos.y(), self._size, self._size, painter)



    def onMouseMove(self, canvas, pos, buttons):

        painter = canvas._painter

        ink = canvas._primaryInk if buttons & Qt.LeftButton else canvas._secondaryInk

        if self._size > 1:
            src.utils.snapPoint(pos, self._size)

        self._lastPos.setX(self._currentPos.x())
        self._lastPos.setY(self._currentPos.y())

        self._currentPos.setX(pos.x())
        self._currentPos.setY(pos.y())



        if self._currentPos != self._lastPos:

            drawing.drawLine(self._lastPos, self._currentPos, self._size, ink, painter)


    def onMouseRelease(self, canvas, pos, button):

        self._active = False

        ink = canvas._primaryInk if button == Qt.LeftButton else canvas._secondaryInk

        ink.finish(canvas._painter)

# ======================================================================================================================

Pen = Pen()
Picker = Picker()