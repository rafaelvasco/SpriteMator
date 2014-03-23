#--------------------------------------------------
# Purpose:          Concentrates the funcionalities of all tools of Canvas like Pen, Picker, Rectangle etc.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------

from quickpixler import floodFill

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPen, QColor, QIcon, QPixmap

import src.drawing as drawing
import src.utils as utils
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

        self._uses_painter = False

        self._refreshWaitTime = 0

        self._drawBrush = None

        self._icon = None

    def name(self):
        return self._name

    def set_name(self, name):

        self._name = name

    def refresh_wait_time(self):

        return self._refreshWaitTime

    def icon(self):

        return self._icon

    def uses_painter(self):

        return self._uses_painter

    def on_mouse_press(self, canvas, painter):
        pass

    def on_mouse_move(self, canvas, painter):
        pass

    def on_mouse_release(self, canvas, painter):
        pass

    def draw(self, canvas, painter):
        pass

# ======================================================================================================================


class Picker(Tool):
    def __init__(self):
        super(Picker, self).__init__()
        self._name = 'Picker'

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_picker"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_picker_hover"), QIcon.Normal, QIcon.On)
        self.add_property('returnlasttool', True, 'After Picking: Go back to last Tool')

    def draw(self, canvas, painter):

        x = canvas.mouse_state().canvas_mouse_position().x()
        y = canvas.mouse_state().canvas_mouse_position().y()

        size = 16 * canvas.zoom_value()

        if size > 32:
            size = 32

        painter.setPen(Qt.white)

        half_size = size // 2
        size_by_8 = size // 8

        painter.drawRect(x - half_size, y - half_size, size, size)

        painter.drawLine(x, y - size_by_8, x, y + size_by_8)
        painter.drawLine(x - size_by_8, y, x + size_by_8, y)

    def on_mouse_press(self, canvas, painter):

        mouse_state = canvas.mouse_state()

        picked_color = QColor(canvas.drawing_surface().pixel(mouse_state.sprite_mouse_position()))
        canvas.colorPicked.emit(picked_color, mouse_state.last_button_pressed())

        if self.property_value('returnlasttool'):
            canvas.tool_box().go_back_to_last_tool()


# ======================================================================================================================

class Pen(Tool):
    def __init__(self):

        super(Pen, self).__init__()

        self._deltaX = 0
        self._deltaY = 0

        self.set_name('Pen')

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(":/icons/ico_pen"), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(":/icons/ico_pen_hover"), QIcon.Normal, QIcon.On)

        self._uses_painter = True

    def draw(self, canvas, painter):

        x = canvas.mouse_state().canvas_mouse_position().x()
        y = canvas.mouse_state().canvas_mouse_position().y()

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

    def _blit(self, canvas, painter, just_pressed):

        size = canvas.pixel_size()
        last_button_pressed = canvas.mouse_state().last_button_pressed()
        mouse_pos = canvas.mouse_state().sprite_mouse_position()
        last_mouse_pos = canvas.mouse_state().last_sprite_mouse_position()

        delta_x = abs(mouse_pos.x() - last_mouse_pos.x())
        delta_y = abs(mouse_pos.y() - last_mouse_pos.y())

        if delta_x == 0 and delta_y == 0 and not just_pressed:
            return

        ink = None
        color = None

        if last_button_pressed == Qt.LeftButton:
            ink = canvas.primary_ink()
            color = canvas.primary_color()

        elif last_button_pressed == Qt.RightButton:
            ink = canvas.secondary_ink()
            color = canvas.secondary_color()

        if ink is not None and color is not None:

            if delta_x > 1 or delta_y > 1:
                drawing.draw_line(last_mouse_pos, mouse_pos, size, ink, color, painter)
            elif delta_x == 1 or delta_y == 1 or just_pressed:
                ink.blit(mouse_pos.x(), mouse_pos.y(), size, size, color, painter)

    def on_mouse_press(self, canvas, painter):

        self._blit(canvas, painter, just_pressed=True)

    def on_mouse_move(self, canvas, painter):

        if canvas.mouse_state().is_mouse_pressing():

            self._blit(canvas, painter, just_pressed=False)

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

    def draw(self, canvas, painter):

        x = canvas.mouse_state().canvas_mouse_position().x()
        y = canvas.mouse_state().canvas_mouse_position().y()

        cursor_w = self._cursorPixmap.width()
        cursor_h = self._cursorPixmap.height()

        painter.drawPixmap(x - cursor_w // 2, y - cursor_h // 2, self._cursorPixmap)

    def on_mouse_press(self, canvas, painter):

        image = canvas.drawing_surface()
        button = canvas.mouse_state().last_button_pressed()
        mouse_pos = canvas.mouse_state().sprite_mouse_position()

        if image is not None:

            image_data = canvas.drawing_surface_pixel_data()

            color = None

            if button == Qt.LeftButton:

                color = canvas.primary_color()

            elif button == Qt.RightButton:

                color = canvas.secondary_color()

            if color is not None:

                floodFill(image_data, mouse_pos.x(), mouse_pos.y(), image.width(), image.height(),
                          color.red(), color.green(), color.blue())

# ======================================================================================================================
