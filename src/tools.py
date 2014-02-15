#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor, QIcon, QPixmap

import src.drawing as drawing
import src.utils as utils

from src.resources_cache import ResourcesCache
#from quickpixler import floodFill


class Tool(object):
    def __init__(self):

        self._name = ''
        self._active = False
        self._pressMousePos = QPoint()
        self._lastMousePos = QPoint()
        self._currentMousePos = QPoint()
        self._absoluteMousePos = QPoint()
        self._lastButtonPressed = None
        self._snapPos = False

        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)

        self._refreshWaitTime = 0

        self._drawBrush = None

        self._icon = None

    def name(self):
        return self._name

    def set_name(self, name):

        self._name = name

    def is_active(self):

        return self._active

    def set_active(self, active):

        self._active = active

    def set_snap(self, snap):

        self._snapPos = snap

    def refresh_wait_time(self):

        return self._refreshWaitTime

    def icon(self):

        return self._icon

    def _process_mouse_press(self, canvas, mouse_event):

        if mouse_event.button() != Qt.LeftButton and mouse_event.button() != Qt.RightButton:
            return

        self.set_active(True)

        pixel_size = canvas.pixel_size()
        mouse_pos = canvas.sprite_mouse_pos()

        if pixel_size > 1 and self._snapPos:

            sprite_pos = utils.snap_point(mouse_pos, pixel_size)
        else:

            sprite_pos = mouse_pos

        self._pressMousePos.setX(sprite_pos.x())
        self._pressMousePos.setY(sprite_pos.y())

        self._lastMousePos.setX(sprite_pos.x())
        self._lastMousePos.setY(sprite_pos.y())

        self._currentMousePos.setX(sprite_pos.x())
        self._currentMousePos.setY(sprite_pos.y())

        self.on_mouse_press(canvas, mouse_event)

    def _process_mouse_move(self, canvas, mouse_event):

        sprite_pos = canvas.sprite_mouse_pos()
        absolute_pos = mouse_event.pos()

        size = canvas.pixel_size()

        self._lastMousePos.setX(self._currentMousePos.x())
        self._lastMousePos.setY(self._currentMousePos.y())

        if size > 1 and self._snapPos:
            self._currentMousePos = utils.snap_point(sprite_pos, size)
        else:
            self._currentMousePos.setX(sprite_pos.x())
            self._currentMousePos.setY(sprite_pos.y())

        self._absoluteMousePos.setX(absolute_pos.x())
        self._absoluteMousePos.setY(absolute_pos.y())

        self.on_mouse_move(canvas, mouse_event)

    def _process_mouse_release(self, canvas, mouse_event):

        self.set_active(False)

        self.on_mouse_release(canvas, mouse_event)

    def on_mouse_press(self, canvas, mouse_event):
        return

    def on_mouse_move(self, canvas, mouse_event):
        return

    def on_mouse_release(self, canvas, mouse_event):
        return

    def draw(self, painter, canvas):
        return

    def blit(self, painter, canvas):
        return


# ======================================================================================================================


class Picker(Tool):
    def __init__(self):
        super(Picker, self).__init__()
        self._name = 'Picker'

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_picker"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_picker_hover"), QIcon.Normal, QIcon.On)

    def draw(self, painter, canvas):
        x = self._absoluteMousePos.x()
        y = self._absoluteMousePos.y()

        size = 16 * canvas.zoom_value()

        if size > 32:
            size = 32

        painter.setPen(Qt.white)

        half_size = size // 2
        size_by_8 = size // 8

        painter.drawRect(x - half_size, y - half_size, size, size)

        painter.drawLine(x, y - size_by_8, x, y + size_by_8)
        painter.drawLine(x - size_by_8, y, x + size_by_8, y)

    def on_mouse_press(self, canvas, mouse_event):
        picked_color = QColor(canvas.drawing_surface().pixel(self._pressMousePos))
        canvas.colorPicked.emit(picked_color, mouse_event)


# ======================================================================================================================

