from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect, QTimer, QPoint
from PyQt5.QtGui import (QColor, QPainter,
                         QFontMetrics,
                         QIcon)
from PyQt5.QtWidgets import QWidget, QAbstractButton, QToolTip, \
    QPushButton

import src.utils as utils


class Button(QAbstractButton):
    clicked = pyqtSignal(int)
    leftClicked = pyqtSignal()
    middleClicked = pyqtSignal()
    rightClicked = pyqtSignal()
    activated = pyqtSignal()

    def __init__(self, label=None):

        super(Button, self).__init__()

        self._bgColor = QColor(51, 51, 51)
        self._activeBgColor = QColor(21, 21, 21)
        self._labelSize = QSize()
        self._size = QSize()
        self._iconSize = QSize()
        self._icon = None
        self._tooltip = None
        self._padding = 8
        self._idlePixmap = None
        self._checkedPixmap = None

        if label is not None:
            self.setText(label)

    def sizeHint(self):

        self._update_size()
        return self._size

    def setIcon(self, icon):

        self._icon = icon

        actual_size = self._icon.actualSize(self.size())

        self._iconSize.setWidth(actual_size.width())
        self._iconSize.setHeight(actual_size.height())

        self._update_icon_pixmaps()

        self.update()

    def setIconSize(self, size):

        self._iconSize.setWidth(size.width())
        self._iconSize.setHeight(size.height())

        self._update_icon_pixmaps()

        #self._updateSize()

        self.update()

    def setTooltip(self, text):

        self._tooltip = text

    def resizeEvent(self, e):
        pass
        #self._updateSize()

    def mousePressEvent(self, e):

        if not self.isCheckable():

            self.setDown(True)

        else:

            was_checked = self.isChecked()

            self.setChecked(not self.isChecked())

            if not was_checked and self.isChecked():
                self.activated.emit()

    def mouseReleaseEvent(self, e):

        if not self.isCheckable():
            self.setDown(False)

        if e.button() == Qt.LeftButton:

            self.leftClicked.emit()

        elif e.button() == Qt.MiddleButton:

            self.middleClicked.emit()

        elif e.button() == Qt.RightButton:

            self.rightClicked.emit()

        self.clicked.emit(e.button())

    def enterEvent(self, e):

        if self._tooltip is not None and len(self._tooltip) > 0:
            QTimer.singleShot(300, lambda t=self._tooltip: self._show_tooltip(t))

    def paintEvent(self, e):
        p = QPainter(self)

        active = self.isDown() or self.isChecked()

        if active:
            bg_color = self._activeBgColor
            border_color = bg_color.lighter(250)

        else:
            bg_color = self._bgColor
            border_color = bg_color.lighter(150)

        p.setPen(border_color)
        draw_rect = e.rect().adjusted(0, 0, -1, -1)

        p.drawRect(draw_rect)

        p.fillRect(draw_rect.adjusted(1, 1, 0, 0), bg_color)

        icon_margin = 0

        icon_present = self._icon is not None
        text_present = len(self.text()) > 0

        if icon_present:

            if not text_present:
                draw_x = round(draw_rect.width() / 2 - self._iconSize.width() / 2)
                draw_y = round(draw_rect.height() / 2 - self._iconSize.height() / 2)
            else:
                draw_x = self._padding
                draw_y = self._padding
                icon_margin = draw_x + self._iconSize.width()

            if not active and self._idlePixmap is not None:
                p.drawPixmap(draw_x, draw_y, self._idlePixmap)

            elif active and self._checkedPixmap is not None:

                p.drawPixmap(draw_x, draw_y, self._checkedPixmap)

        if text_present:

            p.setPen(Qt.white)

            if not icon_present:
                draw_x = round(draw_rect.width() / 2 - self._labelSize.width() / 2)
                draw_y = round(draw_rect.height() / 2 + self._labelSize.height() / 3)

            else:
                draw_x = icon_margin + 8
                draw_y = round(draw_rect.height() / 2 + self._labelSize.height() / 3)

            p.drawText(draw_x, draw_y, self.text())

    def _update_icon_pixmaps(self):

        if self._icon is None:
            return

        self._idlePixmap = self._icon.pixmap(self._iconSize, QIcon.Normal, QIcon.Off)
        self._checkedPixmap = self._icon.pixmap(self._iconSize, QIcon.Normal, QIcon.On)

    def _update_size(self):

        width = 0
        height = 0

        if self._icon is not None:
            width = self._iconSize.width() + (self._padding * 2)
            height = self._iconSize.height() + (self._padding * 2)

        if len(self.text()) > 0:
            font_metrics = QFontMetrics(self.font())

            self._labelSize.setWidth(font_metrics.width(self.text()))
            self._labelSize.setHeight(font_metrics.height())

            width = width + self._labelSize.width() + self._padding

            if height == 0:
                height = self._labelSize.height() + self._padding * 2

        self._size.setWidth(width)
        self._size.setHeight(height)

    def _show_tooltip(self, text):

        QToolTip.showText(self.mapToGlobal(QPoint(0, self.height())), text)


