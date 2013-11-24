# ======================================================================================================================
# Name:             ColorPicker
# Purpose:          Advanced ColorPicker with integrated ColorPalette
#
# Author:           Rafael Vasco
# Date:             29/04/13
# License:          
# ======================================================================================================================


from PyQt4.QtCore import Qt, QSize, QRect, QPoint, pyqtSignal
from PyQt4.QtGui import QBrush, QPen, QWidget, QPainter, QColor, QVBoxLayout, QSizePolicy, \
                        QLinearGradient, QPolygon, QImage, QPixmap, QFont


import src.utils as utils

# ======================================================================================================================


ColorIndex = utils.enum('Primary', 'Secondary')



class ColorBox(QWidget):
    
    mouseClicked = pyqtSignal(int)

    def __init__(self, colorA = None, colorB = None):
        super(ColorBox, self).__init__()

        self._previewColor = QColor()
        self._primaryColor = QColor(colorA)
        self._secondaryColor = QColor(colorB)
        self._activeColorIndex = ColorIndex.Primary
        self._background = utils.generateCheckerTile(8, QColor(150, 150, 150), QColor(175,175,175))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setActiveColorIndex(self, index):
        self._activeColorIndex = index
        
    def primaryColor(self):

        return self._primaryColor

    def setPrimaryColor(self, v):
        print('Color Box set Primary Color')
        if self._primaryColor is None:
            self._primaryColor = QColor()
        
        self._primaryColor.setRgba(v.rgba())

    def secondaryColor(self):

        return self._secondaryColor

    def setSecondaryColor(self, v):
        print('Color Box set Secondary Color')
        if self._secondaryColor is None:
            self._secondaryColor = QColor()
        
        self._secondaryColor.setRgba(v.rgba())
        
    def previewColor(self):

        return self._previewColor

    def setPreviewColor(self, v):
        
        if self._previewColor is None:
            self._previewColor = QColor()
        
        if v is not None:
            self._previewColor.setRgba(v.rgba())
        else:
            self._previewColor = None
    
    def mousePressEvent(self, e):
        
        clickedPos = e.pos()
        
        if clickedPos.x() <= self.rect().width() / 2:
            self._activeColorIndex = 0
            self.update()
            self.mouseClicked.emit(0)
        else:
            self._activeColorIndex = 1
            self.update()
            self.mouseClicked.emit(1)
    
    
    def paintEvent(self, e):

        p = QPainter(self)
        
        paintRect = e.rect()

        halfWidth = paintRect.width() / 2
        paintRect.adjust(0, 0, -halfWidth, -2)

        if self._primaryColor:
            
            if self._primaryColor.alpha() < 255:
                p.drawTiledPixmap(paintRect, self._background)
                
                
            p.fillRect(paintRect, self._primaryColor)
            if self._activeColorIndex == ColorIndex.Primary:
                p.fillRect(paintRect.adjusted(0, paintRect.height(), 0, paintRect.height() + 2), QColor("red"))

        if self._secondaryColor:
            
            secondBoxRect = paintRect.translated(halfWidth, 0)
            
            if self._primaryColor.alpha() < 255:
                p.drawTiledPixmap(secondBoxRect, self._background)
            
            p.fillRect(secondBoxRect, self._secondaryColor)
            if self._activeColorIndex == ColorIndex.Secondary:
                p.fillRect(paintRect.adjusted(paintRect.width(), paintRect.height(), paintRect.width(), paintRect.height() + 2), QColor("red"))

        if self._previewColor:

            if self._activeColorIndex == ColorIndex.Primary:
                p.fillRect(paintRect, self._previewColor)
            else:
                p.fillRect(paintRect.translated(halfWidth, 0), self._previewColor)

    def sizeHint(self):

        return QSize(223,17)

# ======================================================================================================================

