# --------------------------------------------------------------------------------------------------
# Name:        Layer Manager
# Purpose:     Manages and displays current Sprite's layers;
#
# Author:      Rafael Vasco
#
# Created:     04/08/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------------------------------

from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy

from src.view.draggable_list_base_widget import DraggableListWidget, ListItem
import src.helpers.utils as utils


# -------------------------------------------------------------------------------------------------

class LayerListItem(ListItem):
    def __init__(self, parent, layer):
        super().__init__(parent, layer.name)

        self._layerImage = layer.image

        self._layer = layer

    def draw_content(self, painter, draw_area):
        painter.setPen(Qt.white)

        painter.drawText(20, self._top + 20, self._label)

        icon = self._layer.image

        # Draw Icon

        icon_draw_area = QRect(draw_area.right() - 55,
                               draw_area.top() + draw_area.height() / 2 - 24, 48, 48)

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
    layerImported = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._listWidget = DraggableListWidget()
        self._listWidget.selectedItemChanged.connect(self._on_layer_selected_changed)
        self._listWidget.orderChanged.connect(self._on_layer_order_changed)

        self._addLayerBtn = QPushButton()
        self._addLayerBtn.setText('Add Layer')
        self._addLayerBtn.clicked.connect(self._on_add_layer_btn_clicked)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._listWidget)
        self._layout.addWidget(self._addLayerBtn)

        self._sprite = None

        self.setAcceptDrops(True)

    def set_sprite(self, sprite):

        self._sprite = sprite

        self.rebuild()

    def clear(self):

        self._sprite = None

        self._listWidget.clear()

        self.update()

    def rebuild(self):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation.current_frame

        self._listWidget.clear()

        for surface in frame.surfaces:
            layer_item = LayerListItem(self._listWidget, surface)

            self._listWidget.add_item(layer_item)

        self._listWidget.selected_index = frame.current_surface_index

        self.update()

    def set_layer(self, index):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation.current_frame

        frame.set_surface(index)

        self.currentLayerChanged.emit(self._sprite.current_animation.current_frame_index)

    def add_layer(self, source_image=None, at=None):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation.current_frame

        if source_image is None:

            frame.add_empty_surface()

        else:

            frame.add_surface(source_image, at)

        self.rebuild()

    def remove_layer(self):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation.current_frame

        frame.remove_current_surface()

        self.rebuild()

    def move_layer(self, from_index, to_index):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation.current_frame

        frame.move_surface(from_index, to_index)

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
                image = utils.load_image(url.toLocalFile())

                self.add_layer(image)

            self.layerImported.emit()

    def _on_add_layer_btn_clicked(self):

        self.add_layer()

    def _on_layer_selected_changed(self, index):

        self.set_layer(index)

    def _on_layer_order_changed(self, from_index, to_index):

        self.move_layer(from_index, to_index)
