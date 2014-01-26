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
from PyQt4.QtGui import QMainWindow, QVBoxLayout, QDockWidget, QHBoxLayout, QPixmap, QPainter

from ui.mainwindow_ui import Ui_MainWindow

from src.animation_display import AnimationDisplay
from src.canvas import Canvas
from src.color_picker import ColorPicker
from src.layer_manager import LayerManager
from src.new_sprite_dialog import NewSpriteDialog
from src.animation_manager import AnimationManager

from src.resources_cache import ResourcesCache

import src.appdata as appdata


# ----------------------------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow, Ui_MainWindow):

    
    def __init__(self):

        QMainWindow.__init__(self)
        
        self.setupUi(self)
        
        self._logo = QPixmap(':/images/logo')
        
        self._workspaceVisible = False
        
        self._colorPicker = ColorPicker()
        
        self._canvas = Canvas()
        
        self._animationDisplay = AnimationDisplay()
        
        self._canvas.setPrimaryColor(self._colorPicker.primaryColor())
        self._canvas.setSecondaryColor(self._colorPicker.secondaryColor())

        self._animationDisplayDock = QDockWidget(self.previewFrame)

        self._animationDisplayDock.setFeatures(QDockWidget.DockWidgetFloatable)
        self._animationDisplayDock.setWindowTitle("Animation Display")
        self._animationDisplayDock.setWidget(self._animationDisplay)

        self._animationDisplayLastWidth = 0
        self._animationDisplayLastHeight = 0
        
       
        self._animationManager = AnimationManager()
       
        self._layerManager = LayerManager()
        
        self._newSpriteDialog  = NewSpriteDialog()
        
        
        # --------------------------------------------------------------------------------------------------------------
        
        self._initializeComponents()
        self._initializeLayout()
        self._initializeEvents()
        
        # --------------------------------------------------------------------------------------------------------------

        self.hideWorkspace()

    def canvas(self):
        return self._canvas

    def colorPicker(self):
        return self._colorPicker

    def layerManager(self):
        return self._layerManager
    
    def animationManager(self):
        
        return self._animationManager
    
    def topMenu(self):
        
        return self.toolBar
    
    def newSpriteDialog(self):
        return self._newSpriteDialog

    def animationDisplay(self):
        return self._animationDisplay
    
    
    def showWorkspace(self):
        
        self.centralWidget().setVisible(True)
        self._workspaceVisible = True
        
    def hideWorkspace(self):
        
        self.centralWidget().setVisible(False)
        self._workspaceVisible = False
    
    def closeEvent(self, e):
        
        self._canvas.unloadSprite()
        self._animationManager.clear()
        self._layerManager.clear()
        
        QMainWindow.closeEvent(self, e)
        
        
    def paintEvent(self, e):
        
        if not self._workspaceVisible:
            
            p = QPainter(self)
            
            x = self.width() / 2 - self._logo.width() / 2
            y = self.height() / 2 - self._logo.height() / 2
            
            p.drawPixmap(x, y, self._logo)
            
            p.drawText(x + 50, y + 200, '.:: SpriteMator ::. | Version: %s' % appdata.meta['VERSION'])
    
    def resizeEvent(self, e):
        
        self.rightPanel.setMaximumWidth(round(0.37 * e.size().width()))
        
    
    def _initializeComponents(self):
        
        menuFont = ResourcesCache.get('BigFont')
        
        self.actionNew.setFont(menuFont)
        self.actionOpen.setFont(menuFont)
        self.actionClose.setFont(menuFont)
        self.actionExport.setFont(menuFont)
        self.actionImport.setFont(menuFont)
        self.actionQuit.setFont(menuFont)
        self.actionSave.setFont(menuFont)
        self.actionSaveAs.setFont(menuFont)
        
        
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

        layerManagerLayout = QVBoxLayout()
        layerManagerLayout.setContentsMargins(0,0,0,0)
        layerManagerLayout.addWidget(self._layerManager)
        
        self.layerListFrame.setLayout(layerManagerLayout)
        
        # --------------------------------------------------------------------------------------------------------------
        
        animationBarLayout = QHBoxLayout()
        animationBarLayout.setContentsMargins(0, 0, 0, 0)
        animationBarLayout.addWidget(self._animationManager)
        animationBarLayout.setAlignment(Qt.AlignLeft)
        
        self.animationBarFrame.setLayout(animationBarLayout)
        
        

    def _initializeEvents(self):

        self._colorPicker.primaryColorChanged.connect(self._onColorPickerPrimaryColorChanged)
        self._colorPicker.secondaryColorChanged.connect(self._onColorPickerSecondaryColorChanged)
        
        
        self._canvas.surfaceChanged.connect(self._onCanvasSurfaceChanged)
        self._canvas.colorPicked.connect(self._onCanvasColorPicked)
        self._canvas.toolStarted.connect(self._onCanvasToolStarted)
        self._canvas.toolEnded.connect(self._onCanvasToolEnded)
        
        self._animationManager.animationSelectedChanged.connect(self._onAnimationManagerAnimationSelectedChanged)
        self._animationManager.frameSelectedChanged.connect(self._onAnimationManagerFrameSelectedChanged)
        
        self._layerManager.layerSelectedChanged.connect(self._onLayerManagerLayerSelectedChanged)
        self._layerManager.layerOrderChanged.connect(self._onLayerManagerLayerOrderChanged)
        self._layerManager.layerListChanged.connect(self._onLayerManagerLayerListChanged)
        
    
    
    
    # =================== Event Handlers ==============================
    
    def _onColorPickerPrimaryColorChanged(self, color):

        self._canvas.setPrimaryColor(color)

    def _onColorPickerSecondaryColorChanged(self, color):

        self._canvas.setSecondaryColor(color)
    
    
    # ------- Canvas ------------------------------------------------
    
    def _onCanvasSurfaceChanged(self):
        
        self._animationDisplay.update()
        
        self._layerManager.update()
        
        self._animationManager.update()
    
    def _onCanvasColorPicked(self, color, event):
        
        if event.button() == Qt.LeftButton:
            
            self._colorPicker.setPrimaryColor(color)
        else:
            
            self._colorPicker.setSecondaryColor(color)

    def _onCanvasToolStarted(self, tool):
        
        self._animationDisplay._startRefreshing()
        self._layerManager._startRefreshing()
        self._animationManager._startRefreshing()
    
    def _onCanvasToolEnded(self, tool):
        
        if tool.refreshWaitTime() > 0:
            
            QTimer.singleShot(tool.refreshWaitTime(), lambda : self._animationDisplay._stopRefreshing())
        
        else:
            
            self._animationDisplay._stopRefreshing()
            
        self._layerManager._stopRefreshing()
        self._animationManager._stopRefreshing()
        
        
        
    # ------ Animation Manager ------------------------------------------
    
    def _onAnimationManagerAnimationSelectedChanged(self, animation):
        
        self._canvas.refresh()
        self._layerManager.refresh()
        
        self._animationDisplay.update()
        self._animationDisplay.setAnimation(animation)
    
        
    def _onAnimationManagerFrameSelectedChanged(self, index):
        
        self._canvas.refresh()
        self._layerManager.refresh()
        
        self._animationDisplay.update()
        self._animationDisplay.goToFrame(index)
        
    
        
    
    # ------- Layer Manager ----------------------------------------------
    
    def _onLayerManagerLayerSelectedChanged(self):
        
        self._canvas.refresh()
    
    def _onLayerManagerLayerOrderChanged(self):
    
        self._canvas.refresh()
        self._animationDisplay.update()
        self._animationManager.update()
    
    def _onLayerManagerLayerListChanged(self):
        
        self._canvas.refresh()
        self._animationDisplay.update()
        self._animationManager.update()