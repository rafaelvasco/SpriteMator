#--------------------------------------------------
# Name:             layer_list    
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             04/08/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import pyqtSignal, Qt, QTimer, QRect
from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from src.draggable_list import DraggableListWidget, ListItem

import src.utils as Utils


class LayerListItem(ListItem):
    
    def __init__(self, parent, label, image):
        
        super().__init__(parent, label)
        
        self._layerImage = image
        
    def drawContent(self, painter, drawArea):
        
        painter.setPen(Qt.white)
        painter.drawText(20, self._top + 20, self._label)
        
        if self._layerImage is not None:
            
            imageRect = QRect(drawArea.right() - 55, drawArea.top() + drawArea.height() / 2 - 24, 48, 48)
            
            border = self._borderColor if not self._selected else self._borderColorSelected
            
            painter.setPen(border)
            
            imageRect.adjust(0,0,-1,-1)
            
            painter.drawRect(imageRect)
            
            imageRect.adjust(1,1,-1,-1)
            
            painter.setPen(Qt.black)
            painter.drawRect(imageRect)
            
            imageRect.adjust(1,1,0,0)
            
            painter.fillRect(imageRect, Qt.white)
            painter.drawImage(imageRect, self._layerImage, QRect(0, 0, self._layerImage.width(), self._layerImage.height()))

class LayerManager(QWidget):
    
    layerSelectedChanged = pyqtSignal()
    layerOrderChanged = pyqtSignal()
    layerListChanged = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._listWidget = DraggableListWidget()
        self._listWidget.selectedItemChanged.connect(self._onListSelectionChanged)
        self._listWidget.orderChanged.connect(self._onListItemOrderChanged)

        self._addLayerBtn = QPushButton()
        self._addLayerBtn.setText('Add Layer')
        self._addLayerBtn.clicked.connect(self._onAddLayerBtnClicked)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.addWidget(self._listWidget)
        self._layout.addWidget(self._addLayerBtn)
        
        self._refreshSpeed = 16
        
        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refreshEvent)
        self._refreshTimer.stop()
        
        
        self._sprite = None
        
    
    def setSprite(self, sprite):
        
        self._sprite = sprite
        
        self.refresh()
        
    def clear(self):
        
        self._sprite = None
        self._listWidget.clear()
        
        self.update()
        
    def refresh(self):
        
        if self._sprite is None:
            return
        
        frame = self._sprite.currentAnimation().currentFrame()
        
        self._listWidget.clear()
        
        for surface in frame.surfaces():
            
            layerItem = LayerListItem(self._listWidget, surface.name(), surface.image())
            
            self._listWidget.addItem(layerItem)
            
        self._listWidget.setSelectedIndex(frame.currentSurfaceIndex())
        
        self.layerListChanged.emit()
            
        self.update()
        
    
    def setLayer(self, index):
        
        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()

        animation.currentFrame().setSurface(index)
        
        self.layerSelectedChanged.emit()
    

    def addLayer(self, sourceImage=None, at=None):
        
        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()
        
        if sourceImage is None:

            width = animation.frameWidth()
            height = animation.frameHeight()
            sourceImage = Utils.createImage(width, height)

        animation.currentFrame().addSurface(sourceImage, at)
        
        self.refresh()
        
        
   
    
    def deleteLayer(self, index):
        
        if self._sprite is None:
            return
        
        frame = self._sprite.currentAnimation().currentFrame()

        frame.deleteSurface(index)
        
        self.refresh()
    
    
    def moveLayer(self, fromIndex, toIndex):
        
        if self._sprite is None:
            return
        
        frame = self._sprite.currentAnimation().currentFrame()
        
        frame.moveSurface(fromIndex, toIndex)
        
        self.layerOrderChanged.emit()
    


    def _startRefreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def _stopRefreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False
    

    def _onAddLayerBtnClicked(self):
        
        self.addLayer()
       
    def _onListSelectionChanged(self, index):
        print('List Selection Changed')
        self.setLayer(index)
        
    def _onListItemOrderChanged(self, fromIndex, toIndex):
        
        self.moveLayer(fromIndex, toIndex)
       
    def _refreshEvent(self):

        self.update()