class Slider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, min_value, max_value, step=None):

        super(Slider, self).__init__()

        if step is None:
            step = 1

        self._value = 0
        self._minValue = min_value
        self._maxValue = max_value
        self._step = step
        self._thumbWidth = 20
        self._thumbRect = QRect()
        self._slidingAreaRect = QRect()

        self._bgColor = QColor(20, 20, 20)
        self._indicatorColor = QColor(30, 108, 125)
        self._thumbColor = QColor(42, 157, 182)

        self._sliding = False

        self._fontMetrics = QFontMetrics(self.font())

        self._update_thumb()

    def value(self):

        return self._value

    def set_value(self, v):

        v = max(self._minValue, min(v, self._maxValue))

        if v != self._value:

            if self._step == 1:

                self._value = int(round(v))

            elif self._step > 1:

                self._value = int(round(utils.snap(v, self._step)))

        self.valueChanged.emit(self._value)

        self._update_thumb()

    def max_value(self):

        return self._maxValue

    def set_max_value(self, v):

        if v < self._minValue:
            v = self._minValue

        self._maxValue = v

    def min_value(self):

        return self._minValue

    def set_min_value(self, v):

        if v > self._maxValue:
            v = self._maxValue

        self._minValue = v

    def step(self):

        return self._step

    def set_step(self, v):

        self._step = v

    def set_thumb_size(self, size):

        self._thumbWidth = size

    def _get_value_from_position(self, pos):

        pos -= self._thumbWidth / 2

        width = self.width()

        size = width - self._thumbWidth

        if pos > size:
            return self._maxValue

        if pos < 0:
            return self._minValue

        percent = pos / size

        return self._minValue + round((self._maxValue - self._minValue) * percent)

    def _update_thumb(self):

        size = self.width() - self._thumbWidth

        height = self.height()

        pos = round(max(0, min(size * ((self._value - self._minValue) /
                                       (self._maxValue - self._minValue)), size)))

        self._thumbRect.setRect(pos, 0, self._thumbWidth, height)

        self.update()

    def sizeHint(self):

        return QSize(200, 25)

    def resizeEvent(self, e):

        self._update_thumb()


    def mousePressEvent(self, e):

        self._sliding = True

        self.set_value(self._get_value_from_position(e.pos()))


    def mouseReleaseEvent(self, e):

        if self._sliding:
            self._sliding = False
            self.update()

    def mouseMoveEvent(self, e):

        if self._sliding:
            mouse_pos = e.pos().x()

            self.set_value(self._get_value_from_position(mouse_pos))


    def wheelEvent(self, e):

        self.set_value(self._value + utils.sign(e.angleDelta().y() > 0) * self._step)


    def paintEvent(self, e):

        painter = QPainter(self)

        draw_rect = e.rect()

        # SLIDER---------------------------------------------------------------------

        # BAR --------

        painter.setPen(self._bgColor.lighter(200))

        painter.drawRect(draw_rect.adjusted(0, 0, -1, -1))

        painter.fillRect(draw_rect.adjusted(1, 1, -1, -1), self._bgColor)

        # THUMB --------

        painter.setPen(self._thumbColor.lighter())

        painter.drawRect(self._thumbRect.adjusted(0, 0, -1, -1))

        painter.fillRect(self._thumbRect.adjusted(1, 1, -1, -1), self._thumbColor)

        # VALUE LABEL --------

        value_text = str(self._value)

        value_label_size = QSize(self._fontMetrics.width(value_text), self._fontMetrics.height())

        value_indicator_rect = QRect(self._thumbRect.right() + 2, self._thumbRect.top(), value_label_size.width() + 10,
                                     self._thumbRect.height())

        if value_indicator_rect.right() > draw_rect.right():
            value_indicator_rect.setRect(self._thumbRect.left() - value_indicator_rect.width() - 1,
                                         value_indicator_rect.top(), value_indicator_rect.width(),
                                         value_indicator_rect.height())

        painter.setPen(self._indicatorColor.lighter())

        painter.drawRect(value_indicator_rect.adjusted(0, 0, -1, -1))

        painter.fillRect(value_indicator_rect.adjusted(1, 1, -1, -1), self._indicatorColor)

        painter.setPen(Qt.white)

        painter.drawText(value_indicator_rect.left() + value_indicator_rect.width() / 2 - value_label_size.width() / 2,
                   value_indicator_rect.top() + value_indicator_rect.height() / 2 + value_label_size.height() / 3,
                   value_text)


class OnOffButton(QPushButton):
    def __init__(self):

        super(OnOffButton, self).__init__()

        self.setCheckable(True)

        self.toggled.connect(self._on_toggle)

    def _on_toggle(self):

        if self.isChecked():

            self.setText('ON')

        else:

            self.setText('OFF')
