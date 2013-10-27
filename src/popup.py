'''
Created on 19/10/2013

@author: Rafael
'''

from PyQt4.QtCore import QPoint, QPropertyAnimation, QSize
from PyQt4.QtGui import QWidget, QGridLayout

class Popup(QWidget):

    def __init__(self, container, parent, content):
        
        QWidget.__init__(self, container)
        
        self._visible = False
        self._parent = parent
        
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(content)
        
        self.setLayout(layout)
        self.adjustSize()
        
        self.lower()
        
        self.setVisible(self._visible)
        
    def popin(self):
        
        if not self._visible:
        
            self._visible = True
            self.show()
            
            point = self._parent.rect().bottomRight()
            
            global_point = self._parent.mapToParent(point)
            
            self.move(global_point - QPoint(self._parent.width(), 0))
            
            animation = QPropertyAnimation(self, "pos", self)
            animation.setDuration(150)
            animation.setStartValue(QPoint(self.pos().x(), -self.height()))
            animation.setEndValue(self.pos())
            
            animation.start()
        
    def popout(self):
        
        if self._visible:
        
            self._visible = False
            
            animation = QPropertyAnimation(self, "pos", self)
            animation.setDuration(150)
            animation.setStartValue(self.pos())
            animation.setEndValue(QPoint(self.pos().x(), -self.height()))
            animation.finished.connect(self._onCloseAnimationFinished)
            animation.start()
        
    
    def toggleVisible(self):
        
        if not self._visible:
            
            self.popin()
            
        else:
            
            self.popout()
    
    
    def _onCloseAnimationFinished(self):
        
        self.hide()
        