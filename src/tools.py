#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import QPoint, Qt
from PyQt4.QtGui import QPen, QColor

import src.drawing as drawing
import src.utils as utils



class Tool(object):
    

    def __init__(self):

        self._name = ''
        self._active = False
        self._pressMousePos = QPoint()
        self._lastMousePos = QPoint()
        self._currentMousePos = QPoint()
        self._absoluteMousePos = QPoint()
        self._lastButtonPressed = None
        self._snapPos = False
        
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)
        
        self._drawBrush = None
    
    def name(self):
        return self._name
    
    def setName(self, name):
        
        self._name = name

    def isActive(self):
        
        return self._active
    
    def setActive(self, active):
        
        self._active = active
        
    def setSnap(self, snap):
        
        self._snapPos = snap
        

    def _processMousePress(self, canvas, mouseEvent):
            
        if mouseEvent.button() != Qt.LeftButton and mouseEvent.button() != Qt.RightButton:
            return
            
        self.setActive(True)
        
        pixelSize = canvas._pixelSize
        mousePosition = canvas._spriteMousePosition
        
        if pixelSize > 1 and self._snapPos:
        
            spritePos = utils.snapPoint(mousePosition, pixelSize)
        else:
            
            spritePos = mousePosition
        
        self._pressMousePos.setX(spritePos.x())
        self._pressMousePos.setY(spritePos.y())
        
        self._lastMousePos.setX(spritePos.x())
        self._lastMousePos.setY(spritePos.y())
        
        self._currentMousePos.setX(spritePos.x())
        self._currentMousePos.setY(spritePos.y())
        
        self.onMousePress(canvas, mouseEvent)

    def _processMouseMove(self, canvas, mouseEvent):
        
        spritePos = canvas._spriteMousePosition
        absPos = mouseEvent.pos()
        
        size = canvas._pixelSize
        
        self._lastMousePos.setX(self._currentMousePos.x())
        self._lastMousePos.setY(self._currentMousePos.y())
        
        if size > 1 and self._snapPos:
            self._currentMousePos = utils.snapPoint(spritePos, size)
        else:
            self._currentMousePos.setX(spritePos.x())
            self._currentMousePos.setY(spritePos.y())
            
        
        self._absoluteMousePos.setX(absPos.x())
        self._absoluteMousePos.setY(absPos.y())
        
        self.onMouseMove(canvas, mouseEvent)
    
    def _processMouseRelease(self, canvas, mouseEvent):
        
        self.setActive(False)
        
        self.onMouseRelease(canvas, mouseEvent)
        
    def onMousePress(self, canvas, mouseEvent):
        return
    
    def onMouseMove(self, canvas, mouseEvent):
        return 
    
    def onMouseRelease(self, canvas, mouseEvent):
        return
        
        
    
    def draw(self, painter, canvas):
        return
    
    def blit(self, painter, canvas):
        return
    
    
    
        

        
# ======================================================================================================================

class Picker(Tool):

    def __init__(self):
        
        super(Picker, self).__init__()
        self._name = 'Picker'
    
    def draw(self, painter, canvas):
        
        x = self._absoluteMousePos.x()
        y = self._absoluteMousePos.y()
        
        size = canvas._pixelSize * canvas._zoom
        
        
        halfSize = size // 2
        
        painter.setPen(self._drawPen)
        
        painter.drawRect(x - halfSize,
                         y - halfSize,
                         size - 1,
                         size - 1)
    
    def onMousePress(self, canvas, mouseEvent):
        
        pickedColor = QColor(canvas._drawingSurface.pixel(self._pressMousePos))
        canvas.colorPicked.emit(pickedColor,  mouseEvent)
        

# ======================================================================================================================

class Pen(Tool):

    def __init__(self):

        super(Pen, self).__init__()
        
        self._deltaX = 0
        self._deltaY = 0
        
        
        self.setSnap(True)
        self.setName('Pen')
        
    def draw(self, painter, canvas):
        
        x = self._absoluteMousePos.x()
        y = self._absoluteMousePos.y()
        
        size = canvas._pixelSize * canvas._zoom
        
        if size <= 0.0:
            
            return
        
        if size == 1.0:
            
            painter.fillRect(x,y,1,1,Qt.white)
            
            painter.setPen(Qt.white)
            
            painter.drawLine(x, y - 4, x, y - 8)
            painter.drawLine(x, y + 4, x, y + 8)
            
            painter.drawLine(x - 4, y , x - 8, y)
            painter.drawLine(x + 4, y , x + 8, y)
        
        elif size == 2.0:
            
            painter.fillRect(x - 1, y - 1, 2, 2, Qt.white)
            
            painter.setPen(Qt.white)
            
            painter.drawLine(x - 2, y - 8, x + 1 , y - 8)
            painter.drawLine(x - 2, y + 7, x + 1 , y + 7)
            
            painter.drawLine(x - 8, y - 2, x - 8 , y + 1)
            painter.drawLine(x + 7, y - 2, x + 7 , y + 1)
            
        elif size == 4.0:
            
            painter.setPen(Qt.white)
            
            painter.drawRect(x - 2, y - 2, 4, 4)
            
            painter.drawLine(x - 2, y - 8, x + 2, y - 8)
            painter.drawLine(x - 2, y + 8, x + 2, y + 8)
            
            painter.drawLine(x - 8, y - 2, x - 8, y + 2)
            painter.drawLine(x + 8, y - 2, x + 8, y + 2)
            
        else:
            
            painter.setPen(Qt.white)
            
            halfSize = size // 2
            sizeBy8 = size // 8
            
            painter.drawRect(x - halfSize, y - halfSize, size, size)
            
            painter.drawLine(x, y - sizeBy8, x, y + sizeBy8)
            painter.drawLine(x - sizeBy8, y, x + sizeBy8, y)
    
    def blit(self, painter, canvas):
        
        size = canvas._pixelSize
        lastButtonPressed = canvas._lastButtonPressed
        
        if lastButtonPressed == Qt.LeftButton:
            ink = canvas._primaryInk
            color = canvas._primaryColor
        
        elif lastButtonPressed == Qt.RightButton:
            ink = canvas._secondaryInk
            color = canvas._secondaryColor
        
        deltaX = self._currentMousePos.x() - self._lastMousePos.x()
        deltaY = self._currentMousePos.y() - self._lastMousePos.y()
        
        
        if deltaX != 0 or deltaY != 0:
            drawing.drawLine(self._lastMousePos , self._currentMousePos, size, ink, color, painter)
        else:
            ink.blit(self._currentMousePos.x(), self._currentMousePos.y(), size, size, color, painter)

# ======================================================================================================================
