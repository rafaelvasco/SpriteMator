#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import QPoint, Qt, QRect
from PyQt4.QtGui import QColor, QPen

import src.drawing as drawing
import src.utils
from src.color_picker import ColorPicker

class Tool():
    

    def __init__(self):

        self._name = ''
        self._active = False


    def isActive(self):
        return self._active
    
    def dirtyRect(self, zoom):
        return None

    def setActive(self, active):
        self._active = active

    def onMousePress(self, canvas, objectMousePos, button):
        return

    def onMouseMove(self, objectMousePos, absoluteMousePos):
        return
    
    def onMouseRelease(self, canvas, objectMousePos, button):
        return
    
    def draw(self, painter):
        return
    
    def blit(self, painter, ink):
        return
    
    def name(self):
        return self._name


# ======================================================================================================================

class Picker(Tool):

    def __init__(self):
        Tool.__init__(self)

    def onMousePress(self, canvas, objectMousePos, button):

        pickedColor = QColor(canvas._currentDrawingSurface.pixel(objectMousePos))
        ColorPicker.Instance.setColor(pickedColor)

# ======================================================================================================================

class Pen(Tool):

    def __init__(self):

        Tool.__init__(self)
        self._name = 'Pen'

        self._currentPos = QPoint(0, 0)
        self._lastPos = QPoint(0, 0)
        self._pointerPos = QPoint(0, 0)
        self._lastPointerPos = QPoint(0, 0)
        self._size = 16
        self._deltaX = 0
        self._deltaY = 0
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)
    
    def dirtyRect(self, zoom):
        
        size = self._size * zoom * 2
        
        left = self._pointerPos.x() - size
        top = self._pointerPos.y() - size
        right = self._pointerPos.x() + size
        bottom = self._pointerPos.y() + size
        
        if self._deltaX > 0 :
            left -= self._deltaX
        else:
            right -= self._deltaX
            
        if self._deltaY > 0:
            top -= self._deltaY
        else:
            bottom -= self._deltaY
        
        return QRect(left, top, right - left, bottom - top)

    def draw(self, painter, zoom):
        
        x = self._pointerPos.x()
        y = self._pointerPos.y()
        
        size = self._size * zoom
        halfSize = size // 2
        
        painter.setPen(self._drawPen)
        
        
        
        painter.drawRect(x - halfSize,
                         y - halfSize,
                         size - 1,
                         size - 1)

    
    def blit(self, painter, ink):
        
        if self._currentPos.x() != self._lastPos.x() or self._currentPos.y() != self._lastPos.y():
            drawing.drawLine(self._lastPos, self._currentPos, self._size, ink, painter)
        
        else:
            ink.blit(self._currentPos.x(), self._currentPos.y(), self._size, self._size, painter)
    
    def onMousePress(self, canvas, objectMousePos, button):

        if self._size > 1:
            src.utils.snapPoint(objectMousePos, self._size)


        self._lastPos.setX(objectMousePos.x())
        self._lastPos.setY(objectMousePos.y())

    
    def onMouseMove(self, objectMousePos, absoluteMousePos):
        
        self._deltaX = self._pointerPos.x() - self._lastPointerPos.x()
        self._deltaY = self._pointerPos.y() - self._lastPointerPos.y()
        
        
        if self._size > 1:
            src.utils.snapPoint(objectMousePos, self._size)
        
        self._lastPos.setX(self._currentPos.x())
        self._lastPos.setY(self._currentPos.y())
        
        self._lastPointerPos.setX(self._pointerPos.x())
        self._lastPointerPos.setY(self._pointerPos.y())
        
        self._currentPos.setX(objectMousePos.x())
        self._currentPos.setY(objectMousePos.y())
        
        self._pointerPos.setX(absoluteMousePos.x())
        self._pointerPos.setY(absoluteMousePos.y())
    

# ======================================================================================================================

Pen = Pen()
Picker = Picker()