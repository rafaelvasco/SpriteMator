#-----------------------------------------------------------------------------------------------------------------------
# Name:        Canvas
# Purpose:     The Canvas is a Display in which the DisplaySpriteItem's pixels can be edited
#
# Author:      Rafael Vasco
#
# Created:     30/03/2013
# Copyright:   (c) Rafael Vasco 2014
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QColor, QPainter

from src.display import Display
import src.utils as utils
from src import tools, inks
from src.tools import Tool



#-----------------------------------------------------------------------------------------------------------------------

class CanvasMouseState(object):

    def __init__(self):


        self._spritePos = QPoint()
        self._lastSpritePos = QPoint()
        self._canvasPos = QPoint()
        self._lastCanvasPos = QPoint()
        self._pressedButton = None
        self._isCtrlPressed = False
        self._isAltPressed = False
        self._isShiftPressed = False

    @property
    def spritePos(self):
        return self._spritePos

    @spritePos.setter
    def spritePos(self, value):
        self._spritePos = value

    @property
    def lastSpritePos(self):
        return self._lastSpritePos

    @lastSpritePos.setter
    def lastSpritePos(self, value):
        self._lastSpritePos = value

    @property
    def canvasPos(self):
        return self._canvasPos

    @canvasPos.setter
    def canvasPos(self, value):
        self._canvasPos = value

    @property
    def lastCanvasPos(self):
        return self._lastCanvasPos

    @lastCanvasPos.setter
    def lastCanvasPos(self, value):
        self._lastCanvasPos = value

    @property
    def pressedButton(self):
        return self._pressedButton

    @pressedButton.setter
    def pressedButton(self, value):
        self._pressedButton = value




