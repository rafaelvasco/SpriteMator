#--------------------------------------------------
# Name:             draggable_list    
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             28/07/13
# License:          
#--------------------------------------------------

from PyQt4.QtCore import Qt, pyqtSignal, QRect
from PyQt4.QtGui import QPainter, QColor, QWidget, QSizePolicy




class ListItem(object):

    def __init__(self, parent, label, image=None):


        self._posY = 0
        self._index = 0
        self._list = parent
        self._height = parent.itemHeight()
        self._hovered = False
        self._selected = False
        self._dragging = False
        self._label = label
        self._hit = False
        self._backColor = QColor(51,57,64)
        self._borderColor = QColor(132,148,165)
        self._backColorSelected = QColor(47,74,96)
        self._borderColorSelected = QColor(101,172,227)
        
        self._image = image


#-------------------------------------------------------------------------------

    def setLabel(self, v):

        self._label = v

#-------------------------------------------------------------------------------

    def label(self):

        return self._label


#-------------------------------------------------------------------------------

    def setIndex(self, index):

        self._index = index

        itemsLen = self._list.count()
        
        self._posY = ((itemsLen-1)*self._height - index*(self._height))
        
#-------------------------------------------------------------------------------

    def setImage(self, image):
        
        self._image = image

#-------------------------------------------------------------------------------

    def index(self):

        return self._index

#-------------------------------------------------------------------------------

    def top(self):

        return self._posY
#-------------------------------------------------------------------------------

    def bottom(self):

        return self._posY + self._height

#-------------------------------------------------------------------------------

    def move(self, pos):

        self._posY = pos

#-------------------------------------------------------------------------------

    def setDragging(self, v):

        self._dragging = v

#-------------------------------------------------------------------------------

    def isBeingDragged(self):

        return self._dragging

#-------------------------------------------------------------------------------

    def setHovered(self, v):

        self._hovered = v

#-------------------------------------------------------------------------------

    def hovered(self):

        return self._hovered

#-------------------------------------------------------------------------------

    def setSelected(self, v):

        self._selected = v

#-------------------------------------------------------------------------------

    def toggleSelected(self):

        self._selected = not self._selected

#-------------------------------------------------------------------------------

    def isSelected(self):

        return self._selected

#-------------------------------------------------------------------------------

    def draw(self, painter, dragging):

        width = self._list.width()
        
        drawRect = QRect(0, self._posY, width, self._height)
        
        backColor = None
        borderColor = None
        
        if not self._hovered:

            if not self._selected:
                
                backColor = self._backColor
                borderColor = self._borderColor
                

            else:

                backColor = self._backColorSelected
                borderColor = self._borderColorSelected

        else:


            if not self._selected:

                backColor = self._backColor.lighter(120)
                borderColor = self._borderColor.lighter(120)

            else:

                backColor = self._backColorSelected.lighter(120)
                borderColor = self._borderColorSelected.lighter(120)
        
        
        painter.setPen(borderColor)
        painter.drawRect(drawRect.adjusted(0,0,-2,-2))
        painter.fillRect(drawRect.adjusted(1,1,-2,-2), backColor)
        
        painter.setPen(Qt.white)
        painter.drawText(20, self._posY + 30, self._label)
        
        if self._image is not None:
            
            imageRect = QRect(drawRect.right() - 55, drawRect.top() + drawRect.height() / 2 - 24, 48, 48)
            
            painter.setPen(borderColor)
            
            imageRect.adjust(0,0,-1,-1)
            
            painter.drawRect(imageRect)
            
            imageRect.adjust(1,1,-1,-1)
            
            painter.setPen(Qt.black)
            painter.drawRect(imageRect)
            
            imageRect.adjust(1,1,0,0)
            
            painter.fillRect(imageRect, Qt.white)
            painter.drawImage(imageRect, self._image, QRect(0, 0, self._image.width(), self._image.height()))
            



#===============================================================================

class DraggableListWidget(QWidget):

    orderChanged = pyqtSignal(int, int)
    selectedItemChanged = pyqtSignal(int)

    def __init__(self):
        super(DraggableListWidget, self).__init__()

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

    def addItem(self, label, image=None):

        newItem = ListItem(self, label, image)
        newItem.setSelected(True)

        if self._selectedItem is not None:

            self._selectedItem.setSelected(False)

        self._selectedItem = newItem

        self._items.append(newItem)

        self._updateItemIndexes()

        self.update()


    def setSelectedIndex(self, index):

        if index < 0:

            index = 0

        elif index > len(self._items) - 1:

            index = len(self._items) - 1


        if self._selectedItem is not None:

            self._selectedItem.setSelected(False)
            self._selectedItem = None

        self._selectedItem = self._items[index]
        self._selectedItem.setSelected(True)

        self.update()

