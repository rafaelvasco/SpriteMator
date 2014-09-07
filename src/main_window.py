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

from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QDockWidget, QHBoxLayout
from src.pixel_size_widget import PixelSizeWidget

from src.toolbox import ToolBox
from ui.mainwindow_ui import Ui_MainWindow
from src.animation_display import AnimationDisplay
from src.canvas import Canvas
from src.color_picker import ColorPicker
from src.layer_manager import LayerManager
from src.new_sprite_dialog import NewSpriteDialog
from src.animation_manager import AnimationManager
from src.resources_cache import ResourcesCache
import src.appdata as app_data




# ----------------------------------------------------------------------------------------------------------------------


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)

        self._logo = QPixmap(':/images/logo')

        self._workspaceVisible = False

        self._pixelSizeWidget = PixelSizeWidget()

        self._colorPicker = ColorPicker()

        self._canvas = Canvas()

        self._canvas.primaryColor = self._colorPicker.primaryColor
        self._canvas.secondaryColor = self._colorPicker.secondaryColor

        self._toolbox = ToolBox()

        self._animationDisplay = AnimationDisplay()

        self._animationDisplayDock = QDockWidget()
        self._animationDisplayDock.setFeatures(QDockWidget.DockWidgetFloatable)
        self._animationDisplayDock.setWindowTitle("Animation Display")
        self._animationDisplayDock.setWidget(self._animationDisplay)

        self._animationManager = AnimationManager()

        self._layerManager = LayerManager()

        self._newSpriteDialog = NewSpriteDialog()
        self._newSpriteDialog.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # --------------------------------------------------------------------------------------------------------------

        self._initializeComponents()
        self._initializeLayout()
        self._initializeEvents()

        # --------------------------------------------------------------------------------------------------------------

        self.hideWorkspace()


    @property
    def canvas(self):
        return self._canvas

    @property
    def colorPicker(self):
        return self._colorPicker

    @property
    def layerManager(self):
        return self._layerManager

    @property
    def animationManager(self):
        return self._animationManager

    @property
    def toolBarWidget(self):
        return self.toolBar

    @property
    def newSpriteDialog(self):
        return self._newSpriteDialog

    @property
    def animationDisplay(self):
        return self._animationDisplay

    @property
    def toolBox(self):
        return self._toolbox

    def showWorkspace(self):

        self.centralWidget().setVisible(True)
        self._workspaceVisible = True

    def hideWorkspace(self):

        self.centralWidget().setVisible(False)
        self._workspaceVisible = False

    def paintEvent(self, e):

        if not self._workspaceVisible:
            p = QPainter(self)

            x = self.width() / 2 - self._logo.width() / 2
            y = self.height() / 2 - self._logo.height() / 2

            p.drawPixmap(x, y, self._logo)

            p.drawText(x + 50, y + 200, '.:: SpriteMator ::. | Version: %s' % app_data.meta['VERSION'])

    def eventFilter(self, target, event):

        if event.type() == QEvent.Wheel:

            if event.modifiers() & Qt.ControlModifier:

                if event.angleDelta().y() > 0:
                    self.colorPicker.selectNextColorOnPalette()
                elif event.angleDelta().y() < 0:
                    self.colorPicker.selectPrevColorOnPalette()

                return True

            elif event.modifiers() & Qt.AltModifier:

                if event.angleDelta().y() > 0:
                    self.colorPicker.selectNextRampOnPalette()
                elif event.angleDelta().y() < 0:
                    self.colorPicker.selectPrevRampOnPalette()

                return True

        return super(QMainWindow, self).eventFilter(target, event)


    def _initializeComponents(self):

        menufont = ResourcesCache.get('BigFont')

        self.actionNew.setFont(menufont)
        self.actionOpen.setFont(menufont)
        self.actionClose.setFont(menufont)
        self.actionExport.setFont(menufont)
        self.actionImport.setFont(menufont)
        self.actionQuit.setFont(menufont)
        self.actionSave.setFont(menufont)
        self.actionSaveAs.setFont(menufont)

        self._initializeToolbox()


    def _initializeLayout(self):

        # --------------------------------------------------------------------------------------------------------------

        canvaslayout = QVBoxLayout()
        canvaslayout.setContentsMargins(0, 0, 0, 0)

        canvaslayout.addWidget(self._toolbox)
        canvaslayout.addWidget(self._canvas)

        self.canvasFrame.setLayout(canvaslayout)

        # --------------------------------------------------------------------------------------------------------------

        color_picker_layout = QVBoxLayout()
        color_picker_layout.setContentsMargins(0, 0, 0, 0)

        color_picker_layout.addWidget(self._pixelSizeWidget)
        color_picker_layout.addWidget(self._colorPicker)

        self.colorPickerFrame.setLayout(color_picker_layout)

        # --------------------------------------------------------------------------------------------------------------

        animation_preview_layout = QVBoxLayout()
        animation_preview_layout.setContentsMargins(0, 0, 0, 0)
        animation_preview_layout.addWidget(self._animationDisplayDock)

        self.previewFrame.setLayout(animation_preview_layout)

        # --------------------------------------------------------------------------------------------------------------

        layer_manager_layout = QVBoxLayout()
        layer_manager_layout.setContentsMargins(0, 0, 0, 0)
        layer_manager_layout.addWidget(self._layerManager)

        self.layerListFrame.setLayout(layer_manager_layout)

        # --------------------------------------------------------------------------------------------------------------

        animation_bar_layout = QHBoxLayout()
        animation_bar_layout.setContentsMargins(0, 0, 0, 0)
        animation_bar_layout.addWidget(self._animationManager)
        animation_bar_layout.setAlignment(Qt.AlignLeft)

        self.animationBarFrame.setLayout(animation_bar_layout)

    def _initializeEvents(self):

        self._pixelSizeWidget.pixelSizeChanged.connect(self._onPixelSizeWidgetSizeChanged)

        self._colorPicker.primaryColorChanged.connect(self._onColorPickerPrimaryColorChanged)
        self._colorPicker.secondaryColorChanged.connect(self._onColorPickerSecondaryColorChanged)

        self._canvas.surfaceChanged.connect(self._onCanvasSurfaceChanged)
        self._canvas.viewportChanged.connect(self._onCanvasViewportChanged)
        self._canvas.colorPicked.connect(self._onCanvasColorPicked)
        self._canvas.toolStarted.connect(self._onCanvasToolStarted)
        self._canvas.toolEnded.connect(self._onCanvasToolEnded)

        self._toolbox.toolChanged.connect(self._onToolboxToolChanged)
        self._toolbox.primaryInkChanged.connect(self._onToolboxPrimaryInkChanged)
        self._toolbox.secondaryInkChanged.connect(self._onToolboxSecondaryInkChanged)

        self._animationManager.currentFrameChanged.connect(self._onCurrentFrameChanged)

        self._layerManager.currentLayerChanged.connect(self._onCurrentLayerChanged)
        self._layerManager.layerOrderChanged.connect(self._onLayerOrderChanged)
        self._layerManager.layerImported.connect(self._onLayerImported)

    def _initializeToolbox(self):

        self._toolbox.registerTool(self._canvas.findToolByName('Pen'), is_default=True)
        self._toolbox.registerTool(self._canvas.findToolByName('Picker'))
        self._toolbox.registerTool(self._canvas.findToolByName('Filler'))

        self._toolbox.registerInk(self._canvas.findInkByName('Solid'), slot=0)
        self._toolbox.registerInk(self._canvas.findInkByName('Eraser'), slot=1)


    # =================== Event Handlers ==============================

    # ------- Pixel Size Widget ---------------------------------------

    def _onPixelSizeWidgetSizeChanged(self, size):
        self._canvas.pixelSize = size

    # ------- Color Picker --------------------------------------------

    def _onColorPickerPrimaryColorChanged(self, color):

        self._canvas.primaryColor = color

    def _onColorPickerSecondaryColorChanged(self, color):

        self._canvas.secondaryColor = color

    # ------- Canvas ----------------------------------------------------------

    def _onCanvasSurfaceChanged(self):

        self._animationDisplay.refresh()

        self._layerManager.update()

        self._animationManager.update()

    def _onCanvasViewportChanged(self):

        self._animationDisplay.updateViewport()

        self._layerManager.update()

        self._animationManager.update()

    def _onCanvasColorPicked(self, color, button_pressed):

        if button_pressed == Qt.LeftButton:

            self._colorPicker.primaryColor = color

        elif button_pressed == Qt.RightButton:

            self._colorPicker.secondaryColor = color

    def _onCanvasToolStarted(self, tool):

        self._animationDisplay.startRefreshing()

    def _onCanvasToolEnded(self, tool):

        if tool.refreshWaitTime > 0:

            QTimer.singleShot(tool.refreshWaitTime, lambda: self._animationDisplay.stopRefreshing())

        else:
            self._animationDisplay.stopRefreshing()

        self._layerManager.update()
        self._animationManager.update()

    # ------ ToolBox ----------------------------------------------------------

    def _onToolboxToolChanged(self, tool_name):

        self._canvas.currentTool = tool_name

    def _onToolboxPrimaryInkChanged(self, ink_name):

        self._canvas.primaryInk = ink_name

    def _onToolboxSecondaryInkChanged(self, ink_name):

        self._canvas.secondaryInk = ink_name

    # ------ Frame Events------------------------------------------------------

    def _onCurrentFrameChanged(self, index):

        self._canvas.refresh()
        self._layerManager.refresh()
        self._animationDisplay.goToFrame(index)

    # ------- Layer Events ----------------------------------------------------

    def _onCurrentLayerChanged(self):

        self._canvas.refresh()

    def _onLayerOrderChanged(self):

        self._canvas.refresh()
        self._animationDisplay.refresh()
        self._animationManager.update()

    def _onLayerImported(self):

        self._canvas.updateViewport()
        self._animationDisplay.updateViewport()
