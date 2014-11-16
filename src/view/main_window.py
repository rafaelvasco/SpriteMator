# --------------------------------------------------------------------------------------------------
# Name:        MainWindow
# Purpose:     Represents the Application MainWindow and hosts all components inside it:
#              Canvas, Animation Display etc.
# Author:      Rafael Vasco
#
# Created:     26/01/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QDockWidget, QHBoxLayout
from src.view.options_bar_widget import OptionsBar

from src.view.pixel_size_widget import PixelSizeWidget
from src.view.toolbar_widget import ToolBar
from ui.mainwindow_ui import Ui_MainWindow
from src.view.animation_display_widget import AnimationDisplay
from src.view.canvas_widget import Canvas
from src.view.color_picker_widget import ColorPicker
from src.view.layer_manager_widget import LayerManager
from src.view.new_sprite_dialog import NewSpriteDialog
from src.view.animation_manager_widget import AnimationManager
from src.model.resources_cache import ResourcesCache
import src.model.appdata as app_data


# -------------------------------------------------------------------------------------------------


class MainWindow(QMainWindow, Ui_MainWindow):

    closed = pyqtSignal()

    def __init__(self):

        QMainWindow.__init__(self)

        self.setupUi(self)

        self._logo = QPixmap(':/images/logo')

        self._workspaceVisible = False

        self._pixelSizeWidget = PixelSizeWidget()

        self._colorPicker = ColorPicker()

        self._canvas = Canvas()

        self._canvas.primary_color = self._colorPicker.primary_color
        self._canvas.secondary_color = self._colorPicker.secondary_color

        self._toolbar = ToolBar()

        self._optionsBar = OptionsBar()

        self._animationDisplay = AnimationDisplay()

        self._animationDisplayDock = QDockWidget()
        self._animationDisplayDock.setFeatures(QDockWidget.DockWidgetFloatable)
        self._animationDisplayDock.setWindowTitle("Animation Display")
        self._animationDisplayDock.setWidget(self._animationDisplay)

        self._animationManager = AnimationManager()

        self._layerManager = LayerManager()

        self._newSpriteDialog = NewSpriteDialog()
        self._newSpriteDialog.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # -----------------------------------------------------------------------------------------

        self._init_components()
        self._init_layout()
        self._init_events()

        # -----------------------------------------------------------------------------------------

        self.hide_workspace()

    @property
    def canvas(self):
        return self._canvas

    @property
    def color_picker(self):
        return self._colorPicker

    @property
    def layer_manager(self):
        return self._layerManager

    @property
    def animation_manager(self):
        return self._animationManager

    @property
    def toolbar_widget(self):
        return self.toolBar

    @property
    def new_sprite_dialog(self):
        return self._newSpriteDialog

    @property
    def animation_display(self):
        return self._animationDisplay

    @property
    def tool_box(self):
        return self._toolbar

    def show_workspace(self):

        self.centralWidget().setVisible(True)
        self._workspaceVisible = True

    def hide_workspace(self):

        self.centralWidget().setVisible(False)
        self._workspaceVisible = False

    def paintEvent(self, e):

        if not self._workspaceVisible:
            p = QPainter(self)

            x = self.width() / 2 - self._logo.width() / 2
            y = self.height() / 2 - self._logo.height() / 2

            p.drawPixmap(x, y, self._logo)

            p.drawText(x + 50, y + 200,
                       '.:: SpriteMator ::. | Version: %s' % app_data.meta['VERSION'])

    def eventFilter(self, target, event):

        if event.type() == QEvent.Wheel:

            if event.modifiers() & Qt.ControlModifier:

                if event.angleDelta().y() > 0:
                    self.color_picker.select_next_color_on_palette()
                elif event.angleDelta().y() < 0:
                    self.color_picker.select_previous_color_on_palette()

                return True

            elif event.modifiers() & Qt.AltModifier:

                if event.angleDelta().y() > 0:
                    self.color_picker.select_next_ramp_on_palette()
                elif event.angleDelta().y() < 0:
                    self.color_picker.select_previous_ramp_on_palette()

                return True

        return super(QMainWindow, self).eventFilter(target, event)

    def closeEvent(self, e):

        self.closed.emit()

        super(QMainWindow, self).closeEvent(e)

    def _init_components(self):

        menufont = ResourcesCache.get('BigFont')

        self.actionNew.setFont(menufont)
        self.actionOpen.setFont(menufont)
        self.actionClose.setFont(menufont)
        self.actionExport.setFont(menufont)
        self.actionImport.setFont(menufont)
        self.actionQuit.setFont(menufont)
        self.actionSave.setFont(menufont)
        self.actionSaveAs.setFont(menufont)

        self._init_toolbox()

    def _init_layout(self):

        # -----------------------------------------------------------------------------------------

        canvaslayout = QVBoxLayout()
        canvaslayout.setContentsMargins(0, 0, 0, 0)

        canvaslayout.addWidget(self._toolbar)
        canvaslayout.addWidget(self._canvas)
        canvaslayout.addWidget(self._optionsBar)

        self.canvasFrame.setLayout(canvaslayout)

        # -----------------------------------------------------------------------------------------

        color_picker_layout = QVBoxLayout()
        color_picker_layout.setContentsMargins(0, 0, 0, 0)

        color_picker_layout.addWidget(self._pixelSizeWidget)
        color_picker_layout.addWidget(self._colorPicker)

        self.colorPickerFrame.setLayout(color_picker_layout)

        # -----------------------------------------------------------------------------------------

        animation_preview_layout = QVBoxLayout()
        animation_preview_layout.setContentsMargins(0, 0, 0, 0)
        animation_preview_layout.addWidget(self._animationDisplayDock)

        self.previewFrame.setLayout(animation_preview_layout)

        # -----------------------------------------------------------------------------------------

        layer_manager_layout = QVBoxLayout()
        layer_manager_layout.setContentsMargins(0, 0, 0, 0)
        layer_manager_layout.addWidget(self._layerManager)

        self.layerListFrame.setLayout(layer_manager_layout)

        # -----------------------------------------------------------------------------------------

        animation_bar_layout = QHBoxLayout()
        animation_bar_layout.setContentsMargins(0, 0, 0, 0)
        animation_bar_layout.addWidget(self._animationManager)
        animation_bar_layout.setAlignment(Qt.AlignLeft)

        self.animationBarFrame.setLayout(animation_bar_layout)

    def _init_events(self):

        self._pixelSizeWidget.pixelSizeChanged.connect(self._on_pixel_size_changed)

        self._colorPicker.primaryColorChanged.connect(self._on_primary_color_changed)
        self._colorPicker.secondaryColorChanged.connect(self._on_secondary_color_changed)

        self._canvas.surfaceChanged.connect(self._on_canvas_surface_changed)
        self._canvas.surfaceChanging.connect(self._on_canvas_surface_changing)
        self._canvas.viewportChanged.connect(self._on_canvas_viewport_changed)
        self._canvas.colorPicked.connect(self._on_canvas_color_picked)

        self._toolbar.toolChanged.connect(self._on_tool_changed)
        self._toolbar.primaryInkChanged.connect(self._on_primary_ink_changed)
        self._toolbar.secondaryInkChanged.connect(self._on_secondary_ink_changed)

        self._animationManager.currentFrameChanged.connect(self._on_current_frame_changed)

        self._layerManager.currentLayerChanged.connect(self._on_current_layer_changed)
        self._layerManager.layerOrderChanged.connect(self._on_layer_order_changed)
        self._layerManager.layerImported.connect(self._on_layer_imported)

    def _init_toolbox(self):

        self._toolbar.register_tool(self._canvas.find_tool_by_name('Pen'), is_default=True)
        self._toolbar.register_tool(self._canvas.find_tool_by_name('Picker'))
        self._toolbar.register_tool(self._canvas.find_tool_by_name('Filler'))
        self._toolbar.register_tool(self._canvas.find_tool_by_name('Manipulator'))

        self._toolbar.register_ink(self._canvas.find_ink_by_name('Solid'), slot=0)
        self._toolbar.register_ink(self._canvas.find_ink_by_name('Eraser'), slot=1)

    # =================== Event Handlers ==============================

    # ------- Pixel Size Widget ---------------------------------------

    def _on_pixel_size_changed(self, size):
        self._canvas.pixel_size = size

    # ------- Color Picker --------------------------------------------

    def _on_primary_color_changed(self, color):
        self._canvas.primary_color = color

    def _on_secondary_color_changed(self, color):
        self._canvas.secondary_color = color

    # ------- Canvas ----------------------------------------------------------

    def _on_canvas_surface_changed(self):

        self._animationDisplay.update()
        self._animationManager.update()
        self._layerManager.update()

    def _on_canvas_surface_changing(self):

        self._animationDisplay.update()

    def _on_canvas_viewport_changed(self):

        self._animationDisplay.update_viewport()

        self._layerManager.update()

        self._animationManager.update()

    def _on_canvas_color_picked(self, color, button_pressed):

        if button_pressed == Qt.LeftButton:

            self._colorPicker.primary_color = color

        elif button_pressed == Qt.RightButton:

            self._colorPicker.secondary_color = color

    # ------ ToolBar ----------------------------------------------------------

    def _on_tool_changed(self, tool_name):

        self._canvas.current_tool = tool_name
        self._canvas.update()

    def _on_primary_ink_changed(self, ink_name):

        self._canvas.primary_ink = self._canvas.find_ink_by_name(ink_name)

    def _on_secondary_ink_changed(self, ink_name):

        self._canvas.secondary_ink = self._canvas.find_ink_by_name(ink_name)

    # ------ Frame Events------------------------------------------------------

    def _on_current_frame_changed(self, index):

        self._canvas.update()
        self._layerManager.rebuild()
        self._animationDisplay.go_to_frame(index)

    # ------- Layer Events ----------------------------------------------------

    def _on_current_layer_changed(self):

        self._canvas.update()

    def _on_layer_order_changed(self):

        self._canvas.update()
        self._animationDisplay.update()
        self._animationManager.update()

    def _on_layer_imported(self):

        self._canvas.update_viewport()
        self._animationDisplay.update_viewport()