class Pen(Tool):
    def __init__(self):

        super(Pen, self).__init__()

        self._deltaX = 0
        self._deltaY = 0

        self.set_snap(True)
        self.set_name('Pen')

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_pen"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_pen_hover"), QIcon.Normal, QIcon.On)

    def draw(self, painter, canvas):

        x = self._absoluteMousePos.x()
        y = self._absoluteMousePos.y()

        size = canvas.pixel_size() * canvas.zoom_value()

        if size <= 0.0:
            return

        if size == 1.0:

            painter.fillRect(x, y, 1, 1, Qt.white)

            painter.setPen(Qt.white)

            painter.drawLine(x, y - 4, x, y - 8)
            painter.drawLine(x, y + 4, x, y + 8)

            painter.drawLine(x - 4, y, x - 8, y)
            painter.drawLine(x + 4, y, x + 8, y)

        elif size == 2.0:

            painter.fillRect(x - 1, y - 1, 2, 2, Qt.white)

            painter.setPen(Qt.white)

            painter.drawLine(x - 2, y - 8, x + 1, y - 8)
            painter.drawLine(x - 2, y + 7, x + 1, y + 7)

            painter.drawLine(x - 8, y - 2, x - 8, y + 1)
            painter.drawLine(x + 7, y - 2, x + 7, y + 1)

        elif size == 4.0:

            painter.setPen(Qt.white)

            painter.drawRect(x - 2, y - 2, 4, 4)

            painter.drawLine(x - 2, y - 8, x + 2, y - 8)
            painter.drawLine(x - 2, y + 8, x + 2, y + 8)

            painter.drawLine(x - 8, y - 2, x - 8, y + 2)
            painter.drawLine(x + 8, y - 2, x + 8, y + 2)

        else:

            painter.setPen(Qt.white)

            half_size = size // 2
            size_by_8 = size // 8

            painter.drawRect(x - half_size, y - half_size, size, size)

            painter.drawLine(x, y - size_by_8, x, y + size_by_8)
            painter.drawLine(x - size_by_8, y, x + size_by_8, y)

    def blit(self, painter, canvas):

        size = canvas.pixel_size()
        last_button_pressed = canvas.last_button_pressed()

        ink = None
        color = None

        if last_button_pressed == Qt.LeftButton:
            ink = canvas.primary_ink()
            color = canvas.primary_color()

        elif last_button_pressed == Qt.RightButton:
            ink = canvas.secondary_ink()
            color = canvas.secondary_color()

        delta_x = self._currentMousePos.x() - self._lastMousePos.x()
        delta_y = self._currentMousePos.y() - self._lastMousePos.y()

        if delta_x != 0 or delta_y != 0:
            drawing.draw_line(self._lastMousePos, self._currentMousePos, size, ink, color, painter)
        elif ink is not None and color is not None:
            ink.blit(self._currentMousePos.x(), self._currentMousePos.y(), size, size, color, painter)


# ======================================================================================================================

class Filler(Tool):
    def __init__(self):

        super(Filler, self).__init__()

        self.set_name('Filler')

        self._refreshWaitTime = 500
        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_fill"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_fill_hover"), QIcon.Normal, QIcon.On)

        self._cursorPixmap = ResourcesCache.get("ToolCursor1")

    def draw(self, painter, canvas):

        x = self._absoluteMousePos.x()
        y = self._absoluteMousePos.y()

        cursor_w = self._cursorPixmap.width()
        cursor_h = self._cursorPixmap.height()

        painter.drawPixmap(x - cursor_w // 2, y - cursor_h // 2, self._cursorPixmap)

    #         size = 16 * canvas._zoom
    #
    #         if size > 32:
    #             size = 32
    #
    #
    #         painter.setPen(Qt.white)
    #
    #         halfSize = size // 2
    #         sizeBy8 = size // 8
    #
    #         painter.drawRect(x - halfSize - 1, y - halfSize - 1, size, size)
    #
    #         painter.drawLine(x, y - sizeBy8, x, y + sizeBy8)
    #         painter.drawLine(x - sizeBy8, y, x + sizeBy8, y)
    #
    #         painter.setPen(Qt.black)
    #
    #         painter.drawRect(x - halfSize, y - halfSize, size - 2, size - 2)
    #
    #         painter.drawLine(x, y - sizeBy8, x, y + sizeBy8)
    #         painter.drawLine(x - sizeBy8, y, x + sizeBy8, y)

    def on_mouse_press(self, canvas, mouse_event):

        image = canvas.drawing_surface()

        if image is not None:

            image_data = canvas.drawing_surface_pixel_data()

            color = None

            if mouse_event.button() == Qt.LeftButton:

                color = canvas.primary_color()

            elif mouse_event.button() == Qt.RightButton:

                color = canvas.secondary_color()

            if color is not None:

                floodFill(image_data, self._pressMousePos.x(), self._pressMousePos.y(), image.width(), image.height(),
                          color.red(), color.green(), color.blue())

# ======================================================================================================================
