#-----------------------------------------------------------------------------------------------------------------------
# Name:        CanvasOverlay
# Purpose:     Represents canvas overlay where tools icon, selection, etc is drawn on;
#
# Author:      Rafael Vasco
#
# Created:     21/09/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

#-----------------------------------------------------------------------------------------------------------------------


class CanvasOverlay(QWidget):
    
    def __init__(self, canvas):
        
        super(CanvasOverlay, self).__init__(canvas)
        self._canvas = canvas
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(True)
        self._drawEnabled = True
    
    def enable(self):
        self._drawEnabled = True
        self.update()
        
    def disable(self):
        self._drawEnabled = False
        self.update()
        
    def paintEvent(self, e):
        
        if not self._drawEnabled or self._canvas.current_tool() is None:
            return
        
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Difference)
        
        self._canvas.current_tool().draw(painter, self._canvas)
