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
    
    def dirtyRect(self):
        return None

    def setActive(self, active):
        self._active = active

    def onMousePress(self, canvas, pos, button):
        return

    def onMouseMove(self, pos):
        return
    
    def onMouseRelease(self, canvas, pos, button):
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
        self._pointerPos = QPoint(0, 0)
        self._size = 16
        self._deltaX = 0
        self._deltaY = 0
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.black)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setCapStyle(Qt.SquareCap)
    
    def dirtyRect(self):
        
        left = self._pointerPos.x() - self._size
        top = self._pointerPos.y() - self._size 
        right = self._pointerPos.x() + self._size
        bottom = self._pointerPos.y() + self._size
        
        if self._deltaX > 0 :
            left -= self._deltaX
        else:
            right -= self._deltaX
            
        if self._deltaY > 0:
            top -= self._deltaY
        else:
            bottom -= self._deltaY
        
        return QRect(left, top, right - left, bottom - top)

    def draw(self, painter):
        
        painter.setPen(self._drawPen)
        painter.drawRect(self._pointerPos.x() - self._size // 2 ,
                         self._pointerPos.y() - self._size // 2 ,
                         self._size,
                         self._size)

    def blit(self, painter, ink):
        
        if self._currentPos.x() != self._lastPos.x() or self._currentPos.y() != self._lastPos.y():
            drawing.drawLine(self._lastPos, self._currentPos, self._size, ink, painter)
        
        else:
            
            ink.blit(self._currentPos.x(), self._currentPos.y(), self._size, self._size, painter)
    
    def onMousePress(self, canvas, pos, button):

        if self._size > 1:
            src.utils.snapPoint(pos, self._size)


        self._lastPos.setX(pos.x())
        self._lastPos.setY(pos.y())

    
    def onMouseMove(self, pos):
        
        self._deltaX = pos.x() - self._pointerPos.x()
        self._deltaY = pos.y() - self._pointerPos.y()
        
        print(self._deltaX, ' , ' , self._deltaY)
        
        self._pointerPos.setX(pos.x())
        self._pointerPos.setY(pos.y())
        
        if self._size > 1:
            src.utils.snapPoint(pos, self._size)
        
        self._lastPos.setX(self._currentPos.x())
        self._lastPos.setY(self._currentPos.y())
        
        self._currentPos.setX(pos.x())
        self._currentPos.setY(pos.y())
    

# ======================================================================================================================

Pen = Pen()
Picker = Picker()