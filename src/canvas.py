# ------------------------------------------------------------------------------
# Name:        Canvas
# Purpose:     The Canvas is a Display in which the DisplaySpriteItem's pixels
#              can be edited
# Author:      Rafael Vasco
#
# Created:     30/03/2013
# Copyright:   (c) Rafael Vasco 2014
# Licence:     <your licence>
#------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QColor, QPainter
from src.canvas_overlay import CanvasOverlay

from src.display import Display
import src.utils as utils
from src import tools, inks
from src.tools import Tool

#------------------------------------------------------------------------------


class CanvasMouseState(object):
    def __init__(self):
        self._spritePos = QPoint()
        self._lastSpritePos = QPoint()
        self._canvasPos = QPoint()
        self._globalPos = QPoint()
        self._lastCanvasPos = QPoint()
        self._pressedButton = None
        self._isCtrlPressed = False
        self._isAltPressed = False
        self._isShiftPressed = False

    @property
    def sprite_pos(self):
        return self._spritePos

    @sprite_pos.setter
    def sprite_pos(self, value):
        self._spritePos = value

    @property
    def last_sprite_pos(self):
        return self._lastSpritePos

    @last_sprite_pos.setter
    def last_sprite_pos(self, value):
        self._lastSpritePos = value

    @property
    def canvas_pos(self):
        return self._canvasPos

    @canvas_pos.setter
    def canvas_pos(self, value):
        self._canvasPos = value

    @property
    def last_canvas_pos(self):
        return self._lastCanvasPos

    @last_canvas_pos.setter
    def last_canvas_pos(self, value):
        self._lastCanvasPos = value

    @property
    def global_pos(self):
        return self._globalPos

    @global_pos.setter
    def global_pos(self, value):
        self._globalPos = value


    @property
    def pressed_button(self):
        return self._pressedButton

    @pressed_button.setter
    def pressed_button(self, value):
        self._pressedButton = value


