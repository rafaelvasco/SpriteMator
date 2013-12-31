#-----------------------------------------------------------------------------------------------------------------------
# Name:        MainWindow
# Purpose:     Represents the Application MainWindow and hosts all components inside it: Canvas, Animation Display etc.
#
# Author:      Rafael Vasco
#
# Created:     26/01/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt4.QtCore import Qt, QTimer
from PyQt4.QtGui import QMainWindow, QVBoxLayout, QDockWidget, QHBoxLayout

from ui.mainwindow_ui import Ui_MainWindow

from src.animation_display import AnimationDisplay
from src.canvas import Canvas
from src.color_picker import ColorPicker
from src.layer_list import LayerList
from src.new_sprite_dialog import NewSpriteDialog
from src.animation_manager import AnimationManager

from src.resources_cache import ResourcesCache

# ----------------------------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow, Ui_MainWindow):

    
    def __init__(self):

        QMainWindow.__init__(self)
        
        self.setupUi(self)
        
        
        
        self._colorPicker = ColorPicker()

        self._animationDisplay = AnimationDisplay()
        self._canvas = Canvas(self._animationDisplay)
        
        self._canvas.setPrimaryColor(self._colorPicker.primaryColor())
        self._canvas.setSecondaryColor(self._colorPicker.secondaryColor())

        self._animationDisplayDock = QDockWidget(self.previewFrame)

        self._animationDisplayDock.setFeatures(QDockWidget.DockWidgetFloatable)
        self._animationDisplayDock.setWindowTitle("Animation Display")
        self._animationDisplayDock.setWidget(self._animationDisplay)

        self._animationDisplayLastWidth = 0
        self._animationDisplayLastHeight = 0
        
        self._layerList = LayerList()
        
        self._animationManager = AnimationManager()
        
        self._newSpriteDialog  = NewSpriteDialog()

        # --------------------------------------------------------------------------------------------------------------
        
        self._initializeComponents()
        self._initializeLayout()
        self._initializeEvents()

        # --------------------------------------------------------------------------------------------------------------

    def canvas(self):
        return self._canvas

    def colorPicker(self):
        return self._colorPicker

    def layerList(self):
        return self._layerList
    
    def newSpriteDialog(self):
        return self._newSpriteDialog

    def animationDisplay(self):
        return self._animationDisplay
    
    def _initializeComponents(self):
        
        toolbarFont = ResourcesCache.get("DefaultFont")
        
        self.actionNew.setFont(toolbarFont)
        self.actionOpen.setFont(toolbarFont)
        self.actionClose.setFont(toolbarFont)
        self.actionExport.setFont(toolbarFont)
        self.actionImport.setFont(toolbarFont)
        self.actionQuit.setFont(toolbarFont)
        self.actionSave.setFont(toolbarFont)
        self.actionSaveAs.setFont(toolbarFont)
        
    def _initializeLayout(self):

        
        
        # --------------------------------------------------------------------------------------------------------------

        canvasLayout = QVBoxLayout()
        canvasLayout.setContentsMargins(0,0,0,0)
        
        canvasLayout.addWidget(self._canvas)

        self.canvasFrame.setLayout(canvasLayout)

        # --------------------------------------------------------------------------------------------------------------
        
        colorPickerLayout = QVBoxLayout()
        colorPickerLayout.setContentsMargins(0, 0, 0, 0)
        colorPickerLayout.addWidget(self._colorPicker)
        
        self.colorPickerFrame.setLayout(colorPickerLayout)
        
        # ---------------------------------------------------------------------------------------------------------------
        
        animationPreviewLayout = QVBoxLayout()
        animationPreviewLayout.setContentsMargins(0,0,0,0)
        animationPreviewLayout.addWidget(self._animationDisplayDock)
        
        self.previewFrame.setLayout(animationPreviewLayout)
        # --------------------------------------------------------------------------------------------------------------

        layerListLayout = QVBoxLayout()
        layerListLayout.setContentsMargins(0,0,0,0)
        layerListLayout.addWidget(self._layerList)
        
        self.layerListFrame.setLayout(layerListLayout)
        
        # --------------------------------------------------------------------------------------------------------------
        
        animationBarLayout = QHBoxLayout()
        animationBarLayout.setContentsMargins(0, 0, 0, 0)
        animationBarLayout.addWidget(self._animationManager)
        animationBarLayout.setAlignment(Qt.AlignLeft)
        
        self.animationBarFrame.setLayout(animationBarLayout)
        
        

    def _initializeEvents(self):

        self._colorPicker.primaryColorChanged.connect(self._onColorPickerPrimaryColorChanged)
        self._colorPicker.secondaryColorChanged.connect(self._onColorPickerSecondaryColorChanged)
        
        
        self._canvas.spriteChanged.connect(self._onCanvasSpriteChanged)
        self._canvas.animationAdded.connect(self._onCanvasAnimationAdded)
        self._canvas.animationChanged.connect(self._onCanvasAnimationChanged)
        self._canvas.frameChanged.connect(self._onCanvasFrameChanged)
        self._canvas.colorPicked.connect(self._onCanvasColorPicked)
        self._canvas.toolStarted.connect(self._onCanvasToolStarted)
        self._canvas.toolEnded.connect(self._onCanvasToolEnded)
        
        self._layerList.layerAdded.connect(self._onLayerListLayerAdded)
        self._layerList.layerSelected.connect(self._onLayerListLayerSelected)
        self._layerList.layerMoved.connect(self._onLayerListItemOrderChanged)

        self._animationManager.addClicked.connect(self._onAnimationManagerAddClicked)
        self._animationManager.removeClicked.connect(self._onAnimationManagerRemoveClicked)
        self._animationManager.animationIndexChanged.connect(self._onAnimationManagerIndexChanged)


    def _onColorPickerPrimaryColorChanged(self, color):

        self._canvas.setPrimaryColor(color)

    def _onColorPickerSecondaryColorChanged(self, color):

        self._canvas.setSecondaryColor(color)
    
    def _onCanvasColorPicked(self, color, event):
        
        if event.button() == Qt.LeftButton:
            
            self._colorPicker.setPrimaryColor(color)
        else:
            
            self._colorPicker.setSecondaryColor(color)
    
    def _onCanvasSpriteChanged(self, sprite):
        
        self._animationDisplay.setAnimation(sprite.currentAnimation())
    
    
    def _onCanvasAnimationAdded(self, animation, index):
        
        self._animationManager.addItem(animation.name(), index)
    
    def _onCanvasAnimationChanged(self, animation):
        
        self._animationDisplay.setAnimation(animation)
    
    def _onCanvasFrameChanged(self, frame):

        self._layerList.clear()

        layers = frame.surfaces()

        for layer in layers:

            self._layerList.addLayer(layer)
        
        self._layerList.setSelectedIndex(self._canvas.currentLayerIndex())

    def _onCanvasToolStarted(self, tool):
        
        self._animationDisplay._startRefreshing()
        self._layerList._startRefreshing()
    
    def _onCanvasToolEnded(self, tool):
        
        if tool.refreshWaitTime() > 0:
            
            QTimer.singleShot(tool.refreshWaitTime(), lambda : self._animationDisplay._stopRefreshing())
        
        else:
            
            self._animationDisplay._stopRefreshing()
            
        self._layerList._stopRefreshing()


    def _onLayerListLayerAdded(self):
        self._canvas.addLayer()

    def _onLayerListLayerSelected(self, index):
        self._canvas.setLayer(index)

    def _onLayerListItemOrderChanged(self, fromIndex, toIndex):
        self._canvas.moveLayer(fromIndex, toIndex)

        
    def _onAnimationManagerAddClicked(self):
        self._canvas.addAnimation()
    
    def _onAnimationManagerRemoveClicked(self, index):
        print('Removed ' , index)
        
    def _onAnimationManagerIndexChanged(self, index):
        
        self._canvas.setAnimation(index)
