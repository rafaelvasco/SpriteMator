'''
Created on 20/10/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPainter, QColor


class DynamicPanel(QWidget):
    
    mouseEntered = pyqtSignal()
    mouseLeft = pyqtSignal()
    
    def __init__(self, width, height, alignment):

        super(DynamicPanel, self).__init__()
        
        
        if alignment == Qt.Vertical:

            self._mainLayout = QVBoxLayout()

        elif alignment == Qt.Horizontal:

            self._mainLayout = QHBoxLayout()

        self.setLayout(self._mainLayout)

        self._layouts = {}
        
        self.setMinimumSize(width, height)
        
    
    def layout(self, name):

        return self._layouts[name]

    def addLayout(self, name, layout):

        self._layouts[name] = layout
        self._mainLayout.addLayout(layout)
    def addWidget(self, layoutName, widget):

        self._layouts[layoutName].addWidget(widget)

    def clear(self, layout=None):

        if layout is not None:

            layoutToClear = layout
            
        else:

            layoutToClear = self._mainLayout

        for i in reversed(range(layoutToClear.count())):

                item = layoutToClear.takeAt(i)
                widget = item.widget()

                if widget is not None:

                    widget.setParent(None)

                else:

                    self.clear(item.layout())

        #self.adjustSize()
    
    def mousePressEvent(self, e):
        e.accept()
    
    def enterEvent(self, e):
        
        self.setCursor(Qt.ArrowCursor)
        self.mouseEntered.emit()
    
    def leaveEvent(self, e):
        
        self.mouseLeft.emit()

    def paintEvent(self, e):
        
        p = QPainter(self)

        p.fillRect(e.rect(), QColor(10,10,10, 217))