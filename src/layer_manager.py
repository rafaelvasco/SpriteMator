#-----------------------------------------------------------------------------------------------------------------------
# Name:        Layer Manager
# Purpose:     Manages and displays current Sprite's layers;
#
# Author:      Rafael Vasco
#
# Created:     04/08/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from src.draggable_list import DraggableListWidget, ListItem
import src.utils as utils



# ----------------------------------------------------------------------------------------------------------------------


class LayerListItem(ListItem):
    def __init__(self, parent, layer):

        super().__init__(parent, layer.name)

        self._layerImage = layer.image

        self._layer = layer


    def drawContent(self, painter, draw_area):

        painter.setPen(Qt.white)

        painter.drawText(20, self._top + 20, self._label)

        icon = self._layer.image

        # Draw Icon

        icon_draw_area = QRect(draw_area.right() - 55, draw_area.top() + draw_area.height() / 2 - 24, 48, 48)

        border = self._borderColor if not self._selected else self._borderColorSelected

        painter.setPen(border)

        icon_draw_area.adjust(0, 0, -1, -1)

        painter.drawRect(icon_draw_area)

        icon_draw_area.adjust(1, 1, -1, -1)

        painter.setPen(Qt.black)
        painter.drawRect(icon_draw_area)

        icon_draw_area.adjust(1, 1, 0, 0)

        painter.fillRect(icon_draw_area, Qt.white)

        if icon is not None:

            painter.drawImage(icon_draw_area, icon,
                              QRect(0, 0, icon.width(), icon.height()))


class LayerManager(QWidget):

    currentLayerChanged = pyqtSignal(int)
    layerOrderChanged = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self._refreshing = False

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._listWidget = DraggableListWidget()
        self._listWidget.selectedItemChanged.connect(self._onListSelectionChanged)
        self._listWidget.orderChanged.connect(self._onListItemOrderChanged)

        self._addLayerBtn = QPushButton()
        self._addLayerBtn.setText('Add Layer')
        self._addLayerBtn.clicked.connect(self._onAddLayerBtnClicked)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._listWidget)
        self._layout.addWidget(self._addLayerBtn)

        self._refreshSpeed = 16

        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refreshEvent)
        self._refreshTimer.stop()

        self._sprite = None

        self.setAcceptDrops(True)

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

        frame = self._sprite.currentAnimation.currentFrame

        self._listWidget.clear()

        for surface in frame.surfaces:
            layer_item = LayerListItem(self._listWidget, surface)

            self._listWidget.addItem(layer_item)

        self._listWidget.selectedIndex = frame.currentSurfaceIndex

        self.update()

    def setLayer(self, index):

        if self._sprite is None:
            return

        frame = self._sprite.currentAnimation.currentFrame

        frame.setSurface(index)

        self.currentLayerChanged.emit(self._sprite.currentAnimation.currentFrameIndex)

    def addLayer(self, source_image=None, at=None):

        if self._sprite is None:
            return

        frame = self._sprite.currentAnimation.currentFrame

        if source_image is None:

            frame.addEmptySurface()

        else:

           frame.addSurface(source_image, at)

        self.refresh()

    def deleteLayer(self):

        if self._sprite is None:
            return

        frame = self._sprite.currentAnimation.currentFrame

        frame.removeCurrentSurface()

        self.refresh()

    def moveLayer(self, from_index, to_index):

        if self._sprite is None:
            return

        frame = self._sprite.currentAnimation.currentFrame

        frame.moveSurface(from_index, to_index)

        self.layerOrderChanged.emit()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):

        super(LayerManager, self).dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():

            for url in e.mimeData().urls():

                image = utils.loadImage(url.toLocalFile())

                self.addLayer(image)

    def _onAddLayerBtnClicked(self):

        self.addLayer()

    def _onListSelectionChanged(self, index):

        self.setLayer(index)

    def _onListItemOrderChanged(self, from_index, to_index):

        self.moveLayer(from_index, to_index)

    def _refreshEvent(self):

        self.update()