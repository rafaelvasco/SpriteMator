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


class LayerList(QWidget):

    layerAdded = pyqtSignal()
    layerSelected = pyqtSignal(int)
    layerMoved = pyqtSignal(int, int)

    def __init__(self, parent=None):

        super(LayerList, self).__init__(parent)

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


    def addLayer(self, layer):

        self._listWidget.addItem(layer.name(), layer.image())
        self.update()

    def setSelectedIndex(self, index):

        self._listWidget.setSelectedIndex(index)
        self.update()

    def clear(self):

        self._listWidget.clear()
        self.update()


    def _startRefreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def _stopRefreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False
    

    def _onAddLayerBtnClicked(self):

        self.layerAdded.emit()

    def _onListSelectionChanged(self, index):

        self.layerSelected.emit(index)

    def _onListItemOrderChanged(self, fromIndex, toIndex):

        self.layerMoved.emit(fromIndex, toIndex)
        
    def _refreshEvent(self):

        self.update()