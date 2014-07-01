#-----------------------------------------------------------------------------------------------------------------------
# Name:        DraggableList
# Purpose:     Generic draggable scroll list;
#
# Author:      Rafael Vasco
#
# Created:     28/07/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, \
                            QSizePolicy, \
                            QListWidget, \
                            QListWidgetItem, \
                            QAbstractItemView, \
                            QApplication


class ListItem(object):
    def __init__(self, parent, label):

        self._top = 0
        self._index = 0
        self._list = parent
        self._height = parent.item_height()
        self._hovered = False
        self._selected = False
        self._dragging = False
        self._label = label
        self._hit = False
        self._backColor = QColor(51, 57, 64)
        self._borderColor = QColor(132, 148, 165)
        self._backColorSelected = QColor(47, 74, 96)
        self._borderColorSelected = QColor(101, 172, 227)

    #-------------------------------------------------------------------------------

    def set_label(self, v):

        self._label = v

    #-------------------------------------------------------------------------------

    def label(self):

        return self._label

    #-------------------------------------------------------------------------------

    def set_index(self, index):

        self._index = index

        items_length = self._list.count()

        self._top = ((items_length - 1) * self._height - index * self._height)

    #-------------------------------------------------------------------------------

    def index(self):

        return self._index

    #-------------------------------------------------------------------------------

    def top(self):

        return self._top

    #-------------------------------------------------------------------------------

    def bottom(self):

        return self._top + self._height

    #-------------------------------------------------------------------------------

    def move(self, pos):

        self._top = pos

    #-------------------------------------------------------------------------------

    def set_dragging(self, v):

        self._dragging = v

    #-------------------------------------------------------------------------------

    def is_being_dragged(self):

        return self._dragging

    #-------------------------------------------------------------------------------

    def set_hovered(self, v):

        self._hovered = v

    #-------------------------------------------------------------------------------

    def hovered(self):

        return self._hovered

    #-------------------------------------------------------------------------------

    def set_selected(self, v):

        self._selected = v

    #-------------------------------------------------------------------------------

    def toggle_selected(self):

        self._selected = not self._selected

    #-------------------------------------------------------------------------------

    def is_selected(self):

        return self._selected

    #-------------------------------------------------------------------------------

    def draw(self, painter):

        width = self._list.width()

        draw_rect = QRect(0, self._top, width, self._height)

        if not self._hovered:

            if not self._selected:

                back_color = self._backColor
                border_color = self._borderColor

            else:

                back_color = self._backColorSelected
                border_color = self._borderColorSelected

        else:

            if not self._selected:

                back_color = self._backColor.lighter(120)
                border_color = self._borderColor.lighter(120)

            else:

                back_color = self._backColorSelected.lighter(120)
                border_color = self._borderColorSelected.lighter(120)

        painter.setPen(border_color)
        painter.drawRect(draw_rect.adjusted(0, 0, -2, -2))
        painter.fillRect(draw_rect.adjusted(1, 1, -2, -2), back_color)

        self.draw_content(painter, draw_rect)

    def draw_content(self, painter, draw_area):
        pass


#===============================================================================

