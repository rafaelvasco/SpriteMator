# ------------------------------------------------------------------------------
# Name:        ColorPicker
# Purpose:     Represents a palette based color picker;
#
# Author:      Rafael Vasco
#
# Created:     29/04/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, QSize, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QBrush, QPen, QPainter, QColor, QLinearGradient, QPolygon, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

import src.utils as utils


ColorIndex = utils.enum('Primary', 'Secondary')


class ColorBox(QWidget):
    mouseClicked = pyqtSignal(int)

    def __init__(self, color_a=None, color_b=None):
        super(ColorBox, self).__init__()

        self._previewColor = None
        self._primaryColor = QColor(color_a)
        self._secondaryColor = QColor(color_b)
        self._activeColorIndex = ColorIndex.Primary
        self._background = utils.generate_checkerboard_tile(8,
                                                            QColor(150, 150, 150),
                                                            QColor(175, 175, 175))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    @property
    def primary_color(self):
        return self._primaryColor

    @primary_color.setter
    def primary_color(self, value):
        if self._primaryColor is None:
            self._primaryColor = QColor()

        self._primaryColor.setRgba(value.rgba())

    @property
    def secondary_color(self):
        return self._secondaryColor

    @secondary_color.setter
    def secondary_color(self, value):
        if self._secondaryColor is None:
            self._secondaryColor = QColor()

        self._secondaryColor.setRgba(value.rgba())

    @property
    def preview_color(self):
        return self._previewColor

    @preview_color.setter
    def preview_color(self, value):

        if self._previewColor is None:
            self._previewColor = QColor()

        if value is not None:
            self._previewColor.setRgba(value.rgba())
        else:
            self._previewColor = None

    def set_active_color_index(self, index):
        self._activeColorIndex = index

    def mousePressEvent(self, e):

        clicked_pos = e.pos()

        if clicked_pos.x() <= self.rect().width() / 2:
            self._activeColorIndex = 0
            self.update()
            self.mouseClicked.emit(0)
        else:
            self._activeColorIndex = 1
            self.update()
            self.mouseClicked.emit(1)

    def paintEvent(self, e):
        p = QPainter(self)

        paint_rect = e.rect()

        half_width = paint_rect.width() / 2
        paint_rect.adjust(0, 0, -half_width, -2)

        if self._primaryColor:

            if self._primaryColor.alpha() < 255:
                p.drawTiledPixmap(paint_rect, self._background)

            p.fillRect(paint_rect, self._primaryColor)
            if self._activeColorIndex == ColorIndex.Primary:
                p.fillRect(paint_rect.adjusted(0, paint_rect.height(), 0, paint_rect.height() + 2),
                           QColor("red"))

        if self._secondaryColor:

            second_box_rect = paint_rect.translated(half_width, 0)

            if self._primaryColor.alpha() < 255:
                p.drawTiledPixmap(second_box_rect, self._background)

            p.fillRect(second_box_rect, self._secondaryColor)
            if self._activeColorIndex == ColorIndex.Secondary:
                p.fillRect(paint_rect.adjusted(paint_rect.width(), paint_rect.height(),
                                               paint_rect.width(),
                                               paint_rect.height() + 2), QColor("red"))

        if self._previewColor:

            if self._activeColorIndex == ColorIndex.Primary:
                p.fillRect(paint_rect, self._previewColor)
            else:
                p.fillRect(paint_rect.translated(half_width, 0), self._previewColor)

    def sizeHint(self):

        return QSize(223, 17)


# -----------------------------------------------------------------------------


