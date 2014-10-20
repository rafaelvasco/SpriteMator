#--------------------------------------------------------------------------------------------------
# Purpose:          Defines default set of Canvas Tools
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------------------------------------------------------

import quickpixler

from PyQt5.QtCore import Qt, QPoint, QRect, QTimer, QRectF
from PyQt5.QtGui import QPen, QColor, QIcon, QPixmap, QPainter

import src.drawing as drawing
import src.utils as utils
from src.properties import PropertyHolder


class Tool(PropertyHolder):
    def __init__(self, canvas):

        super(Tool, self).__init__()

        self._canvas = canvas

        self._name = ''
        self._drawPen = QPen()
        self._drawPen.setColor(Qt.white)
        self._drawPen.setJoinStyle(Qt.MiterJoin)
        self._drawPen.setWidth(0)
        self._drawPen.setCapStyle(Qt.SquareCap)

        self._isActive = False

        self._default = False

        self._pointerBrush = None

        self._enablePointerDraw = False

        self._refreshWaitTime = 0

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
    def icon(self):
        return self._icon

    @property
    def enable_pointer_draw(self):
        return self._enablePointerDraw

    @enable_pointer_draw.setter
    def enable_pointer_draw(self, value):
        self._enablePointerDraw = value

    @property
    def refresh_wait_time(self):
        return self._refreshWaitTime

    @refresh_wait_time.setter
    def refresh_wait_time(self, value):
        self._refreshWaitTime = value

    def on_mouse_press(self):
        self._isActive = True

    def on_mouse_move(self):
        pass

    def on_mouse_release(self):
        self._isActive = False

    # Draw On Transformed Scene Foreground
    def draw_on_canvas_foreground(self, painter):
        pass

    # Draw on Un-Transformed Scene Foreground
    def draw_on_canvas_overlay(self, painter):
        pass

    def _load_icon(self, icon_path, icon_active_path):

        self._icon = QIcon()
        self._icon.addPixmap(QPixmap(icon_path), QIcon.Normal, QIcon.Off)
        self._icon.addPixmap(QPixmap(icon_active_path), QIcon.Normal, QIcon.On)

# =================================================================================================


class Picker(Tool):
    def __init__(self, canvas):
        super(Picker, self).__init__(canvas)
        self._name = 'Picker'

        self._load_icon(":/icons/ico_picker", ":/icons/ico_picker_hover")

        self.add_property('returnlasttool', True, 'After Picking: Go back to last Tool')

    def draw_on_canvas_overlay(self, painter):

        if not self._enablePointerDraw:
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

    def on_mouse_press(self):

        super(Picker, self).on_mouse_press()

        picked_color = \
            QColor(self._canvas.sprite_object.active_surface.pixel(self._canvas.mouse_state.sprite_pos))
        self._canvas.colorPicked.emit(picked_color, self._canvas.mouse_state.pressed_button)

        #if self.propertyValue('returnlasttool'):
        #    canvas.tool_box().go_back_to_last_tool()


# =================================================================================================

class Pen(Tool):
    def __init__(self, canvas):

        super(Pen, self).__init__(canvas)

        self._deltaX = 0
        self._deltaY = 0

        self.name = 'Pen'

        self._lockHorizontal = False
        self._lockVertical = False

        self._wasLockingMouse = False

        self._load_icon(":/icons/ico_pen", ":/icons/ico_pen_hover")

        self._default = True

    def draw_on_canvas_overlay(self, painter):

        if not self._enablePointerDraw:
            return

        canvas = self._canvas

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

    def _blit(self, just_pressed):

        canvas = self._canvas

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

    def on_mouse_press(self):

        super(Pen, self).on_mouse_press()

        self._blit(just_pressed=True)

    def on_mouse_move(self):

        canvas = self._canvas

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
            self._blit(just_pressed=False)

    def on_mouse_release(self):

        super(Pen, self).on_mouse_release()
        self._lockHorizontal = self._lockVertical = False

# =================================================================================================