class ColorRamp:


    @staticmethod
    def blackWhite():
        blackWhite = ColorRamp()
        blackWhite._hueArray[:] = []
        blackWhite._satArray[:] = []
        blackWhite._valArray[:] = []

        for i in range(0, 16):

            value = min((16 * (16 - i)),255)
            blackWhite._colArray[i].setHsv(0, 0, value)

        return blackWhite

    def __init__(self, hue = None, baseSat = None):

        self._hue = hue or 0
        self._baseSat = baseSat or 0
        self._hueShift = 0

        self._prevIndex = 0
        self._hueArray = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self._satArray = [7,25,43,56,73,94,109,119,137,155,170,191,209,211,224,255]
        self._valArray = [250,240,222,206,194,178,163,145,130,112,97,82,64,48,33,15]
        self._colArray = [None]*16

        self._calculateColors()


    def colorAt(self, index):

        index = max(0, min(index, 15))
        return self._colArray[index]

    def setColorAt(self, index, color):
        
        if self._colArray[index] is None:
            self._colArray[index] = QColor()
        self._colArray[index].setRgb(color.rgb())

    def colorCount(self):

        return len(self._colArray)

    def hue(self):

        return self._hue

    def setHue(self, v):

        self._hue = v % 360

    def baseSaturation(self):

        return self._baseSat

    def setBaseSaturation(self, v):

        self._baseSat = max(-50, min(v, 50))
        self._calculateColors()

    def hueShift(self):

        return self._hueShift

    def setHueShift(self, v):

        self._hueShift = max(0, min(v, 50))

        self._calculateColors()

    def shiftHue(self, delta):

        self.setHueShift(self._hueShift + delta)


    def _calculateColors(self):

        for i in range(0,16):

            self._hueArray[i] = abs((self._hue - self._hueShift * (i-8)) % 360)
            shift = (8 - abs(i-7))*self._baseSat/8

            newSat = self._satArray[i] + shift
            newVal = self._valArray[i] + shift
            newSat = max(0, min(255,newSat))
            newVal = max(0, min(255,newVal))

            self._colArray[i] = (QColor.fromHsv(self._hueArray[i], newSat, newVal))

