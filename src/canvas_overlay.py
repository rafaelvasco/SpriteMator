'''
Created on 21/09/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QPainter

class CanvasOverlay(QWidget):
    
    def __init__(self, parent):
        
        QWidget.__init__(self, parent)
        self._canvas = parent
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(True)
        #self.setUpdatesEnabled(False)
        
    def paintEvent(self, e):
        
        painter = QPainter(self)
        
        print('paint cursor')
        self._canvas._currentTool.draw(painter, self._canvas._zoom)
        
    
