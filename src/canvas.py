#-----------------------------------------------------------------------------------------------------------------------
# Name:        Canvas
# Purpose:     Represent a drawing transformable canvas where current sprite frame's pixels can be edited.
#
# Author:      Rafael Vasco
#
# Created:     30/03/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from src.canvas_mouse_state import CanvasMouseState

import src.utils as utils
from src.display import Display
from src.canvas_overlay import CanvasOverlay
from src import tools, inks
from src.toolbox import ToolBox
from src.tools import Tool

#-----------------------------------------------------------------------------------------------------------------------


class Canvas(Display):
    surfaceChanged = pyqtSignal()

    colorPicked = pyqtSignal(QColor, int)  # Color, Button Pressed
    toolStarted = pyqtSignal(Tool)
    toolEnded = pyqtSignal(Tool)

    def __init__(self, parent=None):

        super(Canvas, self).__init__(parent)

        self._tools = {}
        self._inks = {}

        self._sprite = None
        self._drawingSurface = None
        self._drawingSurfacePixelData = None
        self._currentTool = None
        self._lastTool = None
        self._primaryInk = None
        self._secondaryInk = None
        self._primaryColor = None
        self._secondaryColor = None
        self._pixelSize = 0
        self._drawGrid = True

        self._snap_enabled = True

        self._mouse_state = CanvasMouseState()

        # ======================================

        self._load_tools()
        self._load_inks()

        self._initialize_canvas_state()

        self._overlaySurface = CanvasOverlay(self)
        self._overlaySurface.disable()

        self._toolBox = ToolBox(self)
        self._toolBox.setVisible(False)
        self._initialize_toolbox()

        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)

        self.setAttribute(Qt.WA_NoSystemBackground)

    def current_tool(self):

        return self._currentTool

    def last_tool(self):

        return self._lastTool

    def primary_color(self):

        return self._primaryColor

    def tool_box(self):

        return self._toolBox

    def set_primary_color(self, color):

        self._primaryColor = color

    def secondary_color(self):

        return self._secondaryColor

    def set_secondary_color(self, color):

        self._secondaryColor = color

    def primary_ink(self):

        return self._primaryInk

    def set_primary_ink(self, ink_name):
        self._primaryInk = self.ink(ink_name)

    def secondary_ink(self):

        return self._secondaryInk

    def set_secondary_ink(self, ink_name):

        self._secondaryInk = self.ink(ink_name)

    def set_current_tool(self, name):

        self._lastTool = self._currentTool
        self._currentTool = self.tool(name)
        self.refresh()

    def tool(self, name):

        return self._tools[name]

    def ink(self, name):

        return self._inks[name]

    def pixel_size(self):

        return self._pixelSize

    def sprite_mouse_pos(self):

        return self._sprite_mouse_position

    def sprite_is_loaded(self):

        return self._sprite is not None

    def drawing_surface(self):

        return self._drawingSurface

    def drawing_surface_pixel_data(self):

        return self._drawingSurfacePixelData

    def mouse_state(self):

        return self._mouse_state

    # ----- PUBLIC API -------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def set_sprite(self, sprite):

        if self.sprite_is_loaded():
            self.unload_sprite()

        self._toolBox.setVisible(True)

        self._sprite = sprite

        super().set_object_size(sprite.current_animation().frame_width(),
                                sprite.current_animation().frame_height())

        self.refresh()

        self.setCursor(Qt.BlankCursor)

    def unload_sprite(self):

        self._toolBox.setVisible(False)

        self.reset_view()
        self.set_object_size(0, 0)

        self._sprite = None
        self._drawingSurface = None

        self.update()
        self.setCursor(Qt.ArrowCursor)

    def refresh(self):

        self._update_drawing_surface()

    def clear(self, index=None):

        if not self.sprite_is_loaded():
            return

        animation = self._sprite.current_animation()

        if index is None:
            surface = self._drawingSurface
        else:
            surface = animation.current_frame().surface_at(index).image()

        painter = QPainter()

        painter.begin(surface)

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(0, 0, surface.width(), surface.height(), Qt.white)

        painter.end()

        self.surfaceChanged.emit()

        self.update()

    def resize(self, width, height, index=None):

        pass

    def scale(self, sx, sy, index):

        pass

    # ----- EVENTS -----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    def on_draw_object(self, event, painter):

        if not self.sprite_is_loaded():
            return

        layers = self._sprite.current_animation().current_frame().surfaces()

        for layer in layers:
            painter.drawImage(0, 0, layer.image())

            # if self._drawGrid and self._zoom >= 16.0:
            #
            #     w = self._drawingSurface.width()
            #     h = self._drawingSurface.height()
            #
            #     painter.setPen(QColor(0, 0, 0, 80))
            #
            #     for x in range(0, w):
            #         #xz = x * self._pixelSize
            #         painter.drawLine(x, 0, x, h)
            #
            #     for y in range(0, h):
            #         #yz = y * self._pixelSize
            #         painter.drawLine(0, y, w, y)

    def resizeEvent(self, e):

        self._overlaySurface.resize(self.size())
        self._toolBox.resize(self.width(), self._toolBox.height())

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if not self.sprite_is_loaded() or self.is_panning():

            if self.is_panning():
                self._overlaySurface.disable()

            return

        self._update_mouse_state(e)

        tool = self._currentTool

        self.toolStarted.emit(tool)

        if tool.uses_painter():

            painter = QPainter()

            painter.begin(self._drawingSurface)

            tool.on_mouse_press(self, painter)

            painter.end()

        else:

            tool.on_mouse_press(self, None)

        self.update()

    def mouseMoveEvent(self, e):

        super().mouseMoveEvent(e)

        if not self.sprite_is_loaded():
            return

        self._update_mouse_state(e)

        tool = self._currentTool

        if not self._panning:

            if tool.uses_painter():
                painter = QPainter()

                painter.begin(self._drawingSurface)

                tool.on_mouse_move(self, painter)

                painter.end()

            else:

                tool.on_mouse_move(self, None)

        self.update()

    def mouseReleaseEvent(self, e):

        if not self.sprite_is_loaded():
            return

        self._update_mouse_state(e)

        tool = self._currentTool

        tool.on_mouse_release(self, None)

        self.update()

        self.toolEnded.emit(tool)

        super().mouseReleaseEvent(e)

        if not self.is_panning():
            self.setCursor(Qt.BlankCursor)
            self._overlaySurface.enable()

    def wheelEvent(self, e):

        if not self.sprite_is_loaded():
            return

        super().wheelEvent(e)

    def enterEvent(self, e):

        if not self.sprite_is_loaded():
            return

        self.setCursor(Qt.BlankCursor)
        self._overlaySurface.enable()

    def leaveEvent(self, e):

        if not self.sprite_is_loaded():
            return

        self.setCursor(Qt.ArrowCursor)

        self._overlaySurface.disable()

    def _on_toolbox_mouse_entered(self):

        if not self.sprite_is_loaded():
            return

        self._overlaySurface.disable()

    def _on_toolbox_mouse_left(self):

        if not self.sprite_is_loaded():
            return

        self._overlaySurface.enable()

    def _on_toolbox_tool_changed(self, tool_name):

        self.set_current_tool(tool_name)

    def _on_toolbox_primary_ink_changed(self, ink_name):

        self.set_primary_ink(ink_name)

    def _on_toolbox_secondary_ink_changed(self, ink_name):

        self.set_secondary_ink(ink_name)

    # ---- PRIVATE METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def _load_tools(self):

        # Default Tools

        self._tools['Pen'] = tools.Pen()
        self._tools['Picker'] = tools.Picker()
        self._tools['Filler'] = tools.Filler()

    def _load_inks(self):

        # Default Inks

        self._inks['Solid'] = inks.Solid()
        self._inks['Eraser'] = inks.Eraser()

    def _initialize_canvas_state(self):

        self._pixelSize = 1
        self._primaryColor = QColor('black')
        self._secondaryColor = QColor('white')
        self._currentTool = self.tool('Pen')
        self._primaryInk = self.ink('Solid')
        self._secondaryInk = self.ink('Eraser')

    def _initialize_toolbox(self):

        self._toolBox.mouseEntered.connect(self._on_toolbox_mouse_entered)
        self._toolBox.mouseLeft.connect(self._on_toolbox_mouse_left)

        self._toolBox.register_tool(self.tool('Pen'), is_default=True)
        self._toolBox.register_tool(self.tool('Picker'))
        self._toolBox.register_tool(self.tool('Filler'))

        self._toolBox.register_ink(self.ink('Solid'), slot=0)
        self._toolBox.register_ink(self.ink('Eraser'), slot=1)

        self._toolBox.toolChanged.connect(self._on_toolbox_tool_changed)
        self._toolBox.primaryInkChanged.connect(self._on_toolbox_primary_ink_changed)
        self._toolBox.secondaryInkChanged.connect(self._on_toolbox_secondary_ink_changed)

    def _update_mouse_state(self, e):

        if e.type() == QEvent.MouseButtonPress:

            self._mouse_state.set_mouse_pressing(True)

            if e.button() is not None:
                self._mouse_state.set_last_button_pressed(e.button())

        elif e.type() == QEvent.MouseButtonRelease:

            self._mouse_state.set_mouse_pressing(False)

        object_mouse_pos = super().object_mouse_pos()

        self._mouse_state.set_last_sprite_mouse_position(self._mouse_state.sprite_mouse_position())

        self._mouse_state.set_canvas_mouse_position(e.pos())

        if self._pixelSize > 1 and self._snap_enabled:
            self._mouse_state.set_sprite_mouse_position(utils.snap(object_mouse_pos, self._pixelSize))
        else:
            self._mouse_state.set_sprite_mouse_position(object_mouse_pos)

    def _update_drawing_surface(self):

        if not self.sprite_is_loaded():
            return

        self._drawingSurface = self._sprite.current_animation().current_frame().current_surface().image()

        self._drawingSurfacePixelData = self._drawingSurface.bits()

        self._drawingSurfacePixelData.setsize(self._drawingSurface.byteCount())

        self.update()