#-------------------------------------------------------------------------------

    def _updateItemIndexes(self):

        index = 0
        for item in self._items:

            item.setIndex(index)
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

    def itemHeight(self):

        return self._itemHeight


    def count(self):

        return len(self._items)

#-------------------------------------------------------------------------------
    def _onAddButtonClicked(self):

        self.addClicked.emit()
        self.update()

#-------------------------------------------------------------------------------

    def _itemDragBegin(self, item, cursorPoint):

        item.setDragging(True)

        self._draggedItem = item

        self._currentDragOffset = cursorPoint - item.top()

        self._dragSourceIndex = item.index()

        self._dragTargetIndex = self._dragSourceIndex

        self._lastDragY = cursorPoint

#-------------------------------------------------------------------------------

    def _itemDragMove(self, item, cursorPoint):

        item.move(cursorPoint - self._currentDragOffset)

        draggedItemCenter = item.top() + (item.bottom() - item.top()) // 2

        for layerItem in self._items:

            if layerItem.isBeingDragged(): continue


            layerItemTop = layerItem.top()
            layerItemBottom = layerItem.bottom()

            if layerItemTop <= draggedItemCenter < layerItemBottom - 30:

                self._dragTargetIndex = layerItem.index()

                layerItem.setIndex(layerItem.index() + 1)

                break

            elif layerItemBottom >= draggedItemCenter > layerItemTop + 30:

                self._dragTargetIndex = layerItem.index()

                layerItem.setIndex(layerItem.index() - 1)

                break


        self.update()

#-------------------------------------------------------------------------------

    def _itemDragEnd(self, item, cursorPoint):

        print('Moved Layer from index: ', self._dragSourceIndex, ' to index: ', self._dragTargetIndex)

        item.setIndex(self._dragTargetIndex)

        item.setDragging(False)

        self._draggedItem = None

        if self._dragSourceIndex != self._dragTargetIndex :

            self.orderChanged.emit(self._dragSourceIndex, self._dragTargetIndex)

            self._currentDragOffset = 0
        else:

            print('Order Unchanged...')

        self.update()

#-------------------------------------------------------------------------------

    def _moveItem(self, item, point):

        if point < 0:

            point = 0


        maxTop = (len(self._items) - 1) * 60

        if point > maxTop:

            point = maxTop

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

        dragging = self._draggedItem is not None

        for layerItem in self._items:

            if not layerItem.isBeingDragged():
                layerItem.draw(painter, dragging)

        if self._draggedItem is not None:

            self._draggedItem.draw(painter, dragging)

#-------------------------------------------------------------------------------

    def mousePressEvent(self, e):

        if self._draggedItem is not None: return

        pointerY = e.pos().y() - self._scrollOffset

        if self._hoveredItem is not None:

            if e.button() == Qt.RightButton:

                self._itemDragBegin(self._hoveredItem, pointerY)

            elif e.button() == Qt.LeftButton:

                if self._selectedItem is not None:

                    self._selectedItem.setSelected(False)
                    self._selectedItem = None

                self._selectedItem = self._hoveredItem

                self._hoveredItem.setSelected(True)

                print('Selected: ', self._selectedItem.index())

                self.selectedItemChanged.emit(self._selectedItem.index())

                self.update()


#-------------------------------------------------------------------------------

    def mouseReleaseEvent(self, e):

        pointerY = e.pos().y() - self._scrollOffset

        if e.button() == Qt.RightButton:

            if self._draggedItem is not None:

                self._itemDragEnd(self._draggedItem, pointerY)

#-------------------------------------------------------------------------------

    def mouseMoveEvent(self, e):

        pointerY = e.pos().y() - self._scrollOffset


        if self._draggedItem is None:

            for layerItem in self._items:

                if layerItem.top() <= pointerY <= layerItem.bottom():

                    if self._hoveredItem is not None:

                        self._hoveredItem.setHovered(False)
                        self._hoveredItem = None

                    self._hoveredItem = layerItem
                    self._hoveredItem.setHovered(True)
                    self.update()

                    break

        else:

            self._itemDragMove(self._draggedItem, pointerY)

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


        scrollMax = -((len(self._items)) * 60 - self.height())

        if self._scrollOffset < scrollMax:

            self._scrollOffset = scrollMax



#-------------------------------------------------------------------------------

    def leaveEvent(self, e):

        if self._hoveredItem is not None:

            self._hoveredItem.setHovered(False)
            self._hoveredItem = None
            self.update()

#-------------------------------------------------------------------------------
