#--------------------------------------------------
# Purpose:          Defines default set of Canvas Tools
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------

from quickpixler import floodFill

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QIcon, QPixmap, QPainter

import src.drawing as drawing
from src.resources_cache import ResourcesCache
from src.properties import PropertyHolder


class Tool(PropertyHolder):
    def __init__(self):

        super(Tool, self).__init__()

        self._name = ''
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)

        self._usesPainter = False

        self._isActive = False

        self._refreshWaitTime = 0

        self._default = False

        self._drawBrush = None

        self._icon = None

    @property
    def name(self):
        return self._name

    @property
    def isDefault(self):
        return self._default

    @property
    def isActive(self):
        return self._isActive

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def refreshWaitTime(self):
        return self._refreshWaitTime

    @refreshWaitTime.setter
    def refreshWaitTime(self, value):
        self._refreshWaitTime = value

    @property
    def icon(self):
        return self._icon

    @property
    def usesPainter(self):
        return self._usesPainter

    def onMousePress(self, canvas):
        self._isActive = True

    def onMouseMove(self, canvas):
        pass

    def onMouseRelease(self, canvas):
        self._isActive = False

    def draw(self, canvas, event):
        pass

# ======================================================================================================================


class Picker(Tool):
    def __init__(self):
        super(Picker, self).__init__()
        self._name = 'Picker'

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_picker"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_picker_hover"), QIcon.Normal, QIcon.On)
        self.addProperty('returnlasttool', True, 'After Picking: Go back to last Tool')

    def draw(self, canvas, painter):
        return
        # x = canvas.mouse_state().canvas_mouse_position().x()
        # y = canvas.mouse_state().canvas_mouse_position().y()
        #
        # size = 16 * canvas.zoom_value()
        #
        # if size > 32:
        #     size = 32
        #
        # painter.setPen(Qt.white)
        #
        # half_size = size // 2
        # size_by_8 = size // 8
        #
        # painter.drawRect(x - half_size, y - half_size, size, size)
        #
        # painter.drawLine(x, y - size_by_8, x, y + size_by_8)
        # painter.drawLine(x - size_by_8, y, x + size_by_8, y)

    def onMousePress(self, canvas):

        super(Picker, self).onMousePress(canvas)

        picked_color = QColor(canvas.spriteObject.activeSurface.pixel(canvas.mouseState.spritePos))
        canvas.colorPicked.emit(picked_color, canvas.mouseState.pressedButton)

        #if self.propertyValue('returnlasttool'):
        #    canvas.tool_box().go_back_to_last_tool()


# ======================================================================================================================

