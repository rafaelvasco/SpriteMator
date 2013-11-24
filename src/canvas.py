#--------------------------------------------------
# Name:             Canvas
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             30/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import Qt, pyqtSignal, QPoint
from PyQt4.QtGui import QPainter, QSizePolicy, QColor, QMouseEvent

from src.display import  Display
from src.sprite import Frame
from src.canvas_overlay import CanvasOverlay

import src.utils as Utils
from src import tools, inks
from src.toolbox import ToolBox


    
class Canvas(Display):

    frameChanged = pyqtSignal(Frame)
    colorPicked = pyqtSignal(QColor, QMouseEvent)

    def __init__(self, animationDisplay, parent=None):

        super(Canvas, self).__init__(parent)
        
        
        self._tools = {}
        self._inks = {}
        
        
        self._sprite = None
        self._drawingSurface = None
        self._currentTool = None
        self._primaryInk = None
        self._secondaryInk = None
        self._primaryColor = None
        self._secondaryColor = None
        self._pixelSize = 0
        self._drawGrid = True
        
        
        self._absoluteMousePosition = QPoint()
        self._spriteMousePosition = QPoint()
        self._lastButtonPressed = None
        
        # ======================================
        
        self._loadTools()
        self._loadInks()
        
        self._initializeCanvasState()
        
        self._animationDisplay = animationDisplay
        self._overlaySurface = CanvasOverlay(self)
        self._overlaySurface.turnOff()

        self._toolBox = ToolBox(self)
        self._toolBox.setVisible(False)
        self._initializeToolBox()

        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)

        self.setAttribute(Qt.WA_NoSystemBackground)
    
    
    def primaryColor(self):
        
        return self._primaryColor
    
    def setPrimaryColor(self, color):
        
        self._primaryColor = color
        
    def secondaryColor(self):
        
        return self._secondaryColor
    
    def setSecondaryColor(self, color):
        
        self._secondaryColor = color
    
    def primaryInk(self):
        
        return self._primaryInk
    
    def setPrimaryInk(self, inkName):
        self._primaryInk = self.ink(inkName)
        
    def secondaryInk(self):
        
        return self._secondaryInk
    
    def setSecondaryInk(self, inkName):
        
        self._secondaryInk = self.ink(inkName)
    
    def setCurrentTool(self, name):
        
        self._currentTool = self.tool(name)
    
    def tool(self, name):
        
        return self._tools[name]
    
    def ink(self, name):
        
        return self._inks[name]
    
    def currentLayer(self):
        
        if self.spriteLoaded():

            return self._sprite.currentAnimation().currentFrame().currentSurface()
        
        return None
        
    def currentLayerIndex(self):

        if self.spriteLoaded():

            return self._sprite.currentAnimation().currentFrame().currentSurfaceIndex()
        
        return None
    
    def spriteLoaded(self):
        
        return self._sprite is not None
    
    # ----- PUBLIC API -------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def setSprite(self, sprite):
        
        if self.spriteLoaded():
            self.unloadSprite()
        
        self._toolBox.setVisible(True)
        
        self._sprite = sprite

        super().setObjectSize(sprite.currentAnimation().frameWidth(),
                              sprite.currentAnimation().frameHeight())

        self._animationDisplay.setAnimation(sprite.currentAnimation())

        self._updateDrawingSurface()

        self.frameChanged.emit(self._sprite.currentAnimation().currentFrame())

        self.setCursor(Qt.BlankCursor)

    def unloadSprite(self):
        
        self._toolBox.setVisible(False)
        
        self.resetView()
        self.setObjectSize(0, 0)
        
        self._sprite = None
        self._drawingSurface = None
        
        self.update()
        self.setCursor(Qt.ArrowCursor)

    def addAnimation(self):

        if not self.spriteLoaded():
            return
        
        
        self._sprite.addAnimation()

        self._updateDrawingSurface()
        self._updateOverlaySurface()

        self._animationDisplay.setAnimation(self._sprite.currentAnimation())

        self.frameChanged.emit(self._sprite.currentAnimation().currentFrame())

    def setAnimation(self, index):

        if not self.spriteLoaded():
            return
        
        self._sprite.setAnimation(index)

        self._updateDrawingSurface()
        self._updateOverlaySurface()

        self.frameChanged.emit(self._sprite.currentAnimation().currentFrame())

    def addFrame(self):

        if not self.spriteLoaded():
            return
        
        currentAnimation = self._sprite.currentAnimation()

        currentAnimation.addEmptyFrame(currentAnimation.frameWidth(), currentAnimation.frameHeight())

        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(currentAnimation.currentFrameIndex())

        self.frameChanged.emit(currentAnimation.currentFrame())

    def removeFrame(self, index=None):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.removeFrame(index)

        if animation.frameCount() == 0:

            self.addFrame()

        self._updateDrawingSurface()

        self._animationDisplay.goToFrame(animation.currentFrameIndex())

        self.frameChanged.emit(animation.currentFrame())

    def setFrame(self, index):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.setFrame(index)

        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(index)

        self.frameChanged.emit(animation.currentFrame())

    def goToNextFrame(self):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnLastFrame():
            return

        animation.goToNextFrame()
        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(animation.currentFrameIndex())

        self.frameChanged.emit(animation.currentFrame())

    def goToPreviousFrame(self):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnFirstFrame():
            return

        animation.goToPreviousFrame()
        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(animation.currentFrameIndex())

        self.frameChanged.emit(animation.currentFrame())

    def addLayer(self, sourceImage=None, at=None):

        if not self.spriteLoaded():
            return
        
        
        animation = self._sprite.currentAnimation()
        
        if sourceImage is None:

            width = animation.frameWidth()
            height = animation.frameHeight()
            sourceImage = Utils.createImage(width, height)

        animation.currentFrame().addSurface(sourceImage, at)
        self._updateDrawingSurface()
        self.frameChanged.emit(animation.currentFrame())

    def deleteLayer(self, index):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        animation.currentFrame().deleteSurface(index)
        self._updateDrawingSurface()
        self.frameChanged.emit(animation.currentFrame())

    def setLayer(self, index):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        animation.currentFrame().setSurface(index)
        self._updateDrawingSurface()

    def moveLayer(self, fromIndex, toIndex):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        animation.currentFrame().moveSurface(fromIndex, toIndex)

        self._updateDrawingSurface()

    def clear(self, index=None):

        if not self.spriteLoaded():
            return
        
        animation = self._sprite.currentAnimation()

        if index is None:
            surface = self._drawingSurface
        else:
            surface = animation.currentFrame().surfaceAt(index).image()

        painter = QPainter()
        
        painter.begin(surface)

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(0, 0, surface.width(), surface.height(), Qt.white)

        painter.end()
        
        self.update()

    def resize(self, width, height, index=None):

        pass

    def scale(self, sx, sy, index):

        pass


    # ----- EVENTS -----------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def onDrawObject(self, event, painter):

        if not self.spriteLoaded():
            return

        layers = self._sprite.currentAnimation().currentFrame().surfaces()

        for layer in layers:
            painter.drawImage(0, 0, layer.image())
        
        if self._drawGrid and self._zoom >= 4.0:
            
            
            w = self._drawingSurface.width()
            h = self._drawingSurface.height()
            painter.setPen(QColor(0,0,0,80))
            
            for x in range(0, w):
                #xz = x * self._pixelSize
                painter.drawLine(x, 0, x, h)
                
            for y in range(0, h):
                #yz = y * self._pixelSize
                painter.drawLine(0, y, w, y)  
                    
        
    def resizeEvent(self, e):
        
        self._overlaySurface.resize(self.size())
        self._toolBox.updateSize(self.width(), self.height())
        
    def onDelFrameButtonClicked(self):

        self.removeFrame()

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if not self.spriteLoaded():
            return
        
        self._animationDisplay._startRefreshing()
        
        self._updateMouseState(e)
        
        tool = self._currentTool
        
        tool._processMousePress(self, e)
        
        if tool.isActive():
        
            painter = QPainter()
            
            painter.begin(self._drawingSurface)
            
            
            
            tool.blit(painter, self)
    
            painter.end()

        self.update()

    def mouseMoveEvent(self, e):
        
        super().mouseMoveEvent(e)

        if not self.spriteLoaded():
            return
        
        self._updateMouseState(e)
        
        viewMousePosition = self.viewMousePos()
        
        self._animationDisplay.panTo(-viewMousePosition.x(), -viewMousePosition.y())
        
        tool = self._currentTool
        
        tool._processMouseMove(self, e)
        
        if not self._panning:
        
            if tool.isActive():
                
                painter = QPainter()
            
                painter.begin(self._drawingSurface)
        
                tool.blit(painter, self)
        
                painter.end()
        
        self.update()

    def mouseReleaseEvent(self, e):
        
        if not self.spriteLoaded():
            return
        

        self._animationDisplay._stopRefreshing()

        self._updateMouseState(e)
        
        tool = self._currentTool
        
        tool._processMouseRelease(self, e)
        
        self.update()
        
        super().mouseReleaseEvent(e)
    
    def wheelEvent(self, e):
        
        if not self.spriteLoaded():
            return
        
        super().wheelEvent(e)
        
    def enterEvent(self, e):
        
        if not self.spriteLoaded():
            return
        
        self.setCursor(Qt.BlankCursor)
        self._overlaySurface.turnOn()
       
    def leaveEvent(self, e):
        
        if not self.spriteLoaded():
            return
        
        self.setCursor(Qt.ArrowCursor)
        self._overlaySurface.turnOff()
    
    def _onToolBoxMouseEntered(self):
        
        if not self.spriteLoaded():
            return
        
        self._overlaySurface.turnOff()
    
    def _onToolBoxMouseLeft(self):
         
        if not self.spriteLoaded():
            return
         
        self._overlaySurface.turnOn()
        
    def _onToolBoxToolChanged(self, toolName):
        
        self.setCurrentTool(toolName)
    
    def _onToolBoxPrimaryInkChanged(self, inkName):
        
        self.setPrimaryInk(inkName)
    
    def _onToolBoxSecondaryInkChanged(self, inkName):
        
        self.setSecondaryInk(inkName)
    
    # ---- PRIVATE METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    def _loadTools(self):

        # Default Tools
        
        self._tools['Pen'] = tools.Pen()
        self._tools['Picker'] = tools.Picker()
    
    def _loadInks(self):
        
        # Default Inks
        
        self._inks['Solid'] = inks.Solid()
        self._inks['Eraser'] = inks.Eraser()
    
    def _initializeCanvasState(self):
        
        self._pixelSize = 4
        self._primaryColor = QColor('black')
        self._secondaryColor = QColor('white')
        self._currentTool = self.tool('Pen')
        self._primaryInk = self.ink('Solid')
        self._secondaryInk = self.ink('Eraser')
        
    def _initializeToolBox(self):
        
        self._toolBox.mouseEntered.connect(self._onToolBoxMouseEntered)
        self._toolBox.mouseLeft.connect(self._onToolBoxMouseLeft)
        
        self._toolBox.registerTool(self.tool('Pen'), setAsCurrent=True)
        self._toolBox.registerTool(self.tool('Picker'))
        
        self._toolBox.registerInk(self.ink('Solid'), putOnSlot=1)
        self._toolBox.registerInk(self.ink('Eraser'), putOnSlot=2)
        
        self._toolBox.toolChanged.connect(self._onToolBoxToolChanged)
        self._toolBox.primaryInkChanged.connect(self._onToolBoxPrimaryInkChanged)
        self._toolBox.secondaryInkChanged.connect(self._onToolBoxSecondaryInkChanged)
        
    def _updateMouseState(self, e):
        
        if e.type() == 2  and e.button() is not None:
            
            self._lastButtonPressed = e.button()
            
        
        objectMousePosition = super().objectMousePos()

        objectMousePosition.setX(round(objectMousePosition.x(), 2))
        objectMousePosition.setY(round(objectMousePosition.y(), 2))
        
        
        self._spriteMousePosition.setX(objectMousePosition.x())
        self._spriteMousePosition.setY(objectMousePosition.y())

    def _updateDrawingSurface(self):

        if not self.spriteLoaded():
            return
        
        self._drawingSurface = self._sprite.currentAnimation().currentFrame().currentSurface().image()
        self.update()
        