class Filler(Tool):
    def __init__(self, canvas):

        super(Filler, self).__init__(canvas)

        self.name = 'Filler'

        self._load_icon(":/icons/ico_fill", ":/icons/ico_fill_hover")

        self._refreshWaitTime = 500

    def draw_on_canvas_overlay(self, painter):

        if not self._enablePointerDraw:
            return

    def on_mouse_press(self):

        super(Filler, self).on_mouse_press()

        canvas = self._canvas

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


ManipulatorState = utils.enum('Idle',
                              'MovingPixels',
                              'MovingSelection',
                              'MovingSelectedPixels',
                              'Selecting',
                              'ScalingSelection')


class Manipulator(Tool):

    def __init__(self, canvas):
        super(Manipulator, self).__init__(canvas)

        self._name = 'Manipulator'
        self._load_icon(":/icons/ico_sel_move", ":/icons/ico_sel_move_hover")
        self._cursor = QPixmap(":/images/mover_cursor")

        self._pressMousePos = QPoint()
        self._lastMousePos = QPoint()
        self._curMousePos = QPoint()
        self._selectionRectangle = QRect()
        self._dashingAntsTimer = QTimer()

        self._selectionRectColor = QColor(255, 255, 255, 50)
        self._selectionRectDashOffset = 0
        self._selectionImage = None

        self._selectionBorderPen = QPen()
        self._selectionBorderPen.setWidth(0)
        self._selectionBorderPen.setStyle(Qt.DashLine)
        self._selectionBorderPen.setColor(Qt.white)

        self._selectionRectNodesPen = QPen()
        self._selectionRectNodesPen.setWidth(0)
        self._selectionRectNodesPen.setColor(Qt.white)

        self._dashingAntsTimer.timeout.connect(self._animate_selection_border)
        self._dashingAntsTimer.stop()

        self._state = ManipulatorState.Idle

    def draw_on_canvas_foreground(self, painter):

        if not self._selectionRectangle.isEmpty():

            painter.setCompositionMode(QPainter.CompositionMode_Difference)
            painter.setPen(self._selectionBorderPen)

            if self._selectionImage is None:

                painter.fillRect(self._selectionRectangle, self._selectionRectColor)
                painter.drawRect(self._selectionRectangle)

            else:

                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
                painter.drawImage(self._selectionRectangle, self._selectionImage)

                painter.setCompositionMode(QPainter.CompositionMode_Difference)
                painter.drawRect(self._selectionRectangle)

    def draw_on_canvas_overlay(self, painter):

        canvas = self._canvas

        x = canvas.mouse_state.global_pos.x() + 1
        y = canvas.mouse_state.global_pos.y() + 1

        if self._enablePointerDraw and self._state == ManipulatorState.Idle \
                or self._state == ManipulatorState.MovingSelection\
                or self._state == ManipulatorState.MovingPixels:

            painter.drawPixmap(x - self._cursor.width()/2, y -
                               self._cursor.height()/2, self._cursor)

    def on_mouse_press(self):

        super(Manipulator, self).on_mouse_press()

        canvas = self._canvas

        button = canvas.mouse_state.pressed_button
        mouse_pos = canvas.mouse_state.canvas_pos

        self._lastMousePos.setX(mouse_pos.x())
        self._lastMousePos.setY(mouse_pos.y())
        self._curMousePos.setX(mouse_pos.x())
        self._curMousePos.setY(mouse_pos.y())
        self._pressMousePos.setX(mouse_pos.x())
        self._pressMousePos.setY(mouse_pos.y())

        if button == Qt.LeftButton:
    
            if self._selectionRectangle.isEmpty():
    
                self._state = ManipulatorState.MovingPixels

            else:

                if self._selectionRectangle.contains(
                        QPoint(round(mouse_pos.x()), round(mouse_pos.y()))):

                    self._state = ManipulatorState.MovingSelection

                else:

                    self._clear_selection()
                    self._state = ManipulatorState.Idle
            
        elif button == Qt.RightButton:
            
            self._clear_selection()
            self._state = ManipulatorState.Selecting

    def on_mouse_move(self):

        canvas = self._canvas

        mouse_pos = canvas.mouse_state.canvas_pos

        if self._state == ManipulatorState.MovingPixels:

            self._lastMousePos.setX(self._curMousePos.x())
            self._lastMousePos.setY(self._curMousePos.y())

            self._curMousePos.setX(mouse_pos.x())
            self._curMousePos.setY(mouse_pos.y())

            dx = self._curMousePos.x() - self._lastMousePos.x()
            dy = self._curMousePos.y() - self._lastMousePos.y()

            image = canvas.sprite_object.active_surface

            if image is not None:

                image_data = canvas.sprite_object.active_surface_pixel_data

                if image_data is None:
                    return

                quickpixler.movePixels(image_data, image.width(), image.height(), dx, dy)
                
        elif self._state == ManipulatorState.Selecting:

            top_left = QPoint(min(mouse_pos.x(), self._pressMousePos.x()),
                              min(mouse_pos.y(), self._pressMousePos.y()))

            width = abs(mouse_pos.x() - self._pressMousePos.x())
            height = abs(mouse_pos.y() - self._pressMousePos.y())

            self._selectionRectangle.setRect(top_left.x(), top_left.y(),
                                             width, height)

        elif self._state == ManipulatorState.MovingSelection:

            self._lastMousePos.setX(self._curMousePos.x())
            self._lastMousePos.setY(self._curMousePos.y())

            self._curMousePos.setX(mouse_pos.x())
            self._curMousePos.setY(mouse_pos.y())

            dx = self._curMousePos.x() - self._lastMousePos.x()
            dy = self._curMousePos.y() - self._lastMousePos.y()

            self._selectionRectangle.translate(dx, dy)

        elif self._state == ManipulatorState.ScalingSelection:
            pass

    def on_mouse_release(self):

        super(Manipulator, self).on_mouse_press()

        if self._state == ManipulatorState.Selecting:
            #self._dashingAntsTimer.start()

            if not self._selectionRectangle.isEmpty():
                self._cut_selection()

        self._state = ManipulatorState.Idle

    def _animate_selection_border(self):

        self._selectionRectDashOffset += 1.0

        if self._selectionRectDashOffset > 6.0:
            self._selectionRectDashOffset = 0.0

        self._selectionBorderPen.setDashOffset(self._selectionRectDashOffset)

    def _clear_selection(self):

        self._selectionRectangle = QRect()
        self._selectionImage = None
        #self._dashingAntsTimer.stop()

    def _normalize_selection_rect(self):

        sprite_bounding_rect_global = self._canvas.map_scene_rect_to_global_rect(
            self._canvas.sprite_object.boundingRect())

        if self._selectionRectangle.left() < sprite_bounding_rect_global.left():
            self._selectionRectangle.setLeft(sprite_bounding_rect_global.left())

        if self._selectionRectangle.right() > sprite_bounding_rect_global.right():
            self._selectionRectangle.setRight(sprite_bounding_rect_global.right())

        if self._selectionRectangle.top() < sprite_bounding_rect_global.top():
            self._selectionRectangle.setTop(sprite_bounding_rect_global.top())

        if self._selectionRectangle.bottom() > sprite_bounding_rect_global.bottom():
            self._selectionRectangle.setBottom(sprite_bounding_rect_global.bottom())

        # if self._selectionRectangle.x() < 0:
        #     self._selectionRectangle.setX(0)
        #
        # if self._selectionRectangle.y() < 0:
        #     self._selectionRectangle.setY(0)
        #
        # if self._selectionRectangle.width() > self._canvas.sprite_object.boundingRect().width():
        #     self._selectionRectangle.setWidth(self._canvas.sprite_object.boundingRect().width())
        #
        # if self._selectionRectangle.height() > self._canvas.sprite_object.boundingRect().height():
        #     self._selectionRectangle.setHeight(self._canvas.sprite_object.boundingRect().height())

    def _cut_selection(self):

        #self._normalize_selection_rect()

        sprite_rect = self._canvas.map_global_rect_to_sprite_local_rect(self._selectionRectangle)

        print('CUT: Sel Rect: ', self._selectionRectangle, ', Final Rect: ', sprite_rect)

        self._selectionImage = self._canvas.sprite_object.active_surface.copy(sprite_rect)

    def _paste_selection(self):
        pass