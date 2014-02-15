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
    def __init__(self, parent, label, image):

        super().__init__(parent, label)

        self._layerImage = image

    def draw_content(self, painter, draw_area):

        painter.setPen(Qt.white)

        painter.drawText(20, self._top + 20, self._label)

        if self._layerImage is not None:
            image_rect = QRect(draw_area.right() - 55, draw_area.top() + draw_area.height() / 2 - 24, 48, 48)

            border = self._borderColor if not self._selected else self._borderColorSelected

            painter.setPen(border)

            image_rect.adjust(0, 0, -1, -1)

            painter.drawRect(image_rect)

            image_rect.adjust(1, 1, -1, -1)

            painter.setPen(Qt.black)
            painter.drawRect(image_rect)

            image_rect.adjust(1, 1, 0, 0)

            painter.fillRect(image_rect, Qt.white)
            painter.drawImage(image_rect, self._layerImage,
                              QRect(0, 0, self._layerImage.width(), self._layerImage.height()))


class LayerManager(QWidget):
    layerSelectedChanged = pyqtSignal()
    layerOrderChanged = pyqtSignal()
    layerListChanged = pyqtSignal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self._refreshing = False

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._listWidget = DraggableListWidget()
        self._listWidget.selectedItemChanged.connect(self._on_list_selection_changed)
        self._listWidget.orderChanged.connect(self._on_list_item_order_changed)

        self._addLayerBtn = QPushButton()
        self._addLayerBtn.setText('Add Layer')
        self._addLayerBtn.clicked.connect(self._on_add_layer_btn_clicked)

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._listWidget)
        self._layout.addWidget(self._addLayerBtn)

        self._refreshSpeed = 16

        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refresh_event)
        self._refreshTimer.stop()

        self._sprite = None

    def set_sprite(self, sprite):

        self._sprite = sprite

        self.refresh()

    def clear(self):

        self._sprite = None

        self._listWidget.clear()

        self.update()

    def refresh(self):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation().current_frame()

        self._listWidget.clear()

        for surface in frame.surfaces():
            layer_item = LayerListItem(self._listWidget, surface.name(), surface.image())

            self._listWidget.add_item(layer_item)

        self._listWidget.set_selected_index(frame.current_surface_index())

        self.layerListChanged.emit()

        self.update()

    def set_layer(self, index):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        animation.current_frame().set_surface(index)

        self.layerSelectedChanged.emit()

    def add_layer(self, source_image=None, at=None):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        if source_image is None:
            width = animation.frame_width()
            height = animation.frame_height()
            source_image = utils.create_image(width, height)

        animation.current_frame().add_surface(source_image, at)

        self.refresh()

    def delete_layer(self, index):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation().current_frame()

        frame.remove_surface(index)

        self.refresh()

    def move_layer(self, from_index, to_index):

        if self._sprite is None:
            return

        frame = self._sprite.current_animation().current_frame()

        frame.move_surface(from_index, to_index)

        self.layerOrderChanged.emit()

    def start_refreshing(self):

        self._refreshing = True

        self._refreshTimer.start(self._refreshSpeed)

    def stop_refreshing(self):

        self._refreshTimer.stop()

        self._refreshing = False

    def _on_add_layer_btn_clicked(self):

        self.add_layer()

    def _on_list_selection_changed(self, index):
        print('List Selection Changed')
        self.set_layer(index)

    def _on_list_item_order_changed(self, from_index, to_index):

        self.move_layer(from_index, to_index)

    def _refresh_event(self):

        self.update()