#--------------------------------------------------
# Name:             layer_list    
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             04/08/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import pyqtSignal, Qt, QTimer
from PyQt4.QtGui import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from src.draggable_list import DraggableListWidget

import src.utils as Utils

class LayerManager(QWidget):
    
    layerSelectedChanged = pyqtSignal()
    layerOrderChanged = pyqtSignal()
    layerListChanged = pyqtSignal()

    def __init__(self, parent=None):

        super(LayerManager, self).__init__(parent)

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
            
            self._listWidget.addItem(surface.name(), surface.image())
            
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