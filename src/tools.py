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

    def onMousePress(self, canvas):
            
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
        

    def onMouseMove(self, canvas):
        
        spritePos = canvas._spriteMousePosition
        absPos = canvas._absoluteMousePosition
        
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
        
        #print('Last Pos: ', self._lastMousePos)
        #print('Curr Pos: ', self._currentMousePos)
        
    
    
    def onMouseRelease(self, canvas):
        
        self.setActive(False)
    
    def draw(self, painter, canvas):
        return
    
    def blit(self, painter, canvas):
        return
    
    
    
        

        
# ======================================================================================================================

class Picker(Tool):

    def __init__(self):
        
        super(Picker, self).__init__()
        self._name = 'Picker'
        

# ======================================================================================================================

class Pen(Tool):

    def __init__(self):

        super(Pen, self).__init__()
        
        self._deltaX = 0
        self._deltaY = 0
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)
        
        self.setSnap(True)
        self.setName('Pen')
        
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