class Canvas(Display):

    surfaceChanged = pyqtSignal()
    colorPicked = pyqtSignal(QColor, int)  # Color, Button Pressed
    toolStarted = pyqtSignal(Tool)
    toolEnded = pyqtSignal(Tool)

    def __init__(self):

        super(Canvas, self).__init__()

        self.turnBacklightOn()

        self._tools = {}

        self._inks = {}

        self._currentTool = None

        self._lastTool = None

        self._primaryInk = None

        self._secondaryInk = None

        self._primaryColor = None

        self._secondaryColor = None

        self._pixelSize = 0

        self._drawGrid = True

        self._snapEnabled = True

        self._mouseState = CanvasMouseState()

        self._loadTools()

        self._loadInks()

        self._initializeCanvasState()


        #self._toolbox = ToolBox(self)
        #self._toolbox.setVisible(False)
        #self._initialize_toolbox()

        self.setAcceptDrops(True)


    @property
    def spriteObject(self):
        return self._spriteObject

    @property
    def currentTool(self):
        return self._currentTool

    @property
    def lastTool(self):
        return self._lastTool

    @property
    def primaryColor(self):
        return self._primaryColor

    @primaryColor.setter
    def primaryColor(self, value):
        self._primaryColor = value

    @property
    def secondaryColor(self):
        return self._secondaryColor

    @secondaryColor.setter
    def secondaryColor(self, value):
        self._secondaryColor = value

    @property
    def primaryInk(self):
        return self._primaryInk

    @primaryInk.setter
    def primaryInk(self, value):
        self._primaryInk = value

    @property
    def secondaryInk(self):
        return self._secondaryInk

    @secondaryInk.setter
    def secondaryInk(self, value):
        self._secondaryInk = value

    @property
    def currentTool(self):
        return self._currentTool

    @currentTool.setter
    def currentTool(self, value):

        self._lastTool = self._currentTool
        self._currentTool = self.findToolByName(value)
        self.refresh()

    @property
    def pixelSize(self):
        return self._pixelSize

    @pixelSize.setter
    def pixelSize(self, value):
        self._pixelSize = value


    @property
    def mouseState(self):
        return self._mouseState

    def findToolByName(self, name):

        return self._tools[name]

    def findInkByName(self, name):

        return self._inks[name]

    def spriteIsSet(self):

        return self._spriteObject.sprite is not None


    # ----- PUBLIC API -------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def setSprite(self, sprite):

        if self.spriteIsSet():
            self.unloadSprite()

        #self._toolbox.setVisible(True)

        self._spriteObject.setSprite(sprite)

        self.refresh()


    def unloadSprite(self):

        #self._toolbox.setVisible(False)

        self.resetView()

        self._spriteObject.unloadSprite()

        self.update()

        self.setCursor(Qt.ArrowCursor)


    def refresh(self):

        #self._update_drawing_surface()

        self.update()


    def clear(self):

        if self._spriteObject is None:
            return

        surface = self._spriteObject.activeSurface

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

    # ----- EVENTS -----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def mousePressEvent(self, e):

        super(Canvas, self).mousePressEvent(e)

        if self.isPanning:
            return

        if e.button() == Qt.LeftButton:

            canvasPos = self._mouseState.canvasPos = self.mapToScene(e.pos())
            spritePos = self._mouseState.spritePos
            lastCanvasPos = self._mouseState.lastCanvasPos
            lastSpritePos = self._mouseState.lastSpritePos

            spritePos.setX(canvasPos.x() - self._spriteObject.boundingRect().left())
            spritePos.setY(canvasPos.y() - self._spriteObject.boundingRect().top())

            self._mouseState.pressedButton = e.button()

            self.toolStarted.emit(self._currentTool)

            if self._pixelSize > 1 and self._snapEnabled:
                spritePos = utils.snapPoint(spritePos, self._pixelSize)

            lastCanvasPos.setX(canvasPos.x())
            lastCanvasPos.setY(canvasPos.y())

            lastSpritePos.setX(spritePos.x())
            lastSpritePos.setY(spritePos.y())

            self._currentTool.onMousePress(self)

            self._scene.update()


    def mouseMoveEvent(self, e):

        super(Canvas, self).mouseMoveEvent(e)

        if self.isPanning:
            return

        if not self.spriteIsSet():
            return

        canvasPos = self._mouseState.canvasPos = self.mapToScene(e.pos())
        spritePos = self._mouseState.spritePos
        lastCanvasPos = self._mouseState.lastCanvasPos
        lastSpritePos = self._mouseState.lastSpritePos

        spritePos.setX(canvasPos.x() - self._spriteObject.boundingRect().left())
        spritePos.setY(canvasPos.y() - self._spriteObject.boundingRect().top())

        if self._pixelSize > 1 and self._snapEnabled:
            spritePos = utils.snapPoint(spritePos, self._pixelSize)

        self._currentTool.onMouseMove(self)

        self._scene.update()

        lastCanvasPos.setX(canvasPos.x())
        lastCanvasPos.setY(canvasPos.y())

        lastSpritePos.setX(spritePos.x())
        lastSpritePos.setY(spritePos.y())


    def mouseReleaseEvent(self, e):

        super(Canvas, self).mouseReleaseEvent(e)

        if self.isPanning:
            return

        self._mouseState.pressedButton = None



        self._currentTool.onMouseRelease(self)

        self.toolEnded.emit(self._currentTool)

        self._scene.update()


    def enterEvent(self, e):

        super(Canvas, self).enterEvent(e)


    def leaveEvent(self, e):

        super(Canvas, self).leaveEvent(e)


    def keyPressEvent(self, e):

        super(Canvas, self).keyPressEvent(e)


    def keyReleaseEvent(self, e):

        super(Canvas, self).keyReleaseEvent(e)


    def dragEnterEvent(self, e):

        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()


    def dragMoveEvent(self, e):

        #self.global_mouse_pos().setX(e.pos().x())
        #self.global_mouse_pos().setY(e.pos().y())

        super(Canvas, self).dragMoveEvent(e)


    def dropEvent(self, e):
        if e.mimeData().hasUrls():

            file_path = e.mimeData().urls()[0].toLocalFile()

            if utils.getFileExtension(file_path) == '.png':

                image = utils.loadImage(file_path)

                self._update_mouse_state(e)

                self._spriteObject.sprite.pasteImage(image)

                self._spriteObject.updateBoundingRect()

                self.refresh()


    def _onToolboxMouseEntered(self):

        if not self.spriteIsSet():
            return

        #self._overlay_surface.disable()


    def _onToolboxMouseLeft(self):

        if not self.spriteIsSet():
            return

        #self._overlay_surface.enable()


    def _onToolboxToolChanged(self, tool_name):

        self.currentTool = tool_name

    def _onToolboxPrimaryInkChanged(self, ink_name):

        self.primaryInk = ink_name


    def _onToolboxSecondaryInkChanged(self, ink_name):

        self.secondaryInk = ink_name

    # ---- PRIVATE METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------


    def _loadTools(self):

        # Default Tools

        self._tools['Pen'] = tools.Pen()
        self._tools['Picker'] = tools.Picker()
        self._tools['Filler'] = tools.Filler()


    def _loadInks(self):

        # Default Inks

        self._inks['Solid'] = inks.Solid()
        self._inks['Eraser'] = inks.Eraser()


    def _initializeCanvasState(self):

        self._pixelSize = 1
        self._primaryColor = QColor('black')
        self._secondaryColor = QColor('white')
        self._currentTool = self.findToolByName('Pen')
        self._primaryInk = self.findInkByName('Solid')
        self._secondaryInk = self.findInkByName('Eraser')

    # def _initialize_toolbox(self):
    #
    #     self._toolbox.mouseEntered.connect(self._on_toolbox_mouse_entered)
    #     self._toolbox.mouseLeft.connect(self._on_toolbox_mouse_left)
    #
    #     self._toolbox.register_tool(self.tool('Pen'), is_default=True)
    #     self._toolbox.register_tool(self.tool('Picker'))
    #     self._toolbox.register_tool(self.tool('Filler'))
    #
    #     self._toolbox.register_ink(self.ink('Solid'), slot=0)
    #     self._toolbox.register_ink(self.ink('Eraser'), slot=1)
    #
    #     self._toolbox.toolChanged.connect(self._on_toolbox_tool_changed)
    #     self._toolbox.primaryInkChanged.connect(self._on_toolbox_primary_ink_changed)
    #     self._toolbox.secondaryInkChanged.connect(self._on_toolbox_secondary_ink_changed)
