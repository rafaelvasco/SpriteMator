'''
Created on 06/10/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFont, QColor, QFontMetrics

class ToolBox(object):


    def __init__(self, canvas):
        
        self._canvas = canvas
        self._expanded = False
        self._font = QFont('Nokia Cellphone FC')
        self._font.setPointSize(12)
        
        self._toolNameColor = QColor(117,184,255)
        self._primaryInkNameColor = QColor(171, 214, 84)
        self._secondaryInkNameColor = QColor(250, 153, 92)
        
    
    def _buildLayout(self):
        pass
        
        
        
        
    
    def draw(self, painter):
        
        painter.setFont(self._font)
        
        painter.fillRect(0, 0, self._canvas.width(), 30, QColor(10,10,10,150))
        
        painter.setPen(self._toolNameColor)
        painter.drawText(20, 20, self._canvas.currentTool().name())
        
        painter.setPen(Qt.white)
        painter.drawText(75, 20, ">")
        
        painter.setPen(self._primaryInkNameColor)
        painter.drawText(100, 20, self._canvas.primaryInk().name())
        
        painter.setPen(self._secondaryInkNameColor)
        painter.drawText(200, 20, self._canvas.secondaryInk().name())
        