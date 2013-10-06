#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import QPoint, Qt
from PyQt4.QtGui import QColor, QPen

import src.drawing as drawing
import src.utils
from src.color_picker import ColorPicker

class Tool(object):
    

    def __init__(self):

        self._name = ''
        self._active = False
        
        self._properties = {}

    def isActive(self):
        return self._active
    
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
    
    def addProperty(self, name, value):
        
        self._properties[name] = ToolProperty(name, value)
        
    def property(self, name):
        
        return self._properties[name]
    
    def propertyValue(self, name):
        
        return self._properties[name].value()
        
class ToolProperty(object):
    
    def __init__(self, name, value):
        
        self._name = name
        self._value = value
        
        
    def name(self):
        
        return self._name
    
    def value(self):
        
        return self._value
        
# ======================================================================================================================

class Picker(Tool):

    def __init__(self):
        
        super(Picker, self).__init__()
        self._name = 'Picker'
        
    def onMousePress(self, canvas, objectMousePos, button):

        pickedColor = QColor(canvas._currentDrawingSurface.pixel(objectMousePos))
        ColorPicker.Instance.setColor(pickedColor)

# ======================================================================================================================

class Pen(Tool):

    def __init__(self):

        super(Pen, self).__init__()
        self._name = 'Pen'

        self._currentPos = QPoint(0, 0)
        self._lastPos = QPoint(0, 0)
        self._pointerPos = QPoint(0, 0)
        self._lastPointerPos = QPoint(0, 0)
        
        self.addProperty('size', 16)
        
        self._deltaX = 0
        self._deltaY = 0
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.black)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)
    
   
    def draw(self, painter, zoom):
        
        x = self._pointerPos.x()
        y = self._pointerPos.y()
        
        size = self.propertyValue('size') * zoom
        
        halfSize = size // 2
        
        painter.setPen(self._drawPen)
        
        painter.drawRect(x - halfSize,
                         y - halfSize,
                         size - 1,
                         size - 1)

    
    def blit(self, painter, ink, press=None):
        
        deltaX = self._currentPos.x() - self._lastPos.x()
        deltaY = self._currentPos.y() - self._lastPos.y()
        
        size = self.propertyValue('size')
        
        if deltaX != 0 or deltaY != 0:
            drawing.drawLine(self._lastPos , self._currentPos, size, ink, painter)
            
        
        elif press is not None:
            ink.blit(self._currentPos.x(), self._currentPos.y(), size, size, painter)
    
    def onMousePress(self, canvas, objectMousePos, button):
        
        size = self.propertyValue('size')
        
        if size > 1:
            src.utils.snapPoint(objectMousePos, size)


        self._lastPos.setX(objectMousePos.x())
        self._lastPos.setY(objectMousePos.y())

    
    def onMouseMove(self, objectMousePos, absoluteMousePos):
        
        size = self.propertyValue('size')
        
        if size > 1:
            src.utils.snapPoint(objectMousePos, size)
        
        self._lastPos.setX(self._currentPos.x())
        self._lastPos.setY(self._currentPos.y())
        
        self._lastPointerPos.setX(self._pointerPos.x())
        self._lastPointerPos.setY(self._pointerPos.y())
        
        self._currentPos.setX(objectMousePos.x())
        self._currentPos.setY(objectMousePos.y())
        
        self._pointerPos.setX(absoluteMousePos.x())
        self._pointerPos.setY(absoluteMousePos.y())
    

# ======================================================================================================================