# ======================================================================================================================

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
        self._initializeRamps()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._rampIndex = 0
        self._hoveredCell = -1
        self._selectedCellA = 0
        self._selectedCellB = 15
        self._activeCell = 0
        self._activeSlot = 0
        self._primaryIndicatorColor = QColor(0,245,255)
        self._secondaryIndicatorColor = QColor(255,145,0)
        self._locked = True
        

    def locked(self):
        return self._locked


    def setLocked(self, v):
        self._locked = v

    def colorAt(self, cell):

        rampIndex = self._cellToRampIndex(cell)
        colIndex = int(cell % 16)

        return self._ramps[rampIndex].colorAt(15 - colIndex)

    def setColor(self, color):
        print('Color Pallete Set Color')
        rampIndex = self._cellToRampIndex(self._activeCell)
        colIndex = self._activeCell % 16

        self._ramps[rampIndex].setColorAt(15 - colIndex, color)

        self.update()

    def cellSize(self):

        return self._cellSize

    def setCellSize(self, v):

        if self._cellSize != v:

            self._cellSize = v

            for ramp in self._ramps:

                ramp.setCellSize(v)

    def switchSlot(self):

        if self._activeCell == self._selectedCellA:
            self._activeCell = self._selectedCellB
            self._rampIndex = self._cellToRampIndex(self._selectedCellB)
        else:
            self._activeCell = self._selectedCellA
            self._rampIndex = self._cellToRampIndex(self._selectedCellA)

        self.update()

    def moveColorSelection(self,delta):



        if self._activeCell == self._selectedCellA:

            self._activeCell += delta

            self._activeCell = max( 16 * self._rampIndex, min(self._activeCell, 16 * self._rampIndex + 15))

            if self._selectedCellA != self._activeCell:

                self.colorSelected.emit(self.colorAt(self._activeCell), 0)
                self._selectedCellA = self._activeCell

        elif self._activeCell == self._selectedCellB:

            self._activeCell += delta

            self._activeCell = max( 16 * self._rampIndex, min(self._activeCell, 16 * self._rampIndex + 15))

            if self._selectedCellB != self._activeCell:

                self.colorSelected.emit(self.colorAt(self._activeCell), 1)
                self._selectedCellB = self._activeCell

    def moveRampSelection(self, delta):

        delta = -delta

        self._rampIndex += delta

        self._rampIndex = max(0, min(self._rampIndex, 15))

        if self._activeCell == self._selectedCellA:

            if self._activeCell + delta*16 >= 0 and self._activeCell + delta*16 < 256:

                self._activeCell += delta*16
                self.colorSelected.emit(self.colorAt(self._activeCell), 0)
                self._selectedCellA = self._activeCell


        elif self._activeCell == self._selectedCellB:

            if self._activeCell + delta*16 >= 0 and self._activeCell + delta*16 < 256:

                self._activeCell += delta*16

                self.colorSelected.emit(self.colorAt(self._activeCell), 1)
                self._selectedCellB = self._activeCell

    def mouseMoveEvent(self, e):
    
        mousePos = e.pos()

        hoveredCell = max(0, min(self._cellIndex(mousePos), 255))

        if self._hoveredCell != hoveredCell:

            self._hoveredCell = hoveredCell
            self.colorHovered.emit(self.colorAt(hoveredCell))

    def enterEvent(self, e):

        self.setFocus()

    def mousePressEvent(self, e):

        if self._hoveredCell == -1: return

        selectedColor = self.colorAt(self._hoveredCell)

        self._activeCell = self._hoveredCell

        self._rampIndex = self._cellToRampIndex(self._activeCell)

        if e.button() == Qt.LeftButton:

            self._selectedCellA = self._activeCell

            self.colorSelected.emit(selectedColor, 0)

            self.update()

        elif e.button() == Qt.RightButton:

            self._selectedCellB = self._activeCell

            self.colorSelected.emit(selectedColor, 1)

            self.update()

    def paintEvent(self, e):

        p = QPainter(self)

        cellRect = QRect()

        rampCount = len(self._ramps)

        colCount = self._ramps[0].colorCount()

        index = 0
        rampIndex = 0

        for ramp in self._ramps:

            for i in range(0,colCount):

                cellRect.setRect(i*(self._cellSize + 1),
                                 (index // rampCount) * (self._cellSize + 1),
                                 self._cellSize, self._cellSize)
                p.fillRect(cellRect, ramp.colorAt(colCount - 1 - i))

                index += 1

            rampIndex += 1

        if self._selectedCellA != -1 or self._selectedCellB != -1:

            pen = QPen()

            pen.setWidth(self._cellIndicatorSize)
            pen.setJoinStyle(Qt.MiterJoin)

            borderAjust = self._cellIndicatorSize / 2


            if self._selectedCellA != -1:

                pen.setColor(self._primaryIndicatorColor)
                p.setPen(pen)

                cellRect = self._cellRect(self._selectedCellA)

                p.drawRect(cellRect.adjusted(borderAjust,
                                                borderAjust,
                                                -borderAjust,
                                                -borderAjust))

            if self._selectedCellB != -1:



                pen.setColor(self._secondaryIndicatorColor)
                p.setPen(pen)

                cellRect = self._cellRect(self._selectedCellB)

                p.drawRect(cellRect.adjusted(borderAjust,
                                                borderAjust,
                                                -borderAjust,
                                                -borderAjust))

                

    def leaveEvent(self, e):

        self.mouseLeave.emit()
        self._hoveredCell = -1

    def _cellToRampIndex(self, cell):

        return int(max(0, min(cell // 16, 15)))

    def _cellRect(self, index):

        return QRect(((index - 16 * (index // 16)) * (self._cellSize + 1)) ,
                     (index // 16) * (self._cellSize + 1),
                     self._cellSize, self._cellSize )

    def _cellIndex(self, mousePos):

        return ( (mousePos.y() // (self._cellSize + 1))*16 + (mousePos.x() // (self._cellSize + 1)) )

    def _initializeRamps(self):

        self._ramps.append(ColorRamp.blackWhite())
        self._ramps.append(ColorRamp())
        self._ramps.append(ColorRamp(17))
        self._ramps.append(ColorRamp(33))
        self._ramps.append(ColorRamp(47))
        self._ramps.append(ColorRamp(60))
        self._ramps.append(ColorRamp(78))
        self._ramps.append(ColorRamp(96))
        self._ramps.append(ColorRamp(108))
        self._ramps.append(ColorRamp(180))
        self._ramps.append(ColorRamp(207))
        self._ramps.append(ColorRamp(240))
        self._ramps.append(ColorRamp(252))
        self._ramps.append(ColorRamp(265))
        self._ramps.append(ColorRamp(285))
        self._ramps.append(ColorRamp(300))

    def sizeHint(self):

        return QSize(223,223)

# ======================================================================================================================

class ColorSlider(QWidget):


    Orientation = utils.enum('HORIZONTAL', 'VERTICAL')

    valueChanged = pyqtSignal(int)

    pickerPoly = QPolygon([

        QPoint(0, 13),
        QPoint(16, 13),
        QPoint(8, 0)

    ])


    @staticmethod
    def hueSlider():

        fullSpectrumSlider = ColorSlider(0,359)

        fullSpectrumSlider.setColorAt(0.0, QColor(255,0,0))
        fullSpectrumSlider.setColorAt(0.16, QColor(255,255,0))
        fullSpectrumSlider.setColorAt(0.33, QColor(0,255,0))
        fullSpectrumSlider.setColorAt(0.5, QColor(0,255,255))
        fullSpectrumSlider.setColorAt(0.76, QColor(0,0,255))
        fullSpectrumSlider.setColorAt(0.85, QColor(255,0,255))
        fullSpectrumSlider.setColorAt(1.0, QColor(255,0,0))


        return fullSpectrumSlider


    def __init__(self, minValue, maxValue, alpha=None):
        super(ColorSlider, self).__init__()

        self._value = minValue
        self._minValue = minValue
        self._maxValue = maxValue
        self._pickerWidth = 8
        self._sliding = False
        self._pickRect = QRect()
        self._slideStep = 10
        self._orientation = self.Orientation.HORIZONTAL
        self._label = ""
        self._gradient = None
        self._font = QFont()
        self._font.setFamily("flxpixl")
        self._font.setPointSize(12)
        self._pickerPixmap = None
        self._background = None
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._updateGradient()
        self._positionPicker()
        self._generatePicker()
        
        
        
        if alpha is not None:
            self._background = utils.generateCheckerTile(8, QColor(150, 150, 150), QColor(175,175,175))

    def label(self):

        return self._label

    def setLabel(self, v):

        self._label = v

    def value(self):

        return self._value

    def setValue(self, v):

        v = max(self._minValue, min(v, self._maxValue))



        if v != self._value:

            self._value = int(round(v))

        self._positionPicker()
        self.update()

    def maxValue(self):

        return self._maxValue

    def setMaxValue(self, v):

        if v < self._minValue:

            v = self._minValue


        self._maxValue = v

    def minValue(self):

        return self._minValue

    def setMinValue(self, v):

        if v > self._maxValue:

            v = self._maxValue

        self._minValue = v

    def step(self):

        return self._slideStep

    def setStep(self, v):

        self._slideStep = v

    def setColorAt(self, pos, color):


        pos = max(0, min(pos, 1))

        self._gradient.setColorAt(pos, color)

    def setStartColor(self, color):

        self._gradient.setColorAt(0.0, color)

    def setEndColor(self, color):

        self._gradient.setColorAt(1.0, color)

    def _updateGradient(self):

        if self._gradient is None:

            self._gradient = QLinearGradient()
            self._gradient.setStart(0,0)


        if self._orientation == self.Orientation.HORIZONTAL:


            self._gradient.setFinalStop(self.width(), 0)

        else:

            self._gradient.setFinalStop(0, self.height())

    def _positionToValue(self, pos):

        pos -=     self._pickerWidth / 2.0

        size =     float(self.width()) - self._pickerWidth if self._orientation == self.Orientation.HORIZONTAL else \
            float(self.height()) - self._pickerWidth

        if self._orientation == self.Orientation.VERTICAL:

            pos = round(size - pos)

        if pos > size:

            return self._maxValue

        if pos < 0:

            return self._minValue

        percent = float(pos) / float(size)

        return round((self._maxValue - self._minValue) * percent)

    def _positionPicker(self):

        size = float(self.width()) - self._pickerWidth if self._orientation == self.Orientation.HORIZONTAL else \
            float(self.height()) - self._pickerWidth


        pos = round(max(0, min( size * ( float( self._value - self._minValue ) /
                                         float( self._maxValue - self._minValue ) ), size )))


        if self._orientation == self.Orientation.VERTICAL:

            pos = round(size - pos)

        if self._orientation == self.Orientation.HORIZONTAL:

            self._pickRect = QRect(pos, 13, self._pickerWidth, 18)

        else:

            self._pickRect = QRect(13, pos, self._pickerWidth, 18)
    
    
  
    def _generatePicker(self):

        image = QImage(8,18, QImage.Format_ARGB32_Premultiplied)

        image.fill(Qt.transparent)

        p = QPainter()

        p.begin(image)

        pen = QPen(Qt.black)
        pen.setWidth(2)

        p.setPen(pen)

        p.setBrush(Qt.white)

        rect = QRect(0,0,8,18)

        p.drawRect(rect)

        p.end()

        self._pickerPixmap = QPixmap.fromImage(image)

        image = None

    def sizeHint(self):

        return QSize(223,30)

    def mousePressEvent(self, e):

        self._sliding = True

        mousePos =     e.pos().x() if self._orientation == self.Orientation.HORIZONTAL else \
            e.pos().y()


        self.setValue(self._positionToValue(mousePos))


        self.valueChanged.emit(self._value)

    def mouseReleaseEvent(self, e):

        if self._sliding:

            self._sliding = False
            self.update()

    def mouseMoveEvent(self, e):

        if not self._sliding: return


        self.setValue(self._positionToValue(e.pos().x()))

        self.valueChanged.emit(self._value)

    def wheelEvent(self, e):

        self.setValue(self._value + utils.sign(e.delta())*self._slideStep)

        self.valueChanged.emit(self._value)

    def resizeEvent(self, e):

        self._positionPicker()
        self._updateGradient()

    def paintEvent(self, e):

        p = QPainter(self)

        # Paint border

        barRect = self.rect().adjusted(0, 15, 0, -1)
        
        if self._background is not None:
            p.drawTiledPixmap(barRect, self._background)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(1)

        p.setPen(pen)

        barRect.adjust(0, 0, -1, 0)

        p.drawRect(barRect)

        p.setPen(Qt.white)

        # Paint Spectrum

        barRect.adjust(1,1,0,0)

        p.fillRect(barRect, QBrush(self._gradient))

        # Paint Picker

        p.drawPixmap(self._pickRect, self._pickerPixmap)

        # Draw Label


        labelRect = QRect(200, 1, 20, 15)

        p.setFont(self._font)

        p.drawText(labelRect, Qt.AlignRight,  str(self._value))

        if len(self._label) > 0:

            labelRect.adjust(-200, 0, 0, 0)
            p.drawText(labelRect, Qt.AlignLeft, self._label)

# ======================================================================================================================



class ColorPicker(QWidget):

    Instance = None

    primaryColorChanged = pyqtSignal(QColor)
    secondaryColorChanged = pyqtSignal(QColor)




    """docstring for ColorPicker"""
    def __init__(self, parent=None):
        super(ColorPicker, self).__init__(parent)

        ColorPicker.Instance = self

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._primarySelectedColor = QColor()
        self._secondarySelectedColor = QColor()
        

        self._activeColorIndex = ColorIndex.Primary
        
        
        self._controlPressed = False
        self._altPressed = False

        self._palette = ColorPalette()

        # Initialize Sliders

        self._hueSlider = ColorSlider.hueSlider()
        self._hueSlider.setLabel("Hue")


        self._satSlider = ColorSlider(0, 255)
        self._satSlider.setLabel("Saturation")

        self._valSlider = ColorSlider(0, 255)
        self._valSlider.setLabel("Value")
        self._valSlider.setStartColor(QColor("black"))

        self._redSlider = ColorSlider(0, 255)
        self._redSlider.setLabel("Red")
        self._redSlider.setStartColor(QColor("black"))
        self._redSlider.setEndColor(QColor("red"))

        self._greenSlider = ColorSlider(0, 255)
        self._greenSlider.setLabel("Green")
        self._greenSlider.setStartColor(QColor("black"))
        self._greenSlider.setEndColor(QColor("green"))

        self._blueSlider = ColorSlider(0, 255)
        self._blueSlider.setLabel("Blue")
        self._blueSlider.setStartColor(QColor("black"))
        self._blueSlider.setEndColor(QColor("blue"))
        
        self._alphaSlider = ColorSlider(0, 255, True)
        self._alphaSlider.setLabel("Alpha")
        self._alphaSlider.setStartColor(QColor("black"))
        self._alphaSlider.setEndColor(QColor("black"))
        self._alphaSlider.setValue(255)

       

        # Initialize Color Box
        self._colorBox = ColorBox(self._primarySelectedColor, self._secondarySelectedColor)

        # Set Initial Colors

        self.setPrimaryColor(QColor('black'))
        self.setSecondaryColor(QColor('white'))

        # Initialize Layout

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(0,0,0,0)
        # self._layout.setSizeConstraint(QLayout.SetFixedSize)


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

        # Connect Events

        self._connectEvents()

        # Set Style

        self.setStyleSheet("background-color: #333")


    # ========== PUBLIC API =======================================================================

    def primaryColor(self):

        return self._primarySelectedColor

    def secondaryColor(self):

        return self._secondarySelectedColor

    def setPrimaryColor(self, c):
        print('Color Picker Set Primary Color')
        if self._primarySelectedColor is None:
            self._primarySelectedColor = QColor()
        
        self._primarySelectedColor.setRgba(c.rgba())
        self._onPrimaryColorChanged(updateAlphaValue=True)
        
        

    def setSecondaryColor(self, c):
        print('Color Picker Set Secondary Color')
        if self._secondarySelectedColor is None:
            self._secondarySelectedColor = QColor()
        
        self._secondarySelectedColor.setRgba(c.rgba())
        self._onSecondaryColorChanged(updateAlphaValue=True)


    def setColorHue(self, h, colorIndex = None):
        
        print('Color Picker Set Color Hue')
        colorIndex = colorIndex or ColorIndex.Primary
        
        storeAlpha = self._primarySelectedColor.alpha()
        
        if colorIndex == ColorIndex.Primary:
            
            
            self._primarySelectedColor.setHsv(h, self._primarySelectedColor.saturation(), self._primarySelectedColor.value())
            self._primarySelectedColor.setAlpha(storeAlpha)
            
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:
            
            self._secondarySelectedColor.setHsv(h, self._secondarySelectedColor.saturation(), self._secondarySelectedColor.value())
            self._secondarySelectedColor.setAlpha(storeAlpha)
            
            self._onSecondaryColorChanged()


    def setColorSat(self, s, colorIndex = None):
        print('Color Picker Set Color Sat')
        colorIndex = colorIndex or ColorIndex.Primary

        storeAlpha = self._primarySelectedColor.alpha()

        if colorIndex == ColorIndex.Primary:

            self._primarySelectedColor.setHsv(self._primarySelectedColor.hue(), s, self._primarySelectedColor.value())
            self._primarySelectedColor.setAlpha(storeAlpha)
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:

            self._secondarySelectedColor.setHsv(self._secondarySelectedColor.hue(), s, self._secondarySelectedColor.value())
            self._secondarySelectedColor.setAlpha(storeAlpha)
            self._onSecondaryColorChanged(updateAlphaValue=False)


    def setColorVal(self, v, colorIndex = None):
        print('Color Picker Set Color Val')
        colorIndex = colorIndex or ColorIndex.Primary
        
        storeAlpha = self._primarySelectedColor.alpha()
        
        if colorIndex == ColorIndex.Primary:

            self._primarySelectedColor.setHsv(self._primarySelectedColor.hue(), self._primarySelectedColor.saturation(), v)
            self._primarySelectedColor.setAlpha(storeAlpha)
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:

            self._secondarySelectedColor.setHsv(self._secondarySelectedColor.hue(), self._secondarySelectedColor.saturation(), v)
            self._secondarySelectedColor.setAlpha(storeAlpha)
            self._onSecondaryColorChanged(updateAlphaValue=False)


    def setColorRed(self, r, colorIndex = None):
        print('Color Picker Set Color Red')
        colorIndex = colorIndex or ColorIndex.Primary

        if colorIndex == ColorIndex.Primary:

            self._primarySelectedColor.setRed(r)
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:

            self._secondarySelectedColor.setRed(r)
            self._onSecondaryColorChanged(updateAlphaValue=False)


    def setColorGreen(self, g, colorIndex = None):
        print('Color Picker Set Color Green')
        colorIndex = colorIndex or ColorIndex.Primary

        if colorIndex == ColorIndex.Primary:

            self._primarySelectedColor.setGreen(g)
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:

            self._secondarySelectedColor.setGreen(g)
            self._onSecondaryColorChanged(updateAlphaValue=False)



    def setColorBlue(self, b, colorIndex = None):
        print('Color Picker Set Color Blue')
        colorIndex = colorIndex or ColorIndex.Primary

        if colorIndex == ColorIndex.Primary:

            self._primarySelectedColor.setBlue(b)
            self._onPrimaryColorChanged(updateAlphaValue=False)

        elif colorIndex == ColorIndex.Secondary:

            self._secondarySelectedColor.setBlue(b)
            self._onSecondaryColorChanged(updateAlphaValue=False)

    
    
    def setColorAlpha(self, a, colorIndex = None):
        print('Color Picker Set Color Alpha')
        colorIndex = colorIndex or ColorIndex.Primary
        
        if colorIndex == ColorIndex.Primary:
            
            self._primarySelectedColor.setAlpha(a)
            self._onPrimaryColorChanged(updateAlphaValue=False)
        
        elif colorIndex == ColorIndex.Secondary:
            
            self._secondarySelectedColor.setAlpha(a)
            self._onSecondaryColorChanged(updateAlphaValue=False)
            
    def selectNextColorOnPalette(self):

        self._palette.moveColorSelection(1)

    def selectPreviousColorOnPalette(self):

        self._palette.moveColorSelection(-1)

    def selectNextRampOnPalette(self):

        self._palette.moveRampSelection(1)

    def selectPreviousRampOnPalette(self):

        self._palette.moveRampSelection(-1)

    def switchActiveColor(self):

        if self._activeColorIndex == ColorIndex.Primary:
            self._activeColorIndex = ColorIndex.Secondary
            
        else:
            self._activeColorIndex = ColorIndex.Primary
        
        
        self._colorBox.setActiveColorIndex(self._activeColorIndex)
        self._palette.switchSlot()
        
        self.update()

    def _connectEvents(self):

        self._palette.colorHovered.connect(self._onPaletteColorHovered)
        self._palette.colorSelected.connect(self._onPaletteColorChanged)
        self._palette.mouseLeave.connect(self._onPaletteMouseLeave)

        self._hueSlider.valueChanged.connect(self._onHueSliderValueChanged)
        self._satSlider.valueChanged.connect(self._onSatSliderValueChanged)
        self._valSlider.valueChanged.connect(self._onValSliderValueChanged)

        self._redSlider.valueChanged.connect(self._onRedSliderValueChanged)
        self._greenSlider.valueChanged.connect(self._onGreenSliderValueChanged)
        self._blueSlider.valueChanged.connect(self._onBlueSliderValueChanged)
        
        self._alphaSlider.valueChanged.connect(self._onAlphaSliderValueChanged)
        
        self._colorBox.mouseClicked.connect(self._onColorBoxClicked)
        

    def _updateSliders(self, updateAlphaValue=None):
        print('Update Sliders')
        color = (self._primarySelectedColor
                 if self._activeColorIndex == ColorIndex.Primary
                 else self._secondarySelectedColor)

        # HUE
        self._hueSlider.setValue(color.hue())



        # SATURATION

        self._satSlider.setStartColor(QColor.fromHsv(color.hue(), 0, color.value()))
        self._satSlider.setEndColor(QColor.fromHsv(color.hue(), 255, color.value()))
        self._satSlider.setValue(color.saturation())


        # VALUE

        self._valSlider.setEndColor(QColor.fromHsv(color.hue(), color.saturation(), 255))
        self._valSlider.setValue(color.value())



        # RGB


        self._redSlider.setValue(color.red())
        self._greenSlider.setValue(color.green())
        self._blueSlider.setValue(color.blue())
        
        # ALPHA
        
        alphaColor = QColor(color)
        
        alphaColor.setAlpha(0)
        self._alphaSlider.setStartColor(alphaColor)
        
        alphaColor.setAlpha(255)
        self._alphaSlider.setEndColor(alphaColor)
        
        if updateAlphaValue:
        
            self._alphaSlider.setValue(color.alpha())
    
   
        
    
    def _onPrimaryColorChanged(self, updateAlphaValue=None):
        print('Color Picker onPrimaryColor Changed')
        
        print('Color ALPHA: ', self._primarySelectedColor.alpha())
        
        self._colorBox.setPrimaryColor(self._primarySelectedColor)
        
        self._updateSliders(updateAlphaValue)
        
        self.update()
        
        self.primaryColorChanged.emit(self._primarySelectedColor)
    
    def _onSecondaryColorChanged(self, updateAlphaValue=None):
        print('Color Picker onSecondaryColorChanged')
        self._colorBox.setSecondaryColor(self._secondarySelectedColor)
        
        self._updateSliders(updateAlphaValue)
        
        self.update()
        
        self.secondaryColorChanged.emit(self._secondarySelectedColor)
    
    def _onPaletteColorHovered(self, color):

        self._colorBox.setPreviewColor(color)
        self.update()

    def _onPaletteMouseLeave(self):

        self._colorBox.setPreviewColor(None)
        self.update()

    def _onPaletteColorChanged(self, color, colorIndex):

        print('Color Picker onPalette Color Changed')
        if colorIndex == ColorIndex.Primary:
            self.setPrimaryColor(color)
            self._activeColorIndex = ColorIndex.Primary
            self._colorBox.setActiveColorIndex(ColorIndex.Primary)

        elif colorIndex == ColorIndex.Secondary:

            self.setSecondaryColor(color)
            self._activeColorIndex = ColorIndex.Secondary
            self._colorBox.setActiveColorIndex(ColorIndex.Secondary)



    def _onHueSliderValueChanged(self, value):

        self.setColorHue(value, self._activeColorIndex)

    def _onSatSliderValueChanged(self, value):

        self.setColorSat(value, self._activeColorIndex)

    def _onValSliderValueChanged(self, value):

        self.setColorVal(value, self._activeColorIndex)

    def _onRedSliderValueChanged(self, value):

        self.setColorRed(value, self._activeColorIndex)

    def _onGreenSliderValueChanged(self, value):

        self.setColorGreen(value, self._activeColorIndex)

    def _onBlueSliderValueChanged(self, value):

        self.setColorBlue(value, self._activeColorIndex)
    
    def _onAlphaSliderValueChanged(self, value):
        
        self.setColorAlpha(value, self._activeColorIndex)
    
    
    def _onColorBoxClicked(self, colorboxIndex):
        
        if colorboxIndex != self._activeColorIndex:
        
            if colorboxIndex == 0:
                self._activeColorIndex = ColorIndex.Primary
            elif colorboxIndex == 1:
                self._activeColorIndex = ColorIndex.Secondary
            
            self._palette.switchSlot()
    
#