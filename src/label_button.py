'''
Created on 13/10/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QLabel

class LabelButton(QLabel):
    
    clicked = pyqtSignal()

    def __init__(self, text=None):
        
        super(LabelButton, self).__init__()
        
        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        if text is not None:
        
            self.setText(text)
            
        
    def mouseReleaseEvent(self, e):
        
        self.clicked.emit()
        
   
    