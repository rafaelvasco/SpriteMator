'''
Created on 06/10/2013

@author: Rafael
'''

from PyQt4.QtCore import pyqtSignal, Qt, QSize
from PyQt4.QtGui import QWidget, QPainter, QColor, QHBoxLayout, QPushButton, QButtonGroup, QIcon, QPixmap, QMenu

from src.resources_cache import ResourcesCache

from src.widgets import Button

class ToolBox(QWidget):
    
    mouseEntered = pyqtSignal()
    mouseLeft = pyqtSignal()
    
    toolChanged = pyqtSignal(str)
    primaryInkChanged = pyqtSignal(str)
    secondaryInkChanged = pyqtSignal(str)
    
    def __init__(self, canvas):
        
        super(ToolBox, self).__init__(canvas)
        
        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        self.setFont(ResourcesCache.get("BigFont"))
        
        self._registeredTools = []
        self._registeredInks= []
        
        self._freeToolsIds = []
        
        self._toolSlots = []
        self._inkSlots = []
        
        self._backgroundColor = QColor(40,40,40)
        self._toolLabelColor = QColor(112,231,255)
        
        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignCenter)
        self._layout.setContentsMargins(4, 4, 4, 4)
        
        self._toolsLayout = QHBoxLayout()
        self._inksLayout = QHBoxLayout()
        
        self._toolsLayout.setContentsMargins(0, 0, 0, 0)
        self._toolsLayout.setAlignment(Qt.AlignLeft)
        
        self._inksLayout.setContentsMargins(0, 0, 0, 0)
        self._inksLayout.setAlignment(Qt.AlignLeft)
        
        self._layout.addLayout(self._toolsLayout)
        self._layout.addLayout(self._inksLayout)
        
        self._toolsButtonGroup = QButtonGroup()
        
        self._toolsMenu = QMenu()
        
        self._toolsMenu.addAction("Test1")
        self._toolsMenu.addAction("Test2")
        
        self.setLayout(self._layout)
        
        self._createInkSlot(0)
        self._createInkSlot(1)
        
        self.resize(0, 50)
        
    
    def registerTool(self, tool, isDefault=None):
        
        if tool.name() not in self._registeredTools:
            
            slotIndex = self._createToolSlot(isDefault)
            
            self._registeredTools.append(tool.name())
            
            if len(self._toolSlots) < 5:
            
                self._assignToolToSlot(tool, slotIndex)
            
            else:
                
                self._freeToolsIds.append(tool.name())
                
    def selectToolSlot(self, slot):
        
        self._toolSlots[slot]['button'].setChecked(True)
        self.toolChanged.emit(self._toolSlots[slot]['id'])
            
    def _createToolSlot(self, selected=None):
        
        slotButton = Button()
        slotButton.setCheckable(True)
        
        index = len(self._toolSlots)
        
        if selected is not None and selected == True:
            
            slotButton.setChecked(True)
        
        slotButton.activated.connect(self._toolSlotTriggered)
        
        self._toolSlots.append({'button' : slotButton})
        
        self._toolsButtonGroup.addButton(slotButton, index)
        
        self._toolsLayout.addWidget(slotButton)
        
        return index
    
    
    def _createInkSlot(self, slotNumber):
        
        slotButton = Button()
        slotButton.setFont(self.font())
        slotButton.setStyleSheet("border-color: rgb(56,56,56); background-color: rgb(17,17,17); font-size: 12pt;")
        
        
        index = len(self._inkSlots)
        
        if slotNumber == 0:
            
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button1"), QIcon.Normal, QIcon.Off)
            
            slotButton.setIcon(icon)
            slotButton.setIconSize(18,23)
        
        elif slotNumber == 1:
            
            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button2"), QIcon.Normal, QIcon.Off)
            
            slotButton.setIcon(icon)
            slotButton.setIconSize(18,23)
        
        self._inkSlots.append({'button' : slotButton})
        
        self._inksLayout.addWidget(slotButton)
        
        return index
        
        
    def _assignToolToSlot(self, tool, slot):
        
        if slot < 0 or slot > len(self._toolSlots) - 1:
            
            raise Exception('[ToolBox] > _assignToolToSlot : invalid slot parameter')
        
        self._toolSlots[slot]['id'] = tool.name()
        
        icon = tool.icon()
        
        if icon is not None:
            
            toolButton = self._toolSlots[slot]['button']
            
            toolButton.setIcon(tool.icon())
            toolButton.setTooltip(tool.name())
        
    def _assignInkToSlot(self, ink, slot):
        
        if slot != 0 and slot != 1:
            
            raise Exception('[ToolBox] > _assignInkToSlot : invalid slot parameter')
        
        
        label = ink.name()
        self._inkSlots[slot]['id'] = label
        
        self._inkSlots[slot]['button'].setText(label)

    
    def registerInk(self, ink, slot=None):
        
        if not ink.name() in self._registeredInks:
            
            self._registeredInks.append(ink.name())
            
            if slot is not None:
                
                if slot == 0 or slot == 1:
                    
                    self._assignInkToSlot(ink, slot)
                
    
    
    ####### EVENTS ###################################################################
    
    
    def mousePressEvent(self, e):
        e.accept()
    
    
    def wheelEvent(self, e):
        
        e.accept()
    
    def enterEvent(self, e):
        
        self.mouseEntered.emit()
        self.setCursor(Qt.PointingHandCursor)
    
    def leaveEvent(self, e):
        
        self.mouseLeft.emit()
    
    def paintEvent(self, e):
        
        p = QPainter(self)
        
        rect = e.rect()
        
        p.setPen(self._backgroundColor.lighter())
        p.drawRect(rect.adjusted(0,0,-1,-1))
        
        p.fillRect(rect.adjusted(1,1,-1,-1), self._backgroundColor)
        
    def _toolSlotTriggered(self):  
        
        triggeredSlot = self._toolsButtonGroup.checkedId()
        
        self.toolChanged.emit(self._toolSlots[triggeredSlot]['id'])
        
    ##################################################################################
