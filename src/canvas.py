#-----------------------------------------------------------------------------------------------------------------------
# Name:        Canvas
# Purpose:     Represent a transformable canvas where a Sprite's pixels can be edited
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
        self._current_drawing_surface = None
        self._current_surface_pixel_data = None
        self._current_tool = None
        self._last_tool = None
        self._primary_ink = None
        self._secondary_ink = None
        self._primary_color = None
        self._secondary_color = None
        self._pixel_size = 0
        self._draw_grid = True
        self._snap_enabled = True
        self._mouse_state = CanvasMouseState()

        self._load_tools()
        self._load_inks()

        self._initialize_canvas_state()

        self._overlay_surface = CanvasOverlay(self)
        self._overlay_surface.disable()

        self._toolbox = ToolBox(self)
        self._toolbox.setVisible(False)
        self._initialize_toolbox()

        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)

        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAcceptDrops(True)

    def current_tool(self):

        return self._current_tool

    def last_tool(self):

        return self._last_tool

    def primary_color(self):

        return self._primary_color

    def tool_box(self):

        return self._toolbox

    def set_primary_color(self, color):

        self._primary_color = color

    def secondary_color(self):

        return self._secondary_color

    def set_secondary_color(self, color):

        self._secondary_color = color

    def primary_ink(self):

        return self._primary_ink

    def set_primary_ink(self, ink_name):
        self._primary_ink = self.ink(ink_name)

    def secondary_ink(self):

        return self._secondary_ink

    def set_secondary_ink(self, ink_name):

        self._secondary_ink = self.ink(ink_name)

    def set_current_tool(self, name):

        self._last_tool = self._current_tool
        self._current_tool = self.tool(name)
        self.refresh()

    def tool(self, name):

        return self._tools[name]

    def ink(self, name):

        return self._inks[name]

    def pixel_size(self):

        return self._pixel_size

    def sprite_is_set(self):

        return self._sprite is not None

    def current_drawing_surface(self):

        return self._current_drawing_surface

    def drawing_surface_pixel_data(self):

        return self._current_surface_pixel_data

    def mouse_state(self):

        return self._mouse_state

    # ----- PUBLIC API -------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def set_sprite(self, sprite):

        if self.sprite_is_set():
            self.unload_sprite()

        self._toolbox.setVisible(True)

        self._sprite = sprite

        super().set_object_size(sprite.width(), sprite.height())

        self.refresh()

        self.setCursor(Qt.BlankCursor)

    def unload_sprite(self):

        self._toolbox.setVisible(False)

        self.reset_view()
        self.set_object_size(0, 0)

        self._sprite = None
        self._current_drawing_surface = None

        self.update()
        self.setCursor(Qt.ArrowCursor)

    def refresh(self):

        self._update_drawing_surface()

        self.update()

    def clear(self, index=None):

        if not self.sprite_is_set():
            return

        animation = self._sprite.current_animation()

        if index is None:
            surface = self._current_drawing_surface
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

    def scale(self, scale_width, scale_height):

        pass

    # ----- EVENTS -----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def resizeEvent(self, e):

        self._overlay_surface.resize(self.size())
        self._toolbox.resize(self.width(), self._toolbox.height())

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if not self.sprite_is_set() or self.is_panning():

            if self.is_panning():
                self._overlay_surface.disable()

            return

        self._update_mouse_state(e)

        tool = self._current_tool

        self.toolStarted.emit(tool)

        if tool.uses_painter():

            painter = QPainter()

            painter.begin(self._current_drawing_surface)

            tool.on_mouse_press(self, painter, e)

            painter.end()

        else:

            tool.on_mouse_press(self, None, e)

        self.update()

    def mouseMoveEvent(self, e):

        super().mouseMoveEvent(e)

        if not self.sprite_is_set():
            return

        self._update_mouse_state(e)

        tool = self._current_tool

        if not self._panning:

            if tool.uses_painter():
                painter = QPainter()

                painter.begin(self._current_drawing_surface)

                tool.on_mouse_move(self, painter, e)

                painter.end()

            else:

                tool.on_mouse_move(self, None, e)

        self.update()

    def mouseReleaseEvent(self, e):

        if not self.sprite_is_set():
            return

        self._update_mouse_state(e)

        tool = self._current_tool

        tool.on_mouse_release(self, None, e)

        self.update()

        self.toolEnded.emit(tool)

        super().mouseReleaseEvent(e)

        if not self.is_panning():
            self.setCursor(Qt.BlankCursor)
            self._overlay_surface.enable()

    def wheelEvent(self, e):

        if not self.sprite_is_set():
            return

        super().wheelEvent(e)

    def enterEvent(self, e):

        if not self.sprite_is_set():
            return

        self.setCursor(Qt.BlankCursor)
        self._overlay_surface.enable()

    def leaveEvent(self, e):

        if not self.sprite_is_set():
            return

        self.setCursor(Qt.ArrowCursor)

        self._overlay_surface.disable()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):

        self.global_mouse_pos().setX(e.pos().x())
        self.global_mouse_pos().setY(e.pos().y())

        super(Canvas, self).dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():

            file_path = e.mimeData().urls()[0].toLocalFile()

            if utils.get_file_extension(file_path) == '.png':

                image = utils.load_image(file_path)

                self._update_mouse_state(e)

                self._sprite.paste_image(image)

                self.set_object_size(self._sprite.width(), self._sprite.height())

                self.refresh()

    def on_draw_object(self, event, painter):

        if not self.sprite_is_set():
            return

        layers = self._sprite.current_animation().current_frame().surfaces()

        for layer in layers:

            painter.setOpacity(layer.opacity())

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

    def _on_toolbox_mouse_entered(self):

        if not self.sprite_is_set():
            return

        self._overlay_surface.disable()

    def _on_toolbox_mouse_left(self):

        if not self.sprite_is_set():
            return

        self._overlay_surface.enable()

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

        self._pixel_size = 1
        self._primary_color = QColor('black')
        self._secondary_color = QColor('white')
        self._current_tool = self.tool('Pen')
        self._primary_ink = self.ink('Solid')
        self._secondary_ink = self.ink('Eraser')

    def _initialize_toolbox(self):

        self._toolbox.mouseEntered.connect(self._on_toolbox_mouse_entered)
        self._toolbox.mouseLeft.connect(self._on_toolbox_mouse_left)

        self._toolbox.register_tool(self.tool('Pen'), is_default=True)
        self._toolbox.register_tool(self.tool('Picker'))
        self._toolbox.register_tool(self.tool('Filler'))

        self._toolbox.register_ink(self.ink('Solid'), slot=0)
        self._toolbox.register_ink(self.ink('Eraser'), slot=1)

        self._toolbox.toolChanged.connect(self._on_toolbox_tool_changed)
        self._toolbox.primaryInkChanged.connect(self._on_toolbox_primary_ink_changed)
        self._toolbox.secondaryInkChanged.connect(self._on_toolbox_secondary_ink_changed)

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

        if self._pixel_size > 1 and self._snap_enabled:
            self._mouse_state.set_sprite_mouse_position(utils.snap(object_mouse_pos, self._pixel_size))
        else:
            self._mouse_state.set_sprite_mouse_position(object_mouse_pos)

    def _update_drawing_surface(self):

        if not self.sprite_is_set():
            return

        self._current_drawing_surface = self._sprite.active_surface()

        self._current_surface_pixel_data = self._current_drawing_surface.bits()

        self._current_surface_pixel_data.setsize(self._current_drawing_surface.byteCount())