class ColorRamp:
    @staticmethod
    def black_white():
        bw = ColorRamp()
        bw._hueArray[:] = []
        bw._satArray[:] = []
        bw._valArray[:] = []

        for i in range(0, 16):
            value = min((16 * (16 - i)), 255)
            bw._colArray[i].setHsv(0, 0, value)

        bw._colArray[0].setHsv(0, 0, 255)
        bw._colArray[15].setHsv(0, 0, 0)

        return bw

    def __init__(self, hue=None, base_sat=None):

        self._hue = hue or 0
        self._baseSat = base_sat or 0
        self._hueShift = 0

        self._prevIndex = 0
        self._hueArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._satArray = [7, 25, 43, 56, 73, 94, 109, 119, 137, 155, 170, 191, 209, 211, 224, 255]
        self._valArray = [250, 240, 222, 206, 194, 178, 163, 145, 130, 112, 97, 82, 64, 48, 33, 15]
        self._colArray = [None] * 16

        self._calculate_colors()

    @property
    def color_count(self):
        return len(self._colArray)

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, value):
        self._hue = value % 360

    @property
    def base_saturation(self):
        return self._baseSat

    @base_saturation.setter
    def base_saturation(self, value):
        self._baseSat = max(-50, min(value, 50))
        self._calculate_colors()

    @property
    def hue_shift(self):
        return self._hueShift

    @hue_shift.setter
    def hue_shift(self, value):
        self._hueShift = max(0, min(value, 50))
        self._calculate_colors()

    def color_at(self, index):

        index = max(0, min(index, 15))
        return self._colArray[index]

    def set_color_at(self, index, color):

        if self._colArray[index] is None:
            self._colArray[index] = QColor()
        self._colArray[index].setRgb(color.rgb())

    def shift_hue(self, delta):

        self._hueShift = self._hueShift + delta

    def _calculate_colors(self):

        for i in range(0, 16):
            self._hueArray[i] = abs((self._hue - self._hueShift * (i - 8)) % 360)
            shift = (8 - abs(i - 7)) * self._baseSat / 8

            new_sat = self._satArray[i] + shift
            new_val = self._valArray[i] + shift
            new_sat = max(0, min(255, new_sat))
            new_val = max(0, min(255, new_val))

            self._colArray[i] = (QColor.fromHsv(self._hueArray[i], new_sat, new_val))

        first_color = self._colArray[15]
        last_color = self._colArray[0]

        first_color.setHsv(0, 0, 0)
        last_color.setHsv(0, 0, 255)


# -----------------------------------------------------------------------------


class PaletteCell(object):
    def __init__(self, index):
        self.index = index

    def add_to_index(self, v):
        self.index += v


# -----------------------------------------------------------------------------


