#--------------------------------------------------------------------------------------------------
# Purpose:          Defines default set of Canvas Tools
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------------------------------------------------------

import quickpixler

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPen, QColor, QIcon, QPixmap, QPainter

import src.drawing as drawing
import src.utils as utils
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

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_default(self):
        return self._default

    @property
    def is_active(self):
        return self._isActive

    @property
    def refresh_wait_time(self):
        return self._refreshWaitTime

    @refresh_wait_time.setter
    def refresh_wait_time(self, value):
        self._refreshWaitTime = value

    @property
    def icon(self):
        return self._icon

    def on_mouse_press(self, canvas):
        self._isActive = True

    def on_mouse_move(self, canvas):
        pass

    def on_mouse_release(self, canvas):
        self._isActive = False

    def draw(self, canvas, painter):
        pass

    def _load_icon(self, icon_path, icon_active_path):

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(icon_active_path), QIcon.Normal, QIcon.On)

# =================================================================================================


class Picker(Tool):
    def __init__(self):
        super(Picker, self).__init__()
        self._name = 'Picker'

        self._load_icon(":/icons/ico_picker", ":/icons/ico_picker_hover")

        self.add_property('returnlasttool', True, 'After Picking: Go back to last Tool')

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

    def on_mouse_press(self, canvas):

        super(Picker, self).on_mouse_press(canvas)

        picked_color = \
            QColor(canvas.sprite_object.active_surface.pixel(canvas.mouse_state.sprite_pos))
        canvas.colorPicked.emit(picked_color, canvas.mouse_state.pressed_button)

        #if self.propertyValue('returnlasttool'):
        #    canvas.tool_box().go_back_to_last_tool()


# =================================================================================================

class Pen(Tool):
    def __init__(self):

        super(Pen, self).__init__()

        self._deltaX = 0
        self._deltaY = 0

        self.name = 'Pen'

        self._lockHorizontal = False
        self._lockVertical = False

        self._wasLockingMouse = False

        self._load_icon(":/icons/ico_pen", ":/icons/ico_pen_hover")

        self._usesPainter = True

        self._default = True

    def draw(self, canvas, painter):

        x = canvas.mouse_state.global_pos.x() + 1
        y = canvas.mouse_state.global_pos.y() + 1

        size = canvas.pixel_size * canvas.zoom

        if size <= 0.0:
            return

        painter.setPen(Qt.white)
        painter.setOpacity(0.6)
        painter.setCompositionMode(QPainter.CompositionMode_Difference)

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

            painter.drawRect(x-size/2, y-size/2, size, size)

            painter.drawLine(x-2, y, x+2, y)
            painter.drawLine(x, y-2, x, y+2)

    def _blit(self, canvas, just_pressed):

        size = canvas.pixel_size
        mouse_state = canvas.mouse_state
        last_button_pressed = mouse_state.pressed_button

        if self._lockHorizontal and not self._lockVertical:
            mouse_state.sprite_pos.setY(mouse_state.last_sprite_pos.y())

        elif self._lockVertical and not self._lockHorizontal:
            mouse_state.sprite_pos.setX(mouse_state.last_sprite_pos.x())

        elif self._wasLockingMouse and not self._lockHorizontal and not self._lockVertical:
            mouse_state.last_sprite_pos.setX(mouse_state.sprite_pos.x())
            mouse_state.last_sprite_pos.setY(mouse_state.sprite_pos.y())
            self._wasLockingMouse = False

        delta_x = abs(mouse_state.sprite_pos.x() - mouse_state.last_sprite_pos.x())
        delta_y = abs(mouse_state.sprite_pos.y() - mouse_state.last_sprite_pos.y())

        if delta_x == 0 and delta_y == 0 and not just_pressed:
            return

        ink = None
        color = None

        if last_button_pressed == Qt.LeftButton:

            ink = canvas.primary_ink
            color = canvas.primary_color

        elif last_button_pressed == Qt.RightButton:

            ink = canvas.secondary_ink
            color = canvas.secondary_color

        if ink is not None and color is not None:

            painter = QPainter()

            painter.begin(canvas.sprite_object.active_surface)

            if delta_x > 1 or delta_y > 1:
                drawing.draw_line(mouse_state.last_sprite_pos, mouse_state.sprite_pos, size, ink,
                                  color, painter)
            elif delta_x == 1 or delta_y == 1 or just_pressed:

                ink.blit(mouse_state.sprite_pos.x(), mouse_state.sprite_pos.y(), size, size, color,
                         painter)

            painter.end()

    def on_mouse_press(self, canvas):

        super(Pen, self).on_mouse_press(canvas)

        self._blit(canvas, just_pressed=True)

    def on_mouse_move(self, canvas):

        mouse_state = canvas.mouse_state

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

        if mouse_state.pressed_button is not None:
            self._blit(canvas, just_pressed=False)

    def on_mouse_release(self, canvas):

        super(Pen, self).on_mouse_release(canvas)
        self._lockHorizontal = self._lockVertical = False

# =================================================================================================