class DraggableListWidget(QWidget):
    orderChanged = pyqtSignal(int, int)
    selectedItemChanged = pyqtSignal(int)

    def __init__(self):
        super(DraggableListWidget, self).__init__()

        self._lastDragY = 0
        self._items = []

        self._selectedItem = None

        self._hoveredItem = None

        self._itemHeight = 60

        self._draggedItem = None

        self._scrollOffset = 0

        self._currentDragOffset = 0

        self._dragSourceIndex = 0

        self._dragTargetIndex = 0

        self.setMouseTracking(True)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #-------------------------------------------------------------------------------

    def add_item(self, item):

        item.set_selected(True)

        if self._selectedItem is not None:
            self._selectedItem.set_selected(False)

        self._selectedItem = item

        self._items.append(item)

        self._update_item_indexes()

        self.update()

    def set_selected_index(self, index):

        if index < 0:

            index = 0

        elif index > len(self._items) - 1:

            index = len(self._items) - 1

        if self._selectedItem is not None:
            self._selectedItem.set_selected(False)
            self._selectedItem = None

        self._selectedItem = self._items[index]
        self._selectedItem.set_selected(True)

        self.update()

    #-------------------------------------------------------------------------------

    def _update_item_indexes(self):

        index = 0
        for item in self._items:
            item.set_index(index)
            index += 1

        #-------------------------------------------------------------------------------

    def clear(self):

        self._items.clear()

        self._hoveredItem = None

        self._selectedItem = None

        self._scrollOffset = 0

        self._draggedItem = None

        self._currentDragOffset = 0

        self._dragSourceIndex = 0

        self._dragTargetIndex = 0

        self.update()

    #-------------------------------------------------------------------------------

    def item_height(self):

        return self._itemHeight

    def count(self):

        return len(self._items)

    #-------------------------------------------------------------------------------
    def _on_add_button_clicked(self):

        self.addClicked.emit()
        self.update()

    #-------------------------------------------------------------------------------

    def _item_drag_begin(self, item, cursor_point):

        item.set_dragging(True)

        self._draggedItem = item

        self._currentDragOffset = cursor_point - item.top()

        self._dragSourceIndex = item.index()

        self._dragTargetIndex = self._dragSourceIndex

        self._lastDragY = cursor_point

    #-------------------------------------------------------------------------------

    def _item_drag_move(self, item, cursor_point):

        item.move(cursor_point - self._currentDragOffset)

        dragged_item_center = item.top() + (item.bottom() - item.top()) // 2

        for layerItem in self._items:

            if layerItem.is_being_dragged():
                continue

            layer_item_top = layerItem.top()
            layer_item_bottom = layerItem.bottom()

            if layer_item_top <= dragged_item_center < layer_item_bottom - 30:

                self._dragTargetIndex = layerItem.index()

                layerItem.set_index(layerItem.index() + 1)

                break

            elif layer_item_bottom >= dragged_item_center > layer_item_top + 30:

                self._dragTargetIndex = layerItem.index()

                layerItem.set_index(layerItem.index() - 1)

                break

        self.update()

    #-------------------------------------------------------------------------------

    def _item_drag_end(self, item, cursor_point):

        print('Moved Layer from index: ', self._dragSourceIndex, ' to index: ', self._dragTargetIndex)

        item.set_index(self._dragTargetIndex)

        item.set_dragging(False)

        self._draggedItem = None

        if self._dragSourceIndex != self._dragTargetIndex:
            self.orderChanged.emit(self._dragSourceIndex, self._dragTargetIndex)

            self._currentDragOffset = 0

        self.update()

    #-------------------------------------------------------------------------------

    def _move_item(self, item, point):

        if point < 0:
            point = 0

        max_top = (len(self._items) - 1) * 60

        if point > max_top:
            point = max_top

        collided = False

        for layerItem in self._items:

            if layerItem.top() == point:
                collided = True

                break

        if not collided:
            item.move(point)

        #-------------------------------------------------------------------------------

    def paintEvent(self, e):

        painter = QPainter(self)

        painter.translate(0, self._scrollOffset)

        for layerItem in self._items:

            if not layerItem.is_being_dragged():
                layerItem.draw(painter)

        if self._draggedItem is not None:
            self._draggedItem.draw(painter)

        #-------------------------------------------------------------------------------

    def mousePressEvent(self, e):

        if self._draggedItem is not None:
            return

        pointer_x = e.pos().y() - self._scrollOffset

        if self._hoveredItem is not None:

            if e.button() == Qt.RightButton:

                self._item_drag_begin(self._hoveredItem, pointer_x)

            elif e.button() == Qt.LeftButton:

                if self._selectedItem is not None:
                    self._selectedItem.set_selected(False)
                    self._selectedItem = None

                self._selectedItem = self._hoveredItem

                self._hoveredItem.set_selected(True)

                self.selectedItemChanged.emit(self._selectedItem.index())

                self.update()

            #-------------------------------------------------------------------------------

    def mouseReleaseEvent(self, e):

        pointer_y = e.pos().y() - self._scrollOffset

        if e.button() == Qt.RightButton:

            if self._draggedItem is not None:
                self._item_drag_end(self._draggedItem, pointer_y)

            #-------------------------------------------------------------------------------

    def mouseMoveEvent(self, e):

        pointer_y = e.pos().y() - self._scrollOffset

        if self._draggedItem is None:

            for layerItem in self._items:

                if layerItem.top() <= pointer_y <= layerItem.bottom():

                    if self._hoveredItem is not None:
                        self._hoveredItem.set_hovered(False)
                        self._hoveredItem = None

                    self._hoveredItem = layerItem
                    self._hoveredItem.set_hovered(True)
                    self.update()

                    break

        else:

            self._item_drag_move(self._draggedItem, pointer_y)

        #-------------------------------------------------------------------------------

    def wheelEvent(self, e):

        if len(self._items) * 60 < self.height():
            return

        if self._draggedItem is not None: return

        if e.delta() > 0:

            self._scrollOffset += 60
            self.update()

        elif e.delta() < 0:

            self._scrollOffset -= 60
            self.update()

        if self._scrollOffset > 0:
            self._scrollOffset = 0

        scroll_max = -((len(self._items)) * 60 - self.height())

        if self._scrollOffset < scroll_max:
            self._scrollOffset = scroll_max

    def leaveEvent(self, e):

        if self._hoveredItem is not None:
            self._hoveredItem.set_hovered(False)
            self._hoveredItem = None
            self.update()

