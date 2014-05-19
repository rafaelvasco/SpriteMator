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

        self._colorPicker = ColorPicker()

        self._canvas = Canvas()

        self._animationDisplay = AnimationDisplay()

        self._canvas.set_primary_color(self._colorPicker.primary_color())
        self._canvas.set_secondary_color(self._colorPicker.secondary_color())

        self._animationDisplayDock = QDockWidget(self.previewFrame)

        self._animationDisplayDock.setFeatures(QDockWidget.DockWidgetFloatable)

        self._animationDisplayDock.setWindowTitle("Animation Display")

        self._animationDisplayDock.setWidget(self._animationDisplay)

        self._animationDisplayLastWidth = 0

        self._animationDisplayLastHeight = 0

        self._animationManager = AnimationManager()

        self._layerManager = LayerManager()

        self._newSpriteDialog = NewSpriteDialog()

        # --------------------------------------------------------------------------------------------------------------

        self._initialize_components()
        self._initialize_layout()
        self._initialize_events()

        # --------------------------------------------------------------------------------------------------------------

        self.hide_workspace()

    def canvas(self):
        return self._canvas

    def color_picker(self):
        return self._colorPicker

    def layer_manager(self):
        return self._layerManager

    def animation_manager(self):

        return self._animationManager

    def top_menu(self):

        return self.toolBar

    def new_sprite_dialog(self):
        return self._newSpriteDialog

    def animation_display(self):
        return self._animationDisplay

    def show_workspace(self):

        self.centralWidget().setVisible(True)
        self._workspaceVisible = True

    def hide_workspace(self):

        self.centralWidget().setVisible(False)
        self._workspaceVisible = False

    def closeEvent(self, e):

        self._canvas.unload_sprite()
        self._animationManager.clear()
        self._layerManager.clear()

        QMainWindow.closeEvent(self, e)

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
                    self.color_picker().select_next_color_on_palette()
                elif event.angleDelta().y() < 0:
                    self.color_picker().select_previous_color_on_palette()

                return True

            elif event.modifiers() & Qt.AltModifier:

                if event.angleDelta().y() > 0:
                    self.color_picker().select_next_ramp_on_palette()
                elif event.angleDelta().y() < 0:
                    self.color_picker().select_previous_ramp_on_palette()

                return True

        return super(QMainWindow, self).eventFilter(target, event)

    def resizeEvent(self, e):

        self.rightPanel.setMaximumWidth(round(0.37 * e.size().width()))

    def _initialize_components(self):

        menufont = ResourcesCache.get('BigFont')

        self.actionNew.setFont(menufont)
        self.actionOpen.setFont(menufont)
        self.actionClose.setFont(menufont)
        self.actionExport.setFont(menufont)
        self.actionImport.setFont(menufont)
        self.actionQuit.setFont(menufont)
        self.actionSave.setFont(menufont)
        self.actionSaveAs.setFont(menufont)

    def _initialize_layout(self):

        # --------------------------------------------------------------------------------------------------------------

        canvaslayout = QVBoxLayout()
        canvaslayout.setContentsMargins(0, 0, 0, 0)

        canvaslayout.addWidget(self._canvas)

        self.canvasFrame.setLayout(canvaslayout)

        # --------------------------------------------------------------------------------------------------------------

        color_picker_layout = QVBoxLayout()
        color_picker_layout.setContentsMargins(0, 0, 0, 0)
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

    def _initialize_events(self):

        self._colorPicker.primaryColorChanged.connect(self._on_colorpicker_primary_color_changed)
        self._colorPicker.secondaryColorChanged.connect(self._on_colorpicker_secondary_color_changed)

        self._canvas.surfaceChanged.connect(self._on_canvas_surface_changed)
        self._canvas.colorPicked.connect(self._on_canvas_color_picked)
        self._canvas.toolStarted.connect(self._on_canvas_tool_started)
        self._canvas.toolEnded.connect(self._on_canvas_tool_ended)

        self._animationManager.animationSelectedChanged.connect(self._on_animation_manager_animation_selected_changed)
        self._animationManager.frameSelectedChanged.connect(self._on_animation_manager_frame_selected_changed)

        self._layerManager.layerSelectedChanged.connect(self._on_layer_manager_layer_selected_changed)
        self._layerManager.layerOrderChanged.connect(self._on_layer_manager_layer_order_changed)
        self._layerManager.layerListChanged.connect(self._on_layer_manager_layer_list_changed)

    # =================== Event Handlers ==============================

    # ------- Color Picker -----------------------------------------

    def _on_colorpicker_primary_color_changed(self, color):

        self._canvas.set_primary_color(color)

    def _on_colorpicker_secondary_color_changed(self, color):

        self._canvas.set_secondary_color(color)

    # ------- Canvas ------------------------------------------------

    def _on_canvas_surface_changed(self):
        self._animationDisplay.update()

        self._layerManager.update()

        self._animationManager.update()

    def _on_canvas_color_picked(self, color, button_pressed):

        if button_pressed == Qt.LeftButton:

            self._colorPicker.set_primary_color(color)

        elif button_pressed == Qt.RightButton:

            self._colorPicker.set_secondary_color(color)

    def _on_canvas_tool_started(self, tool):

        self._animationDisplay.start_refreshing()
        self._layerManager.start_refreshing()
        self._animationManager.start_refreshing()

    def _on_canvas_tool_ended(self, tool):

        if tool.refresh_wait_time() > 0:

            QTimer.singleShot(tool.refresh_wait_time(), lambda: self._animationDisplay.stop_refreshing())

        else:

            self._animationDisplay.stop_refreshing()

        self._layerManager.stop_refreshing()
        self._animationManager.stop_refreshing()

    # ------ Animation Manager ------------------------------------------

    def _on_animation_manager_animation_selected_changed(self, animation):

        self._canvas.refresh()
        self._layerManager.refresh()

        self._animationDisplay.update()
        self._animationDisplay.set_animation(animation)

    def _on_animation_manager_frame_selected_changed(self, index):

        self._canvas.refresh()
        self._layerManager.refresh()

        self._animationDisplay.update()
        self._animationDisplay.go_to_frame(index)

    # ------- Layer Manager ----------------------------------------------

    def _on_layer_manager_layer_selected_changed(self):

        self._canvas.refresh()

    def _on_layer_manager_layer_order_changed(self):

        self._canvas.refresh()
        self._animationDisplay.update()
        self._animationManager.update()

    def _on_layer_manager_layer_list_changed(self):

        self._canvas.refresh()
        self._animationDisplay.update()
        self._animationManager.update()