class Filler(Tool):
    def __init__(self):

        super(Filler, self).__init__()

        self.name = 'Filler'

        self._refreshWaitTime = 500

        self._load_icon(":/icons/ico_fill", ":/icons/ico_fill_hover")

    def draw(self, canvas, painter):

        return

    def on_mouse_press(self, canvas):

        super(Filler, self).on_mouse_press(canvas)

        image = canvas.sprite_object.active_surface
        button = canvas.mouse_state.pressed_button
        mouse_pos = canvas.mouse_state.sprite_pos

        sprite_bounding_box = canvas.sprite_object.area_rect

        if not sprite_bounding_box.contains(mouse_pos):
            return

        if image is not None:

            image_data = canvas.sprite_object.active_surface_pixel_data

            if image_data is None:
                return

            color = None

            if button == Qt.LeftButton:

                color = canvas.primary_color

            elif button == Qt.RightButton:

                color = canvas.secondary_color

            if color is not None:

                quickpixler.floodFill(image_data, mouse_pos.x(), mouse_pos.y(), image.width(),
                                      image.height(),
                                      color.red(), color.green(), color.blue())

# =================================================================================================


ManipulatorState = utils.enum('Idle', 'MovingPixels', 'MovingSelection', 'Selecting',
                              'ScalingSelection')


class Manipulator(Tool):

    def __init__(self):
        super(Manipulator, self).__init__()

        self._name = 'Manipulator'
        self._load_icon(":/icons/ico_sel_move", ":/icons/ico_sel_move_hover")
        self._cursor = QPixmap(":/images/mover_cursor")

        self._pressMousePos = QPoint()
        self._lastMousePos = QPoint()
        self._curMousePos = QPoint()
        self._selectionRectangle = QRect()

        self._state = ManipulatorState.Idle

    def draw(self, canvas, painter):

        x = canvas.mouse_state.global_pos.x() + 1
        y = canvas.mouse_state.global_pos.y() + 1
    
        if self._state == ManipulatorState.Idle \
                or self._state == ManipulatorState.MovingSelection\
                or self._state == ManipulatorState.MovingPixels:
    
            painter.drawPixmap(x - self._cursor.width()/2, y -
                               self._cursor.height()/2, self._cursor)

        elif self._state == ManipulatorState.Selecting:

            pen = QPen()
            pen.setStyle(Qt.DotLine)
            pen.setBrush(Qt.black)

            painter.setPen(pen)
            print(self._selectionRectangle)
            painter.drawRect(self._selectionRectangle)

    def on_mouse_press(self, canvas):

        super(Manipulator, self).on_mouse_press(canvas)

        button = canvas.mouse_state.pressed_button
        mouse_pos = canvas.mouse_state.sprite_pos
        
        self._lastMousePos.setX(mouse_pos.x())
        self._lastMousePos.setY(mouse_pos.y())
        self._curMousePos.setX(mouse_pos.x())
        self._curMousePos.setY(mouse_pos.y())
        self._pressMousePos.setX(canvas.mouse_state.global_pos.x())
        self._pressMousePos.setY(canvas.mouse_state.global_pos.y())
        
        if button == Qt.LeftButton:
    
            sprite_bounding_box = canvas.sprite_object.area_rect
    
            if not sprite_bounding_box.contains(mouse_pos):
                return
    
            self._state = ManipulatorState.MovingPixels
            
        elif button == Qt.RightButton:
            
            self._state = ManipulatorState.Selecting

    def on_mouse_move(self, canvas):

        mouse_pos = canvas.mouse_state.sprite_pos
        global_mouse_pos = canvas.mouse_state.global_pos

        if self._state == ManipulatorState.MovingPixels:

            image = canvas.sprite_object.active_surface

            self._lastMousePos.setX(self._curMousePos.x())
            self._lastMousePos.setY(self._curMousePos.y())

            self._curMousePos.setX(mouse_pos.x())
            self._curMousePos.setY(mouse_pos.y())

            dx = self._curMousePos.x() - self._lastMousePos.x()
            dy = self._curMousePos.y() - self._lastMousePos.y()

            if image is not None:

                image_data = canvas.sprite_object.active_surface_pixel_data

                if image_data is None:
                    return

                quickpixler.movePixels(image_data, image.width(), image.height(), dx, dy)
                
        elif self._state == ManipulatorState.Selecting:

            top_left = QPoint(min(global_mouse_pos.x(), self._pressMousePos.x()),
                              min(global_mouse_pos.y(), self._pressMousePos.y()))

            width = abs(global_mouse_pos.x() - self._pressMousePos.x())
            height = abs(global_mouse_pos.y() - self._pressMousePos.y())

            self._selectionRectangle.setRect(top_left.x(), top_left.y(),
                                             width, height)

        elif self._state == ManipulatorState.MovingSelection:
            pass
        
        elif self._state == ManipulatorState.ScalingSelection:
            pass

    def on_mouse_release(self, canvas):

        super(Manipulator, self).on_mouse_press(canvas)

        if self._state == ManipulatorState.Selecting:

            self._selectionRectangle = QRect()

        self._state = ManipulatorState.Idle