#-------------------------------------------------------------------------------


class DraggableListWidget2(QListWidget):

    itemMoved = pyqtSignal(int, int, QListWidgetItem)

    def __init__(self):
        super(DraggableListWidget2, self).__init__()
        self._initUi()
        self._draggedItem = None
        self._draggedRow = None

    def _initUi(self):
        self.setMouseTracking(True)
        self.setSelectionRectVisible(False)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.itemSelectionChanged.connect(self._onItemSelected)
        self.itemMoved.connect(self._onItemMoved)

    def paintEvent(self, e):

        p = QPainter(self)

        p.fillRect(e.rect(), QColor(20,20,20))

        super(DraggableListWidget2, self).paintEvent(e)

    def dropEvent(self, e):

        super(DraggableListWidget2, self).dropEvent(e)

        print(self.row(self._draggedItem))

        self.itemMoved.emit(self._draggedRow, self.row(self._draggedItem), self._draggedItem)

    def startDrag(self, e):

        self._draggedItem = self.currentItem()
        self._draggedRow= self.row(self._draggedItem)

        super(DraggableListWidget2, self).startDrag(e)

    def _onItemSelected(self):
        pass

    def _onItemMoved(self, original_index, new_index, item):

        pass


class DraggableListItem(QListWidgetItem):

    def __init__(self, title):
        super(DraggableListItem, self).__init__()

        self.setText(title)

    def set_draggable(self, draggable):

        if draggable:

            self.setFlags(self.flags() | Qt.ItemIsDragEnabled)

        else:

            self.setFlags(self.flags() & ~Qt.ItemIsDragEnabled)


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    listWidget = DraggableListWidget2()

    listWidget.addItem(DraggableListItem('Item1'))
    listWidget.addItem(DraggableListItem('Item2'))
    listWidget.addItem(DraggableListItem('Item3'))

    item = DraggableListItem('Item4')
    item.set_draggable(False)

    listWidget.addItem(item)


    listWidget.show()

    sys.exit(app.exec_())