class Pen(Tool):
    def __init__(self):

        super(Pen, self).__init__()

        self._deltaX = 0
        self._deltaY = 0

        self.name = 'Pen'

        self._lockHorizontal = False
        self._lockVertical = False

        self._wasLockingMouse = False

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_pen"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_pen_hover"), QIcon.Normal, QIcon.On)

        self._usesPainter = True

        self._default = True

    def draw(self, canvas, event):
        return
        # x = canvas.mouse_state().canvas_mouse_position().x()
        # y = canvas.mouse_state().canvas_mouse_position().y()
        #
        # size = canvas.pixel_size() * canvas.zoom_value()
        #
        # if size <= 0.0:
        #     return
        #
        # if size == 1.0:
        #
        #     painter.fillRect(x, y, 1, 1, Qt.white)
        #
        #     painter.setPen(Qt.white)
        #
        #     painter.drawLine(x, y - 4, x, y - 8)
        #     painter.drawLine(x, y + 4, x, y + 8)
        #
        #     painter.drawLine(x - 4, y, x - 8, y)
        #     painter.drawLine(x + 4, y, x + 8, y)
        #
        # elif size == 2.0:
        #
        #     painter.fillRect(x - 1, y - 1, 2, 2, Qt.white)
        #
        #     painter.setPen(Qt.white)
        #
        #     painter.drawLine(x - 2, y - 8, x + 1, y - 8)
        #     painter.drawLine(x - 2, y + 7, x + 1, y + 7)
        #
        #     painter.drawLine(x - 8, y - 2, x - 8, y + 1)
        #     painter.drawLine(x + 7, y - 2, x + 7, y + 1)
        #
        # elif size == 4.0:
        #
        #     painter.setPen(Qt.white)
        #
        #     painter.drawRect(x - 2, y - 2, 4, 4)
        #
        #     painter.drawLine(x - 2, y - 8, x + 2, y - 8)
        #     painter.drawLine(x - 2, y + 8, x + 2, y + 8)
        #
        #     painter.drawLine(x - 8, y - 2, x - 8, y + 2)
        #     painter.drawLine(x + 8, y - 2, x + 8, y + 2)
        #
        # else:
        #
        #     painter.setPen(Qt.white)
        #
        #     half_size = size // 2
        #     size_by_8 = size // 8
        #
        #     painter.drawRect(x - half_size, y - half_size, size, size)
        #
        #     painter.drawLine(x, y - size_by_8, x, y + size_by_8)
        #     painter.drawLine(x - size_by_8, y, x + size_by_8, y)

    def _blit(self, canvas, just_pressed):

        size = canvas.pixelSize
        mouseState = canvas.mouseState
        last_button_pressed = mouseState.pressedButton

        if self._lockHorizontal and not self._lockVertical:
            mouseState.spritePos.setY(mouseState.lastSpritePos.y())

        elif self._lockVertical and not self._lockHorizontal:
            mouseState.spritePos.setX(mouseState.lastSpritePos.x())

        elif self._wasLockingMouse and not self._lockHorizontal and not self._lockVertical:
            mouseState.lastSpritePos.setX(mouseState.spritePos.x())
            mouseState.lastSpritePos.setY(mouseState.spritePos.y())
            self._wasLockingMouse = False

        delta_x = abs(mouseState.spritePos.x() - mouseState.lastSpritePos.x())
        delta_y = abs(mouseState.spritePos.y() - mouseState.lastSpritePos.y())

        if delta_x == 0 and delta_y == 0 and not just_pressed:
            return

        ink = None
        color = None

        if last_button_pressed == Qt.LeftButton:

            ink = canvas.primaryInk
            color = canvas.primaryColor

        elif last_button_pressed == Qt.RightButton:

            ink = canvas.secondaryInk
            color = canvas.secondaryColor

        if ink is not None and color is not None:

            painter = QPainter()

            painter.begin(canvas.spriteObject.activeSurface)

            if delta_x > 1 or delta_y > 1:
                drawing.drawLine(mouseState.lastSpritePos, mouseState.spritePos, size, ink, color, painter)
            elif delta_x == 1 or delta_y == 1 or just_pressed:

                ink.blit(mouseState.spritePos.x(), mouseState.spritePos.y(), size, size, color, painter)

            painter.end()

    def onMousePress(self, canvas):

        super(Pen, self).onMousePress(canvas)

        self._blit(canvas, just_pressed=True)

    def onMouseMove(self, canvas):

        mouseState = canvas.mouseState

        #if mouseState.isControlPressed:

        #    self._wasLockingMouse = True
        #    self._lockHorizontal = True
        #    self._lockVertical = False

        #elif mouseState.isAltPressed:

        #    self._wasLockingMouse = True
        #    self._lockHorizontal = False
        #    self._lockVertical = True

        #else:

        #    self._lockVertical = self._lockHorizontal = False

        if mouseState.pressedButton is not None:
            self._blit(canvas, just_pressed=False)

    def onMouseRelease(self, canvas):

        super(Pen, self).onMouseRelease(canvas)
        self._lockHorizontal = self._lockVertical = False

# ======================================================================================================================


class Filler(Tool):
    def __init__(self):

        super(Filler, self).__init__()

        self.name = 'Filler'

        self._refreshWaitTime = 500
        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_fill"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_fill_hover"), QIcon.Normal, QIcon.On)

        self._cursorPixmap = ResourcesCache.get("ToolCursor1")

    def draw(self, canvas, painter):

        return

    def onMousePress(self, canvas):

        super(Filler, self).onMousePress(canvas)

        image = canvas.spriteObject.activeSurface
        button = canvas.mouseState.pressedButton
        mouse_pos = canvas.mouseState.spritePos


        sprite_bounding_box = canvas.spriteObject.areaRect

        if not sprite_bounding_box.contains(mouse_pos):
            return

        if image is not None:

            image_data = canvas.spriteObject.activeSurfacePixelData

            if image_data is None:
                return

            color = None

            if button == Qt.LeftButton:

                color = canvas.primaryColor

            elif button == Qt.RightButton:

                color = canvas.secondaryColor

            if color is not None:

                floodFill(image_data, mouse_pos.x(), mouse_pos.y(), image.width(), image.height(),
                          color.red(), color.green(), color.blue())

# ======================================================================================================================
