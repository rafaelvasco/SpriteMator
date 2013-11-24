'''
Created on 06/10/2013

@author: Rafael
'''

from PyQt4.QtCore import pyqtSignal, Qt, QSize
from PyQt4.QtGui import QWidget, QPainter, QHBoxLayout, QVBoxLayout, QColor, QGridLayout

from src.label_button import LabelButton
from src.resources_cache import ResourcesCache
from src.dynamic_panel import DynamicPanel
from src.popup import Popup

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
        
        self.setFont(ResourcesCache.get("NokiaFont"))
        
        self._registeredTools = {}
        self._registeredInks= {}
        
        self._currentActiveInkPanelIndex = 0
        self._currentToolId = None
        self._currentPrimaryInkId = None
        self._currentSecondaryInkId = None
        
        self._currentToolButton = LabelButton()
        self._currentToolButton.setAlignment(Qt.AlignCenter)
        self._currentToolButton.clicked.connect(self._onCurrentToolButtonClicked)
        
        self._currentPrimaryInkButton = LabelButton()
        self._currentPrimaryInkButton.setAlignment(Qt.AlignCenter)
        self._currentPrimaryInkButton.clicked.connect(self._onCurrentPrimaryInkButtonClicked)
        
        self._currentSecondaryInkButton = LabelButton()
        self._currentSecondaryInkButton.setAlignment(Qt.AlignCenter)
        self._currentSecondaryInkButton.clicked.connect(self._onCurrentSecondaryInkButtonClicked)
        
        self._toolsPanel = DynamicPanel(canvas.width(), canvas.height(), Qt.Horizontal)
        self._toolsPanel.setFont(ResourcesCache.get("NokiaFont"))
        self._toolsPanel.setBackgroundColor(QColor(36, 50, 64, 180))
        self._toolsPanel.mouseEntered.connect(self._onPanelMouseEntered)
        self._toolsPanel.mouseLeft.connect(self._onPanelMouseLeft)
        
        self._inksPanel = DynamicPanel(canvas.width(), canvas.height(), Qt.Horizontal)
        self._inksPanel.setFont(ResourcesCache.get("NokiaFont"))
        self._inksPanel.setBackgroundColor(QColor(36, 50, 64, 180))
        self._inksPanel.mouseEntered.connect(self._onPanelMouseEntered)
        self._inksPanel.mouseLeft.connect(self._onPanelMouseLeft)
        
        self._toolsPopup = Popup(canvas, self, self._toolsPanel)
        self._inksPopup = Popup(canvas, self, self._inksPanel)
        
        layout = QHBoxLayout()
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._currentToolButton)
        layout.addWidget(self._currentPrimaryInkButton)
        layout.addWidget(self._currentSecondaryInkButton)
        
        
        self.setLayout(layout)
        
        self._initializePanels()
        
        
    
    def registerTool(self, tool, setAsCurrent=None):
        
        if tool.name() not in self._registeredTools:
        
            self._registeredTools[tool.name()] = tool
            
            toolButton = LabelButton(tool.name())
            toolButton.clicked.connect(lambda: self._onToolSelected(tool))
            
            self._toolsPanel.addWidget("toolsNamesPanel", toolButton)
            self._toolsPopup.adjustSize()
            
            if setAsCurrent is not None:
                
                self._updateCurrentTool(tool.name())
                
            
    
    def registerInk(self, ink, putOnSlot=None):
        
        if not ink in self._registeredInks:
            
            self._registeredInks[ink.name] = ink
            
            inkButton = LabelButton(ink.name())
            inkButton.clicked.connect(lambda: self._onInkSelected(self._currentActiveInkPanelIndex, ink))
            
            self._inksPanel.addWidget("inksNamesPanel", inkButton)
            self._inksPopup.adjustSize()
            
            if putOnSlot is not None:
                
                if putOnSlot == 1:
                    
                    self._updateCurrentPrimaryInk(ink.name())
                    
                elif putOnSlot == 2:
                    
                    self._updateCurrentSecondaryInk(ink.name())
    
    def updateSize(self, width, height):
        
        self.resize(width, 40)
        self._toolsPopup.resize(width + 1, height)
        self._inksPopup.resize(width + 1, height)
    
    def _updateCurrentTool(self, toolName):
        
        self._currentToolId = toolName
        self._currentToolButton.setText(toolName)
        
    def _updateCurrentPrimaryInk(self, inkName):
        
        self._currentPrimaryInkId = inkName
        self._currentPrimaryInkButton.setText(inkName)
    
    def _updateCurrentSecondaryInk(self, inkName):
        
        self._currentSecondaryInkId = inkName
        self._currentSecondaryInkButton.setText(inkName)
    
    def _initializePanels(self):
        
        toolsPanelLayout = QVBoxLayout()
        toolsPanelLayout.setAlignment(Qt.AlignTop)
        toolsPanelLayout.setSpacing(20)
        
        self._toolsPanel.addLayout("toolsNamesPanel", toolsPanelLayout)
        self._toolsPanel.addLayout("toolsPropsPanel", QGridLayout())
        
        self._inksPanel.addLayout("inksNamesPanel", QVBoxLayout())
        self._inksPanel.addLayout("inksPropsPanel", QGridLayout())
        
        
    def mousePressEvent(self, e):
        e.accept()
    
    
    def enterEvent(self, e):
        
        self.setCursor(Qt.ArrowCursor)
        self.mouseEntered.emit()
    
    def leaveEvent(self, e):
        self.mouseLeft.emit()
    
    def paintEvent(self, e):
        
        p = QPainter(self)
        
        p.fillRect(e.rect(), QColor(36,50,64))
    
    
    
    
    
    def _onCurrentToolButtonClicked(self):
        
        
        
        if self._currentToolId is None:
            return
        
        self._currentActiveInkPanelIndex = 0
        
        self._toolsPopup.toggleVisible()
        self._inksPopup.popout()
    
    def _onCurrentPrimaryInkButtonClicked(self):
        
        
        
        if self._currentPrimaryInkId is None:
            return
        
        self._toolsPopup.popout()
        
        if self._currentActiveInkPanelIndex != 0 and self._currentActiveInkPanelIndex != 1:
            self._inksPopup.popout()
        
        last = self._currentActiveInkPanelIndex
        self._currentActiveInkPanelIndex = 1
        
        if last != self._currentActiveInkPanelIndex:
            
            self._inksPopup.popin()
            
        else:
            
            self._inksPopup.popout()
            self._currentActiveInkPanelIndex = 0
        
    
    def _onCurrentSecondaryInkButtonClicked(self):
        
        
        
        if self._currentSecondaryInkId is None:
            return
        
        self._toolsPopup.popout()
        
        if self._currentActiveInkPanelIndex != 0 and self._currentActiveInkPanelIndex != 2:
            self._inksPopup.popout()
        
        last = self._currentActiveInkPanelIndex
        self._currentActiveInkPanelIndex = 2
        
        if last != self._currentActiveInkPanelIndex:
            
            self._inksPopup.popin()
            
        else:
            
            self._inksPopup.popout()
            self._currentActiveInkPanelIndex = 0
        
        
    def _onToolSelected(self, tool):
        
        self.toolChanged.emit(tool.name())
        self._updateCurrentTool(tool.name())
        self._toolsPopup.popout()
        
    def _onInkSelected(self, slot, ink):
        
        if slot == 1:
            self.primaryInkChanged.emit(ink.name())
            self._updateCurrentPrimaryInk(ink.name())
            
        elif slot == 2:
            self.secondaryInkChanged.emit(ink.name())
            self._updateCurrentSecondaryInk(ink.name())
        
        self._inksPopup.popout()
    
    def _onPanelMouseEntered(self):
        
        self.mouseEntered.emit()
    
    def _onPanelMouseLeft(self):
        
        self.mouseLeft.emit()