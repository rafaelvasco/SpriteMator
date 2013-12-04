'''
Created on 25/11/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, pyqtSignal, QSize, QRect
from PyQt4.QtGui import QWidget, QColor, QFont, QPainter, QFontMetrics, QFrame, QVBoxLayout, QHBoxLayout, QStackedLayout, QIcon, QAbstractButton

import math

import src.utils as utils

from src.properties import BooleanValue, RangedValue



class Button(QAbstractButton):
    
    leftClicked = pyqtSignal()
    middleClicked = pyqtSignal()
    rightClicked = pyqtSignal()
    activated = pyqtSignal()
    
    def __init__(self, label=None):

        super(Button, self).__init__()

        self._bgColor = QColor(51,51,51)
        self._activeBgColor = QColor(21,21,21)
        self._labelSize = QSize()
        self._size = QSize()
        self._iconSize = QSize()
        self._icon = None
        self._padding = 8
        self._contextMenu = None
        self._idlePixmap = None
        self._checkedPixmap = None
        self._menuTriggerButton = Qt.MiddleButton

        if label is not None:

            self.setText(label)

        else:

            self.setText('Button')

        self._updateSize()
    
    
    def sizeHint(self):
        
        return self._size
    
    def setIcon(self, icon):
        
        self._icon = icon
        
        actualSize = self._icon.actualSize(self.size())
        
        self._iconSize.setWidth(actualSize.width())
        self._iconSize.setHeight(actualSize.height())
        
        self._updateIconPixmaps()
        
        self._updateSize()
        
        self.update()
    
    
    def setIconSize(self, width, height):
        
        self._iconSize.setWidth(width)
        self._iconSize.setHeight(height)
        
        self._updateIconPixmaps()
        
        self._updateSize()
        
        self.update()
    
    
    def setMenu(self, menu):
        
        self._contextMenu = menu
        
   
    def resizeEvent(self, e):

        self._updateSize()

    def mousePressEvent(self, e):
        
    
        if not self.isCheckable():
            
            self.setDown(True)
            
        else:
            
            wasChecked = self.isChecked()
            
            self.setChecked(not self.isChecked())
            
            if not wasChecked and self.isChecked():
                
                self.activated.emit()
    
    def mouseReleaseEvent(self, e):
        
        if not self.isCheckable():
            
            self.setDown(False)
        
        if e.button() == Qt.LeftButton:
            
            self.leftClicked.emit()
            
        elif e.button() == Qt.MiddleButton:
            
            self.middleClicked.emit()
            
        elif e.button() == Qt.RightButton:
            
            self.rightClicked.emit()

    def paintEvent(self, e):

        p = QPainter(self)
        
        active = self.isDown() or self.isChecked()
        
        if active:
            
            
            bgColor = self._activeBgColor
            borderColor = bgColor.lighter(250)
            
        else:

            bgColor = self._bgColor
            borderColor = bgColor.lighter(150)

        p.setPen(borderColor)
        
        drawRect = e.rect().adjusted(0,0,-1,-1)

        p.drawRect(drawRect)

        p.fillRect(drawRect.adjusted(1,1,0,0), bgColor)
        
        
        if self._icon is not None:
            
            drawX = round(drawRect.width() / 2 - self._iconSize.width() / 2) 
            drawY = round(drawRect.height() / 2 - self._iconSize.height() / 2) 
            
            if not active and self._idlePixmap is not None:
                p.drawPixmap(drawX, drawY, self._idlePixmap)
            
            elif active and self._checkedPixmap is not None:
                
                p.drawPixmap(drawX, drawY, self._checkedPixmap) 
            
        else:
                
            p.setPen(Qt.white)
            
            drawX = round(drawRect.width() / 2 - self._labelSize.width() / 2 + self._padding)
            drawY = round(drawRect.height() / 2 + self._labelSize.height() / 3 + self._padding)
            
            p.drawText(drawX, drawY, self.text())

    
    def _updateIconPixmaps(self):
        
        if self._icon is None:
            return
        
        self._idlePixmap = self._icon.pixmap(self._iconSize,  QIcon.Normal, QIcon.Off)
        self._checkedPixmap = self._icon.pixmap(self._iconSize,  QIcon.Normal, QIcon.On)

    def _updateSize(self):
        
        if self._icon is None:
            
            fontMetrics = QFontMetrics(self.font())
            
            self._labelSize.setWidth(fontMetrics.width(self.text()))
            self._labelSize.setHeight(fontMetrics.height())
            
            width = self._labelSize.width() + self._padding * 2
            height = self._labelSize.height() + self._padding * 2
        
        else:
           
            width = self._iconSize.width() + (self._padding * 2)
            height = self._iconSize.height() + (self._padding * 2)
            
        self._size.setWidth(width)
        self._size.setHeight(height)
        
        self.setMinimumSize(self._size)



######################################################################################

  
class Slider(QWidget):

    valueChanged = pyqtSignal(int)

    def __init__(self, minValue, maxValue, label=None):

        super(Slider, self).__init__()

        self._value = 0
        self._minValue = minValue
        self._maxValue = maxValue
        self._step = 1
        self._thumbWidth = 20
        self._thumbRect = QRect()
        self._slidingAreaRect = QRect()

        if label is not None:

            self._label = label

        else:

            self._label = 'Slider'

        self._labelBarColor = QColor(63,91,110)
        self._bgColor = QColor(20,20,20)
        self._indicatorColor = QColor(30,108,125)
        self._thumbColor = QColor(42,157,182)

        self._sliding = False
        

        self._fontMetrics = QFontMetrics(self.font())

        

    def value(self):

        return self._value

    def setValue(self, v):

        v = max(self._minValue, min(v, self._maxValue))

        if v != self._value:

            if self._step == 1:
                
                self._value = int(round(v))

            elif self._step > 1:

                self._value = int(round(utils.snap(v, self._step)))

        self.valueChanged.emit(self._value)

        self._updateThumb()

    def maxValue(self):

        return self._maxValue

    def setMaxValue(self, v):

        if v < self._minValue:

            v = self._minValue

        self._maxValue = v

    def minValue(self):

        return self._minValue

    def setMinValue(self, v):

        if v > self._maxValue:

            v = self._maxValue

        self._minValue = v

    def step(self):

        return self._step

    def setStep(self, v):

        self._step = v


    def _getValueFromPosition(self, pos):

        pos -= self._thumbWidth / 2

        size = self.width() - self._thumbWidth
        

        if pos > size:

            return self._maxValue

        if pos < 0:

            return self._minValue

        percent = pos / size

        return round((self._maxValue - self._minValue) * percent)

    def _updateThumb(self):

        size = self.width() - self._thumbWidth


        pos = round(max(0, min( size * ( ( self._value - self._minValue ) /
                                         ( self._maxValue - self._minValue ) ), size )))



        self._thumbRect.setRect(pos, self.height() / 2, self._thumbWidth, self.height() / 2)
            


        self.update()


    def sizeHint(self):

        return QSize(200,80)

    def resizeEvent(self, e):


        self._updateThumb()

    def mousePressEvent(self, e):

        self._sliding = True

        mousePos = e.pos().x()

        self.setValue(self._getValueFromPosition(mousePos))

    def mouseReleaseEvent(self, e):

        if self._sliding:

            self._sliding = False
            self.update()


    def mouseMoveEvent(self, e):

        if self._sliding:

            mousePos = e.pos().x()

            self.setValue(self._getValueFromPosition(mousePos))


    def wheelEvent(self, e):

        self.setValue(self._value + utils.sign(e.delta())* self._step)

    def paintEvent(self, e):

        drawRect = e.rect()

        p = QPainter(self)

        # LABEL --------------------------------------------------------------------

        labelRect = drawRect.adjusted(0,0,0,-drawRect.height() / 2 - 1)

        p.setPen(self._labelBarColor.lighter())

        p.drawRect(labelRect.adjusted(0,0,-1,-1))

        p.fillRect(labelRect.adjusted(1,1,-1,-1), self._labelBarColor)

        labelSize = QSize(self._fontMetrics.width(self._label), self._fontMetrics.height())

        p.setPen(Qt.white)

        p.drawText(labelRect.width() / 2 - labelSize.width() / 2, labelRect.height() / 2 + labelSize.height() / 3, self._label)


        # ---------------------------------------------------------------------------

        # SLIDER---------------------------------------------------------------------

        # BAR --------

        barRect = drawRect.adjusted(0,drawRect.height() / 2, 0, drawRect.height() * 2)

        p.setPen(self._bgColor.lighter(200))

        p.drawRect(barRect.adjusted(0,0,-1,-1))

        p.fillRect(barRect.adjusted(1,1,-1,-1), self._bgColor)

        # THUMB --------

        p.setPen(self._thumbColor.lighter())

        p.drawRect(self._thumbRect.adjusted(0,0,-1,-1))

        p.fillRect(self._thumbRect.adjusted(1,1,-1,-1), self._thumbColor)

        # VALUE LABEL --------

        valueText = str(self._value)

        valueLabelSize = QSize(self._fontMetrics.width(valueText), self._fontMetrics.height())

        valueIndicatorRect = QRect(self._thumbRect.right() + 2, self._thumbRect.top(), valueLabelSize.width() + 10, self._thumbRect.height())

        if(valueIndicatorRect.right() > barRect.right()):

            valueIndicatorRect.setRect(self._thumbRect.left() - valueIndicatorRect.width() - 1, valueIndicatorRect.top(), valueIndicatorRect.width(), valueIndicatorRect.height())

        p.setPen(self._indicatorColor.lighter())

        p.drawRect(valueIndicatorRect.adjusted(0,0,-1,-1))

        p.fillRect(valueIndicatorRect.adjusted(1,1,-1,-1), self._indicatorColor)

        p.setPen(Qt.white)

        p.drawText(valueIndicatorRect.left() + valueIndicatorRect.width() / 2 - valueLabelSize.width() / 2, 
             valueIndicatorRect.top() + valueIndicatorRect.height() / 2 + valueLabelSize.height() / 3, valueText)



# ========== Vertical Menu ==============================================================

class VerticalMenuItem(object):

    def __init__(self, label):

        super(VerticalMenuItem, self).__init__()

        self._label = label
        self._data = None


    def setData(self, d):

        self._data = d

    def data(self):

        return self._data

    def label(self):

        return self._label


class VerticalMenu(QWidget):

    itemSelectedChanged = pyqtSignal(VerticalMenuItem)
    itemIndexChanged = pyqtSignal(int)
    itemClicked = pyqtSignal(VerticalMenuItem)

    def __init__(self):

        super(VerticalMenu, self).__init__()

        self._items = []
        self._itemHeight = 30
        self._selectedItemIndex = 0
        self._bgColor = QColor(30,30,30)
        self._itemBgColor = QColor(40,40,40)
        self._itemSelectedBgColor = QColor(42,157,182)

    def addItem(self, item):

        self._items.append(item)

        self.update()


    def mousePressEvent(self, e):

        clickedPos = e.pos()

        if clickedPos.y() < len(self._items) * (self._itemHeight):

            oldIndex = self._selectedItemIndex

            self._selectedItemIndex = int(math.floor(clickedPos.y() / self._itemHeight))

            self.itemClicked.emit(self._items[self._selectedItemIndex])

            if self._selectedItemIndex != oldIndex:

                self.itemSelectedChanged.emit(self._items[self._selectedItemIndex])
                self.itemIndexChanged.emit(self._selectedItemIndex)

                self.update()

            

    def paintEvent(self, e):

        widgetArea = e.rect()
        p = QPainter(self)

        

        p.fillRect(widgetArea, self._bgColor)

        for index, item in enumerate(self._items):

            itemRect = QRect(0, (index * (self._itemHeight + 1)), self.width(), self._itemHeight)
            if self._selectedItemIndex is None or self._selectedItemIndex != index:
                p.fillRect(itemRect, self._itemBgColor)
            else:
                p.fillRect(itemRect, self._itemSelectedBgColor)

            p.setPen(QColor('white'))
            p.drawText(itemRect.left() + 20, itemRect.top() + (itemRect.height() / 2 + 4), item.label())

# ========================================================================================


class Inspector(QWidget):
    
    def __init__(self):
        
        super(Inspector, self).__init__()

        self._inspectedItemsMenu = VerticalMenu()

        self._inspectedItemsMenu.itemIndexChanged.connect(self._onItemSelectedChanged)

        self._propertyPages = QStackedLayout()

        self._bgColor = QColor(30,30,30)

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)

        mainLayout.addWidget(self._inspectedItemsMenu)

        mainLayout.addLayout(self._propertyPages)

        mainLayout.setStretch(0, 1)
        mainLayout.setStretch(1, 1)

        self.setLayout(mainLayout)

    def addItem(self, propertyHolder):

        menuItem = VerticalMenuItem(propertyHolder.name())
        menuItem.setData(propertyHolder)

        self._inspectedItemsMenu.addItem(menuItem)

        self._buildPropertyPage(propertyHolder)


    def _buildPropertyPage(self, propertyHolder):

        page = QFrame()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        page.setLayout(layout)

        for propName, propObject in propertyHolder.properties().items():


            if isinstance(propObject, BooleanValue):

                onOffButton = Button(propName)
                onOffButton.setCheckable(True)
                onOffButton.setChecked(propObject.isOn())

                onOffButton.toggled.connect(lambda v, prop = propObject : prop.setValue(v))

                layout.addWidget(onOffButton)


            elif isinstance(propObject, RangedValue):


                slider = Slider(propObject.min(), propObject.max(), propName)
                slider.setValue(propObject.value())

                slider.valueChanged.connect(lambda v, prop = propObject : prop.setValue(v))

                layout.addWidget(slider)

        self._propertyPages.addWidget(page)

    def _onItemSelectedChanged(self, index):

        self.showPage(index)




    def showPage(self, index):

        self._propertyPages.setCurrentIndex(index)

        self.update()

    def paintEvent(self, e):

        p = QPainter(self)

        p.fillRect(e.rect(), self._bgColor)
    
    def sizeHint(self):

        return QSize(800,400)