'''
Created on 21/09/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QPainter

class CanvasOverlay(QWidget):
    
    def __init__(self, canvas):
        
        super(CanvasOverlay, self).__init__(canvas)
        self._canvas = canvas
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(True)
        self._drawEnabled = True
    
    
    def turnOn(self):
        self._drawEnabled = True
        self.update()
        
    def turnOff(self):
        self._drawEnabled = False
        self.update()
        
    def paintEvent(self, e):
        
        if not self._drawEnabled or self._canvas._currentTool is None:
            return
        
        painter = QPainter(self)
        #painter.setCompositionMode(QPainter.CompositionMode_Difference)
        
        self._canvas._currentTool.draw(painter, self._canvas)
   
