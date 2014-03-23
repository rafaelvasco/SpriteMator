from PyQt5.QtCore import QPoint


class CanvasMouseState(object):

    def __init__(self):

        self._canvas_pos = QPoint()
        self._sprite_pos = QPoint()
        self._last_sprite_pos = QPoint()
        self._last_button_pressed = None
        self._mouse_pressing = False

    def canvas_mouse_position(self):

        return self._canvas_pos

    def set_canvas_mouse_position(self, pos):

        self._canvas_pos.setX(pos.x())
        self._canvas_pos.setY(pos.y())

    def sprite_mouse_position(self):

        return self._sprite_pos

    def last_sprite_mouse_position(self):

        return self._last_sprite_pos

    def set_sprite_mouse_position(self, pos):

        self._sprite_pos.setX(round(pos.x(), 2))
        self._sprite_pos.setY(round(pos.y(), 2))

    def set_last_sprite_mouse_position(self, pos):

        self._last_sprite_pos.setX(pos.x())
        self._last_sprite_pos.setY(pos.y())

    def last_button_pressed(self):

        return self._last_button_pressed

    def set_last_button_pressed(self, button):

        self._last_button_pressed = button

    def is_mouse_pressing(self):

        return self._mouse_pressing

    def set_mouse_pressing(self, pressing):

        self._mouse_pressing = pressing