class Canvas(Display):
    surfaceChanged = pyqtSignal()
    viewportChanged = pyqtSignal()
    colorPicked = pyqtSignal(QColor, int)  # Color, Button Pressed
    toolStarted = pyqtSignal(Tool)
    toolEnded = pyqtSignal(Tool)

    def __init__(self):

        super(Canvas, self).__init__()

        self._overlay = CanvasOverlay(self)

        self.turn_backlight_on()

        self._tools = {}

        self._inks = {}

        self._currentTool = None

        self._lastTool = None

        self._primaryInk = None

        self._secondaryInk = None

        self._primaryColor = None

        self._secondaryColor = None

        self._pixelSize = 0

        self._isOnDragDrop = False

        self._drawGrid = True

        self._snapEnabled = True

        self._mouseState = CanvasMouseState()

        self._load_tools()

        self._load_inks()

        self._init_canvas_state()

        self.setAcceptDrops(True)

    @property
    def sprite_object(self):
        return self._spriteObject

    @property
    def current_tool(self):
        return self._currentTool

    @current_tool.setter
    def current_tool(self, value):
        self._lastTool = self._currentTool
        self._currentTool = self.find_tool_by_name(value)


    @property
    def last_tool(self):
        return self._lastTool

    @property
    def tools(self):
        return self._tools.items()

    @property
    def inks(self):
        return self._inks.items()

    @property
    def primary_color(self):
        return self._primaryColor

    @primary_color.setter
    def primary_color(self, value):
        self._primaryColor = value

    @property
    def secondary_color(self):
        return self._secondaryColor

    @secondary_color.setter
    def secondary_color(self, value):
        self._secondaryColor = value

    @property
    def primary_ink(self):
        return self._primaryInk

    @primary_ink.setter
    def primary_ink(self, value):
        self._primaryInk = value

    @property
    def secondary_ink(self):
        return self._secondaryInk

    @secondary_ink.setter
    def secondary_ink(self, value):
        self._secondaryInk = value

    @property
    def pixel_size(self):
        return self._pixelSize

    @pixel_size.setter
    def pixel_size(self, value):
        self._pixelSize = value

    @property
    def mouse_state(self):
        return self._mouseState

    def find_tool_by_name(self, name):

        return self._tools[name]

    def find_ink_by_name(self, name):

        return self._inks[name]

    def sprite_is_set(self):

        return self._spriteObject.sprite is not None

    # -------------------------------------------------------------------------

    def set_sprite(self, sprite):

        if self.sprite_is_set():
            self.unload_sprite()

        self._spriteObject.set_sprite(sprite)

        self.update_viewport()

    def clear(self):

        if self._spriteObject is None:
            return

        surface = self._spriteObject.active_surface

        painter = QPainter()

        painter.begin(surface)

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(0, 0, surface.width(), surface.height(), Qt.white)

        painter.end()

        self.update()

        self.surfaceChanged.emit()

        self.update()

    def resize(self, width, height, index=None):
        pass

    def rescale(self, scale_width, scale_height):
        pass

    # -------------------------------------------------------------------------

    def resizeEvent(self, e):

        super(Canvas, self).resizeEvent(e)

        self._overlay.setGeometry(QRect(0, 0, self.width(), self.height()))

    def mousePressEvent(self, e):

        super(Canvas, self).mousePressEvent(e)

        if self.is_panning:
            self._overlay.disable()
            return

        self._mouseState.canvas_pos = self.mapToScene(e.pos())

        self._mouseState.sprite_pos.setX(
            self._mouseState.canvas_pos.x() - self._spriteObject.boundingRect().left())
        self._mouseState.sprite_pos.setY(
            self._mouseState.canvas_pos.y() - self._spriteObject.boundingRect().top())

        self._mouseState.pressed_button = e.button()

        self.toolStarted.emit(self._currentTool)

        if self._pixelSize > 1 and self._snapEnabled:
            self._mouseState.sprite_pos = utils.snap_point(self._mouseState.sprite_pos,
                                                           self._pixelSize)

        self._mouseState.last_canvas_pos.setX(self._mouseState.canvas_pos.x())
        self._mouseState.last_canvas_pos.setY(self._mouseState.canvas_pos.y())

        self._mouseState.last_sprite_pos.setX(self._mouseState.sprite_pos.x())
        self._mouseState.last_sprite_pos.setY(self._mouseState.sprite_pos.y())

        self._currentTool.on_mouse_press(self)

        self.update()

    def mouseMoveEvent(self, e):

        super(Canvas, self).mouseMoveEvent(e)

        self.mouse_state.global_pos.setX(e.pos().x())
        self.mouse_state.global_pos.setY(e.pos().y())

        if not self.sprite_is_set() or self.is_panning:
            return

        canvas_pos = self._mouseState.canvas_pos = self.mapToScene(e.pos())

        self._mouseState.sprite_pos.setX(canvas_pos.x() - self._spriteObject.boundingRect().left())
        self._mouseState.sprite_pos.setY(canvas_pos.y() - self._spriteObject.boundingRect().top())

        if self._pixelSize > 1 and self._snapEnabled:
            self._mouseState.sprite_pos = utils.snap_point(self._mouseState.sprite_pos,
                                                           self._pixelSize)
            self._mouseState.canvas_pos = utils.snap_point(self._mouseState.canvas_pos,
                                                           self._pixelSize)

        if self._currentTool.is_active:

            self._currentTool.on_mouse_move(self)

        self._mouseState.last_canvas_pos.setX(canvas_pos.x())
        self._mouseState.last_canvas_pos.setY(canvas_pos.y())

        self._mouseState.last_sprite_pos.setX(self._mouseState.sprite_pos.x())
        self._mouseState.last_sprite_pos.setY(self._mouseState.sprite_pos.y())

        self.update()

    def mouseReleaseEvent(self, e):

        super(Canvas, self).mouseReleaseEvent(e)

        if not self._overlay.isEnabled:

            self._overlay.enable()

        self._mouseState.pressed_button = None

        self._currentTool.on_mouse_release(self)

        self.toolEnded.emit(self._currentTool)

        self.update()

    def enterEvent(self, e):

        super(Canvas, self).enterEvent(e)

        self.setCursor(Qt.BlankCursor)

        self._overlay.enable()

        self.update()

    def leaveEvent(self, e):

        super(Canvas, self).leaveEvent(e)

        self.setCursor(Qt.ArrowCursor)

        self._overlay.disable()

        self.update()

    def keyPressEvent(self, e):

        super(Canvas, self).keyPressEvent(e)

    def keyReleaseEvent(self, e):

        super(Canvas, self).keyReleaseEvent(e)

    def dragEnterEvent(self, e):

        if e.mimeData().hasUrls():
            self._isOnDragDrop = True
            e.acceptProposedAction()

    def dragMoveEvent(self, e):

        if self._isOnDragDrop:
            e.acceptProposedAction()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            file_path = e.mimeData().urls()[0].toLocalFile()

            if utils.get_file_extension(file_path) == '.png':
                image = utils.load_image(file_path)

                self._spriteObject.sprite.paste_image(image)

                self.viewportChanged.emit()

                self.update_viewport()

    # -------------------------------------------------------------------------

    def _load_tools(self):

        # Default Tools

        self._tools['Pen'] = tools.Pen()
        self._tools['Picker'] = tools.Picker()
        self._tools['Filler'] = tools.Filler()
        self._tools['Manipulator'] = tools.Manipulator()

    def _load_inks(self):

        # Default Inks

        self._inks['Solid'] = inks.Solid()
        self._inks['Eraser'] = inks.Eraser()

    def _init_canvas_state(self):

        self._pixelSize = 1
        self._primaryColor = QColor('black')
        self._secondaryColor = QColor('white')
        self._currentTool = self.find_tool_by_name('Pen')
        self._primaryInk = self.find_ink_by_name('Solid')
        self._secondaryInk = self.find_ink_by_name('Eraser')