class ColorPalette(QWidget):
    colorHovered = pyqtSignal(QColor)
    colorSelected = pyqtSignal(QColor, int)
    mouseLeave = pyqtSignal()

    def __init__(self):

        super(ColorPalette, self).__init__()
        self._ramps = []
        self._cellSize = 13
        self._cellIndicatorSize = 2
        self._wheelColorShiftActive = False
        self._wheelRampShiftActive = False
        self._initialize_ramps()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._rampIndex = 0
        self._hoveredCellIndex = -1

        self._selectedCellA2 = PaletteCell(index=0)
        self._selectedCellB2 = PaletteCell(index=15)

        self._activeCell = self._selectedCellA2
        self._primaryIndicatorColor = QColor(0, 245, 255)
        self._secondaryIndicatorColor = QColor(255, 145, 0)
        self._locked = True

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value

    @property
    def cell_size(self):
        return self._cellSize

    @cell_size.setter
    def cell_size(self, value):

        if self._cellSize != value:

            self._cellSize = value

            for ramp in self._ramps:
                ramp.set_cell_size(value)

    def color_at(self, cell):

        ramp_index = self._cell_to_ramp_index(cell)
        col_index = int(cell % 16)

        return self._ramps[ramp_index].color_at(15 - col_index)

    def switch_slot(self):

        if self._activeCell == self._selectedCellA2:

            self._activeCell = self._selectedCellB2

        else:

            self._activeCell = self._selectedCellA2

        self._rampIndex = self._cell_to_ramp_index(self._activeCell.index)

        self.update()

    def move_color_selection(self, delta):

        self._activeCell.add_to_index(delta)

        self._activeCell.index = (max(16 * self._rampIndex,
                                      min(self._activeCell.index, 16 * self._rampIndex + 15)))

        if self._activeCell == self._selectedCellA2:

            self.colorSelected.emit(self.color_at(self._activeCell.index), 0)

        elif self._activeCell == self._selectedCellB2:

            self.colorSelected.emit(self.color_at(self._activeCell.index), 1)

    def move_ramp_selection(self, delta):

        delta = -delta

        self._rampIndex += delta

        self._rampIndex = max(0, min(self._rampIndex, 15))

        if 0 <= self._activeCell.index + delta * 16 < 256:

            self._activeCell.add_to_index(delta * 16)

            if self._activeCell == self._selectedCellA2:

                self.colorSelected.emit(self.color_at(self._activeCell.index), 0)

            elif self._activeCell == self._selectedCellB2:

                self.colorSelected.emit(self.color_at(self._activeCell.index), 1)

    def mouseMoveEvent(self, e):

        mouse_pos = e.pos()

        hovered_cell = max(0, min(self._cell_index(mouse_pos), 255))

        if self._hoveredCellIndex != hovered_cell:
            self._hoveredCellIndex = hovered_cell
            self.colorHovered.emit(self.color_at(hovered_cell))

    def enterEvent(self, e):

        self.setFocus()

    def mousePressEvent(self, e):

        if self._hoveredCellIndex == -1:
            return

        selected_color = self.color_at(self._hoveredCellIndex)

        self._rampIndex = self._cell_to_ramp_index(self._hoveredCellIndex)

        if e.button() == Qt.LeftButton:

            self._activeCell = self._selectedCellA2

            self.colorSelected.emit(selected_color, 0)

            self.update()

        elif e.button() == Qt.RightButton:

            self._activeCell = self._selectedCellB2

            self.colorSelected.emit(selected_color, 1)

            self.update()

        self._activeCell.index = self._hoveredCellIndex

    def paintEvent(self, e):

        p = QPainter(self)

        cell_rect = QRect()

        ramp_count = len(self._ramps)

        col_count = self._ramps[0].color_count

        index = 0
        ramp_index = 0

        for ramp in self._ramps:

            for i in range(0, col_count):
                cell_rect.setRect(i * (self._cellSize + 1),
                                  (index // ramp_count) * (self._cellSize + 1),
                                  self._cellSize, self._cellSize)
                p.fillRect(cell_rect, ramp.color_at(col_count - 1 - i))

                index += 1

            ramp_index += 1

        pen = QPen()

        pen.setWidth(self._cellIndicatorSize)
        pen.setJoinStyle(Qt.MiterJoin)

        border_adjust = self._cellIndicatorSize / 2

        # PAINT SELECTED CELL A

        pen.setColor(self._primaryIndicatorColor)
        p.setPen(pen)

        cell_rect = self._cell_rect(self._selectedCellA2.index)

        p.drawRect(cell_rect.adjusted(border_adjust,
                                      border_adjust,
                                      -border_adjust,
                                      -border_adjust))

        # PAINT SELECTED CELL B

        pen.setColor(self._secondaryIndicatorColor)
        p.setPen(pen)

        cell_rect = self._cell_rect(self._selectedCellB2.index)

        p.drawRect(cell_rect.adjusted(border_adjust,
                                      border_adjust,
                                      -border_adjust,
                                      -border_adjust))

    def leaveEvent(self, e):

        self.mouseLeave.emit()
        self._hoveredCellIndex = -1

    @staticmethod
    def _cell_to_ramp_index(cell):

        return int(max(0, min(cell // 16, 15)))

    def _cell_rect(self, index):

        return QRect(((index - 16 * (index // 16)) * (self._cellSize + 1)),
                     (index // 16) * (self._cellSize + 1),
                     self._cellSize, self._cellSize)

    def _cell_index(self, mouse_pos):

        return (mouse_pos.y() // (self._cellSize + 1)) * 16 + \
               (mouse_pos.x() // (self._cellSize + 1))

    def _initialize_ramps(self):

        self._ramps.append(ColorRamp.black_white())
        self._ramps.append(ColorRamp())
        self._ramps.append(ColorRamp(17, 50))
        self._ramps.append(ColorRamp(33, 50))
        self._ramps.append(ColorRamp(47, 50))
        self._ramps.append(ColorRamp(60, 50))
        self._ramps.append(ColorRamp(78, 50))
        self._ramps.append(ColorRamp(96, 50))
        self._ramps.append(ColorRamp(108, 50))
        self._ramps.append(ColorRamp(180, 50))
        self._ramps.append(ColorRamp(207, 50))
        self._ramps.append(ColorRamp(240, 50))
        self._ramps.append(ColorRamp(252, 50))
        self._ramps.append(ColorRamp(265, 50))
        self._ramps.append(ColorRamp(285, 50))
        self._ramps.append(ColorRamp(300, 50))

    def sizeHint(self):

        return QSize(223, 223)


# -----------------------------------------------------------------------------


class ColorSlider(QWidget):
    Orientation = utils.enum('HORIZONTAL', 'VERTICAL')

    valueChanged = pyqtSignal(int)

    pickerPoly = QPolygon([

        QPoint(0, 13),
        QPoint(16, 13),
        QPoint(8, 0)

    ])

    def __init__(self, min_value, max_value, alpha=None):
        super(ColorSlider, self).__init__()

        self._value = min_value
        self._minValue = min_value
        self._maxValue = max_value
        self._pickerWidth = 8
        self._sliding = False
        self._pickRect = QRect()
        self._slideStep = 10
        self._orientation = self.Orientation.HORIZONTAL
        self._label = ""
        self._gradient = None

        self._pickerPixmap = None
        self._background = None

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._update_gradient()
        self._update_picker_position()
        self._generate_picker()

        if alpha is not None:
            self._background = utils.generate_checkerboard_tile(8,
                                                                QColor(150, 150, 150),
                                                                QColor(175, 175, 175))

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        value = max(self._minValue, min(value, self._maxValue))

        if value != self._value:
            self._value = int(round(value))

        self._update_picker_position()
        self.update()

    @property
    def max_value(self):
        return self._maxValue

    @max_value.setter
    def max_value(self, value):

        if value < self._minValue:
            value = self._minValue

        self._maxValue = value

    @property
    def step(self):
        return self._slideStep

    @step.setter
    def step(self, value):
        self._slideStep = value

    @property
    def start_color(self):
        return self._gradient.getColorAt(0.0)

    @start_color.setter
    def start_color(self, value):
        self._gradient.setColorAt(0.0, value)

    @property
    def end_color(self):
        return self._gradient.getColorAt(1.0)

    @end_color.setter
    def end_color(self, value):
        self._gradient.setColorAt(1.0, value)

    def _update_gradient(self):

        if self._gradient is None:
            self._gradient = QLinearGradient()
            self._gradient.setStart(0, 0)

        if self._orientation == self.Orientation.HORIZONTAL:

            self._gradient.setFinalStop(self.width(), 0)

        else:

            self._gradient.setFinalStop(0, self.height())

    def set_color_at(self, pos, color):

        pos = max(0, min(pos, 1))

        self._gradient.setColorAt(pos, color)

    def _position_to_value(self, pos):

        pos -= self._pickerWidth / 2.0

        size = float(self.width()) - self._pickerWidth if \
            self._orientation == self.Orientation.HORIZONTAL else \
            float(self.height()) - self._pickerWidth

        if self._orientation == self.Orientation.VERTICAL:
            pos = round(size - pos)

        if pos > size:
            return self._maxValue

        if pos < 0:
            return self._minValue

        percent = float(pos) / float(size)

        return round((self._maxValue - self._minValue) * percent)

    def _update_picker_position(self):

        size = float(self.width()) - self._pickerWidth \
            if self._orientation == self.Orientation.HORIZONTAL \
            else float(self.height()) - self._pickerWidth

        pos = round(max(0, min(size * (float(self._value - self._minValue) /
                                       float(self._maxValue - self._minValue)), size)))

        if self._orientation == self.Orientation.VERTICAL:
            pos = round(size - pos)

        if self._orientation == self.Orientation.HORIZONTAL:

            self._pickRect = QRect(pos, 13, self._pickerWidth, 18)

        else:

            self._pickRect = QRect(13, pos, self._pickerWidth, 18)

    def _generate_picker(self):

        image = QImage(8, 18, QImage.Format_ARGB32_Premultiplied)

        image.fill(Qt.transparent)

        p = QPainter()

        p.begin(image)

        pen = QPen(Qt.black)
        pen.setWidth(2)

        p.setPen(pen)

        p.setBrush(Qt.white)

        rect = QRect(0, 0, 8, 18)

        p.drawRect(rect)

        p.end()

        self._pickerPixmap = QPixmap.fromImage(image)

    def sizeHint(self):

        return QSize(223, 30)

    def mousePressEvent(self, e):

        self._sliding = True

        mouse_pos = e.pos().x() if self._orientation == self.Orientation.HORIZONTAL else \
            e.pos().y()

        self.value = self._position_to_value(mouse_pos)

        self.valueChanged.emit(self._value)

    def mouseReleaseEvent(self, e):

        if self._sliding:
            self._sliding = False
            self.update()

    def mouseMoveEvent(self, e):

        if not self._sliding:
            return

        self.value = self._position_to_value(e.pos().x())

        self.valueChanged.emit(self._value)

    def wheelEvent(self, e):

        self.value = self._value + utils.sign(e.angleDelta().y()) * self._slideStep

        self.valueChanged.emit(self._value)

    def resizeEvent(self, e):

        self._update_picker_position()
        self._update_gradient()

    def paintEvent(self, e):

        p = QPainter(self)

        # Paint border

        bar_rect = self.rect().adjusted(0, 15, 0, -1)

        if self._background is not None:
            p.drawTiledPixmap(bar_rect, self._background)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(1)

        p.setPen(pen)

        bar_rect.adjust(0, 0, -1, 0)

        p.drawRect(bar_rect)

        p.setPen(Qt.white)

        # Paint Spectrum

        bar_rect.adjust(1, 1, 0, 0)

        p.fillRect(bar_rect, QBrush(self._gradient))

        # Paint Picker

        p.drawPixmap(self._pickRect, self._pickerPixmap)

        # Draw Label

        label_rect = QRect(200, 1, 20, 15)

        p.drawText(label_rect, Qt.AlignRight, str(self._value))

        if len(self._label) > 0:
            label_rect.adjust(-200, 0, 0, 0)
            p.drawText(label_rect, Qt.AlignLeft, self._label)


# -----------------------------------------------------------------------------


class ColorPicker(QWidget):
    primaryColorChanged = pyqtSignal(QColor)
    secondaryColorChanged = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(ColorPicker, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._primarySelectedColor = QColor()
        self._secondarySelectedColor = QColor()

        self._activeColorIndex = ColorIndex.Primary

        self._controlPressed = False
        self._altPressed = False

        self._palette = ColorPalette()

        # Initialize Sliders

        self._hueSlider = ColorSlider(0, 359)
        self._hueSlider.set_color_at(0.0, QColor(255, 0, 0))
        self._hueSlider.set_color_at(0.16, QColor(255, 255, 0))
        self._hueSlider.set_color_at(0.33, QColor(0, 255, 0))
        self._hueSlider.set_color_at(0.5, QColor(0, 255, 255))
        self._hueSlider.set_color_at(0.76, QColor(0, 0, 255))
        self._hueSlider.set_color_at(0.85, QColor(255, 0, 255))
        self._hueSlider.set_color_at(1.0, QColor(255, 0, 0))

        self._hueSlider.label = 'Hue'

        self._satSlider = ColorSlider(0, 255)
        self._satSlider.label = 'Saturation'

        self._valSlider = ColorSlider(0, 255)
        self._valSlider.label = 'Value'
        self._valSlider.start_color = QColor("black")

        self._redSlider = ColorSlider(0, 255)
        self._redSlider.label = 'Red'

        self._redSlider.start_color = QColor("black")
        self._redSlider.end_color = QColor("red")

        self._greenSlider = ColorSlider(0, 255)
        self._greenSlider.label = 'Green'

        self._greenSlider.start_color = QColor("black")
        self._greenSlider.end_color = QColor("green")

        self._blueSlider = ColorSlider(0, 255)
        self._blueSlider.label = 'Blue'

        self._blueSlider.start_color = QColor("black")
        self._blueSlider.end_color = QColor("blue")

        self._alphaSlider = ColorSlider(0, 255)
        self._alphaSlider.label = 'Alpha'

        self._alphaSlider.start_color = QColor("black")
        self._alphaSlider.end_color = QColor("black")
        self._alphaSlider.value = 255

        # Initialize Color Box
        self._colorBox = ColorBox(self._primarySelectedColor, self._secondarySelectedColor)

        # Set Initial Colors

        self.primary_color = QColor('black')

        self.secondary_color = QColor('white')

        # Initialize Layout

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._palette)
        self._layout.addWidget(self._colorBox)
        self._layout.addWidget(self._hueSlider)
        self._layout.addWidget(self._satSlider)
        self._layout.addWidget(self._valSlider)
        self._layout.addWidget(self._redSlider)
        self._layout.addWidget(self._greenSlider)
        self._layout.addWidget(self._blueSlider)
        self._layout.addWidget(self._alphaSlider)

        self.setLayout(self._layout)

        # Initialize Events

        self._init_events()

        # Set Style

        self.setStyleSheet("background-color: #333")

    # ========== PUBLIC API =======================================================================

    @property
    def primary_color(self):
        return self._primarySelectedColor

    @primary_color.setter
    def primary_color(self, value):

        if self._primarySelectedColor is None:
            self._primarySelectedColor = QColor()

        self._primarySelectedColor.setRgba(value.rgba())
        self._on_primary_color_changed(update_alpha_value=True)

        self._primarySelectedColor = value

    @property
    def secondary_color(self):
        return self._secondarySelectedColor

    @secondary_color.setter
    def secondary_color(self, value):

        if self._secondarySelectedColor is None:
            self._secondarySelectedColor = QColor()

        self._secondarySelectedColor.setRgba(value.rgba())
        self._on_secondary_color_changed(update_alpha_value=True)

        self._secondarySelectedColor = value

    def set_color_hue(self, h, color_index=None):

        color_index = color_index or ColorIndex.Primary

        store_alpha = self._primarySelectedColor.alpha()

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setHsv(h, self._primarySelectedColor.saturation(),
                                              self._primarySelectedColor.value())
            self._primarySelectedColor.setAlpha(store_alpha)

            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setHsv(h, self._secondarySelectedColor.saturation(),
                                                self._secondarySelectedColor.value())
            self._secondarySelectedColor.setAlpha(store_alpha)

            self._on_secondary_color_changed()

    def set_color_saturation(self, s, color_index=None):

        color_index = color_index or ColorIndex.Primary

        store_alpha = self._primarySelectedColor.alpha()

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setHsv(self._primarySelectedColor.hue(),
                                              s,
                                              self._primarySelectedColor.value())
            self._primarySelectedColor.setAlpha(store_alpha)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setHsv(self._secondarySelectedColor.hue(), s,
                                                self._secondarySelectedColor.value())
            self._secondarySelectedColor.setAlpha(store_alpha)
            self._on_secondary_color_changed(update_alpha_value=False)

    def set_color_value(self, v, color_index=None):

        color_index = color_index or ColorIndex.Primary

        store_alpha = self._primarySelectedColor.alpha()

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setHsv(self._primarySelectedColor.hue(),
                                              self._primarySelectedColor.saturation(),
                                              v)
            self._primarySelectedColor.setAlpha(store_alpha)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setHsv(self._secondarySelectedColor.hue(),
                                                self._secondarySelectedColor.saturation(), v)
            self._secondarySelectedColor.setAlpha(store_alpha)
            self._on_secondary_color_changed(update_alpha_value=False)

    def set_color_red(self, r, color_index=None):

        color_index = color_index or ColorIndex.Primary

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setRed(r)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setRed(r)
            self._on_secondary_color_changed(update_alpha_value=False)

    def set_color_green(self, g, color_index=None):

        color_index = color_index or ColorIndex.Primary

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setGreen(g)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setGreen(g)
            self._on_secondary_color_changed(update_alpha_value=False)

    def set_color_blue(self, b, color_index=None):

        color_index = color_index or ColorIndex.Primary

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setBlue(b)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setBlue(b)
            self._on_secondary_color_changed(update_alpha_value=False)

    def set_color_alpha(self, a, color_index=None):

        color_index = color_index or ColorIndex.Primary

        if color_index == ColorIndex.Primary:

            self._primarySelectedColor.setAlpha(a)
            self._on_primary_color_changed(update_alpha_value=False)

        elif color_index == ColorIndex.Secondary:

            self._secondarySelectedColor.setAlpha(a)
            self._on_secondary_color_changed(update_alpha_value=False)

    def select_next_color_on_palette(self):

        self._palette.move_color_selection(1)

    def select_previous_color_on_palette(self):

        self._palette.move_color_selection(-1)

    def select_next_ramp_on_palette(self):

        self._palette.move_ramp_selection(1)

    def select_previous_ramp_on_palette(self):

        self._palette.move_ramp_selection(-1)

    def switch_active_color(self):

        if self._activeColorIndex == ColorIndex.Primary:
            self._activeColorIndex = ColorIndex.Secondary

        else:
            self._activeColorIndex = ColorIndex.Primary

        self._colorBox.set_active_color_index(self._activeColorIndex)
        self._palette.switch_slot()

        self.update()

    def _init_events(self):

        self._palette.colorHovered.connect(self._on_palette_color_hovered)
        self._palette.colorSelected.connect(self._on_palette_color_changed)
        self._palette.mouseLeave.connect(self.on_palette_mouse_leave)

        self._hueSlider.valueChanged.connect(self._on_hue_slider_value_changed)
        self._satSlider.valueChanged.connect(self._on_sat_slider_value_changed)
        self._valSlider.valueChanged.connect(self._on_val_slider_value_changed)

        self._redSlider.valueChanged.connect(self._on_red_slider_value_changed)
        self._greenSlider.valueChanged.connect(self._on_green_slider_value_changed)
        self._blueSlider.valueChanged.connect(self._on_blue_slider_value_changed)

        self._alphaSlider.valueChanged.connect(self._on_alpha_slider_value_changed)

        self._colorBox.mouseClicked.connect(self._on_color_box_clicked)

    def _update_sliders(self, update_alpha_value=None):
        color = (self._primarySelectedColor
                 if self._activeColorIndex == ColorIndex.Primary
                 else self._secondarySelectedColor)

        # HUE
        self._hueSlider.value = color.hue()

        # SATURATION

        self._satSlider.start_color = QColor.fromHsv(color.hue(), 0, color.value())
        self._satSlider.end_color = QColor.fromHsv(color.hue(), 255, color.value())
        self._satSlider.value = color.saturation()

        # VALUE

        self._valSlider.end_color = QColor.fromHsv(color.hue(), color.saturation(), 255)
        self._valSlider.value = color.value()

        # RGB

        self._redSlider.value = color.red()
        self._greenSlider.value = color.green()
        self._blueSlider.value = color.blue()

        # ALPHA

        alpha_color = QColor(color)

        alpha_color.setAlpha(0)
        self._alphaSlider.start_color = alpha_color

        alpha_color.setAlpha(255)
        self._alphaSlider.end_color = alpha_color

        if update_alpha_value:
            self._alphaSlider.value = color.alpha()

    def _on_primary_color_changed(self, update_alpha_value=None):

        self._colorBox.primary_color = self._primarySelectedColor

        self._update_sliders(update_alpha_value)

        self.update()

        self.primaryColorChanged.emit(self._primarySelectedColor)

    def _on_secondary_color_changed(self, update_alpha_value=None):

        self._colorBox.secondary_color = self._secondarySelectedColor

        self._update_sliders(update_alpha_value)

        self.update()

        self.secondaryColorChanged.emit(self._secondarySelectedColor)

    def _on_palette_color_hovered(self, color):

        self._colorBox.preview_color = color
        self.update()

    def on_palette_mouse_leave(self):

        self._colorBox.preview_color = None
        self.update()

    def _on_palette_color_changed(self, color, color_index):

        if color_index == ColorIndex.Primary:
            self._activeColorIndex = ColorIndex.Primary
            self.primary_color = color
            self._colorBox.set_active_color_index(ColorIndex.Primary)

        elif color_index == ColorIndex.Secondary:
            self._activeColorIndex = ColorIndex.Secondary
            self.secondary_color = color
            self._colorBox.set_active_color_index(ColorIndex.Secondary)

    def _on_hue_slider_value_changed(self, value):

        self.set_color_hue(value, self._activeColorIndex)

    def _on_sat_slider_value_changed(self, value):

        self.set_color_saturation(value, self._activeColorIndex)

    def _on_val_slider_value_changed(self, value):

        self.set_color_value(value, self._activeColorIndex)

    def _on_red_slider_value_changed(self, value):

        self.set_color_red(value, self._activeColorIndex)

    def _on_green_slider_value_changed(self, value):

        self.set_color_green(value, self._activeColorIndex)

    def _on_blue_slider_value_changed(self, value):

        self.set_color_blue(value, self._activeColorIndex)

    def _on_alpha_slider_value_changed(self, value):

        self.set_color_alpha(value, self._activeColorIndex)

    def _on_color_box_clicked(self, color_box_index):

        if color_box_index != self._activeColorIndex:

            if color_box_index == 0:
                self._activeColorIndex = ColorIndex.Primary
            elif color_box_index == 1:
                self._activeColorIndex = ColorIndex.Secondary

            self._palette.switch_slot()
