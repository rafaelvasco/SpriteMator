#--------------------------------------------------
# Name:             Canvas
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             30/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import Qt, pyqtSignal, QPoint
from PyQt4.QtGui import QPainter, QColor, QSizePolicy, QFont

from src.display import  Display
from src.sprite import Frame
from src.canvas_overlay import CanvasOverlay
from src.toolbox import ToolBox

import src.utils as Utils
from src import tools, inks

class Canvas(Display):

    frameChanged = pyqtSignal(Frame)

    def __init__(self, animationDisplay, parent=None):

        super(Canvas, self).__init__(parent)

        self._currentSprite = None
        self._animationDisplay = animationDisplay
        self._currentDrawingSurface = None
        self._overlaySurface = CanvasOverlay(self)
        
        
        self._currentCompositionMode = QPainter.CompositionMode_SourceOver
        self._painter = QPainter()
        
        self._tools = {}
        self._inks = {}
        
        self._toolBox = ToolBox(self)
        
        self._absoluteMousePosition = QPoint()
        self._spriteMousePosition = QPoint()

        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)
        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        self._loadTools()
        self._loadInks()
        
        self._currentTool = self.tool('Pen')
        
        self._primaryInk = self.ink('Solid')
        self._secondaryInk = self.ink('Eraser')
        
      

    # TODO: Do get sets of Tools and Inks
    
    def currentTool(self):
        
        return self._currentTool

    def primaryInk(self):
        return self._primaryInk

    def secondaryInk(self):
        return self._secondaryInk

    def currentSprite(self):
        return self._currentSprite

    def currentAnimation(self):

        if self._currentSprite is not None:

            return self._currentSprite.currentAnimation()

        return None

    def currentFrame(self):

        if self._currentSprite is not None and self._currentSprite.currentAnimation() is not None:

            return self._currentSprite.currentAnimation().currentFrame()

        return None

    def currentLayer(self):

        if (self._currentSprite is not None and
        self._currentSprite.currentAnimation() is not None and
        self._currentSprite.currentAnimation().currentFrame() is not None):

            return self._currentSprite.currentAnimation().currentFrame().currentSurface()

    def currentLayerIndex(self):

        if (self._currentSprite is not None and
        self._currentSprite.currentAnimation() is not None and
        self._currentSprite.currentAnimation().currentFrame() is not None):

            return self._currentSprite.currentAnimation().currentFrame().currentSurfaceIndex()
    
    
    def tool(self, name):
        
        return self._tools[name]
    
    def ink(self, name):
        
        return self._inks[name]
    
    # ----- PUBLIC API -------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def setSprite(self, sprite):

        if self._currentSprite is not None:
            self.unloadSprite()

        self._currentSprite = sprite


        super().setObjectSize(self._currentSprite.currentAnimation().frameWidth(),
                              self._currentSprite.currentAnimation().frameHeight())

        self._animationDisplay.setAnimation(self._currentSprite.currentAnimation())

        self._updateDrawingSurface()

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

        self.setCursor(Qt.BlankCursor)



    def unloadSprite(self):

        self.resetView()
        self.setObjectSize(0, 0)
        self._currentDrawingSurface = None
        self._currentSprite = None
        self.update()
        
        self.setCursor(Qt.ArrowCursor)

    def addAnimation(self):

        if self._currentSprite is None:
            return

        self._currentSprite.addAnimation()

        self._updateDrawingSurface()
        self._updateOverlaySurface()

        self._animationDisplay.setAnimation(self._currentSprite.currentAnimation())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())


    def setAnimation(self, index):

        if self._currentSprite is None:
            return

        self._currentSprite.setAnimation(index)

        self._updateDrawingSurface()
        self._updateOverlaySurface()

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())



    def addFrame(self):

        if self._currentSprite is None:
            return

        currentAnimation = self._currentSprite.currentAnimation()

        currentAnimation.addEmptyFrame(currentAnimation.frameWidth(), currentAnimation.frameHeight())

        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(self._currentSprite.currentAnimation().currentFrameIndex())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

    def removeFrame(self, index=None):

        if self._currentSprite is None:
            return

        self._currentSprite.currentAnimation().removeFrame(index)

        if self._currentSprite.currentAnimation().frameCount() == 0:

            self.addFrame()

        self._updateDrawingSurface()

        self._animationDisplay.goToFrame(self._currentSprite.currentAnimation().currentFrameIndex())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

    def setFrame(self, index):

        if self._currentSprite is None:
            return

        self._currentSprite.currentAnimation().setFrame(index)

        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(index)

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())



    def goToNextFrame(self):

        if self._currentSprite is None:
            return

        if self._currentSprite.currentAnimation().isOnLastFrame():
            return

        self._currentSprite.currentAnimation().goToNextFrame()
        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(self._currentSprite.currentAnimation().currentFrameIndex())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

    def goToPreviousFrame(self):

        if self._currentSprite is None:
            return

        if self._currentSprite.currentAnimation().isOnFirstFrame():
            return

        self._currentSprite.currentAnimation().goToPreviousFrame()
        self._updateDrawingSurface()

        if not self._animationDisplay.isPlaying():
            self._animationDisplay.goToFrame(self._currentSprite.currentAnimation().currentFrameIndex())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

    def addLayer(self, sourceImage=None, at=None):

        if self._currentSprite is None:
            return

        if sourceImage is None:

            width = self._currentSprite.currentAnimation().frameWidth()
            height = self._currentSprite.currentAnimation().frameHeight()
            sourceImage = Utils.createImage(width, height)

        self._currentSprite.currentAnimation().currentFrame().addSurface(sourceImage, at)
        self._updateDrawingSurface()
        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())


    def deleteLayer(self, index):

        if self._currentSprite is None:
            return

        self._currentSprite.currentAnimation().currentFrame().deleteSurface(index)
        self._updateDrawingSurface()
        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())

    def setLayer(self, index):

        if self._currentSprite is None:
            return

        self._currentSprite.currentAnimation().currentFrame().setSurface(index)
        self._updateDrawingSurface()

    def moveLayer(self, fromIndex, toIndex):

        if self._currentSprite is None:
            return

        self._currentSprite.currentAnimation().currentFrame().moveSurface(fromIndex, toIndex)

        self._updateDrawingSurface()




    def clear(self, index=None):

        if self._currentSprite is None:
            return
        
        if index is None:
            surface = self._currentDrawingSurface
        else:
            surface = self._currentSprite.currentAnimation().currentFrame().surfaceAt(index).image()

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

        if self._currentSprite is None:
            return

        layers = self._currentSprite.currentAnimation().currentFrame().surfaces()

        for layer in layers:
            painter.drawImage(0, 0, layer.image())
        
        
       
        painter.resetMatrix()
        
        self._toolBox.draw(painter)
  
#         painter.drawText(20,20, Test"
#                 .format(self._currentSprite.currentAnimation().name(),
#                         self._currentSprite.currentAnimation().currentFrameIndex(),
#                         self._currentSprite.currentAnimation().currentFrame().currentSurfaceIndex()))
#   
#         painter.drawText(10, 70, "Current Layer Stack: ")
#   
#         layers = self.currentFrame().surfaces()
#         index = 0
#         for layer in layers:
#   
#             painter.drawText( 10, 20 * (index) + 100, "Index: " + str(index) + ", Name: " + layer.name())
#             index += 1
            
        
        
    def resizeEvent(self, e):
        
        self._overlaySurface.resize(self.size())
        
    def onDelFrameButtonClicked(self):

        self.removeFrame()


    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if self._currentSprite is None:
            return
        
    
        
        button = e.button()
        
        if button != Qt.LeftButton and button != Qt.RightButton:
            return
        
        self._updateMouseState(e)
        
        self._currentTool.onMousePress(self, self._spriteMousePosition, e.button())
        
        self._currentTool.setActive(True)
        
        self._animationDisplay._startRefreshing()
        
        self._painter.begin(self._currentDrawingSurface)
        
        ink = self._primaryInk if button == Qt.LeftButton else self._secondaryInk
        
        ink.prepare(self._painter)
        
        self._currentTool.blit(self._painter, ink, True)

        self._painter.end()

        self.update()

    def mouseMoveEvent(self, e):
        
        super().mouseMoveEvent(e)

        if self._currentSprite is None:
            return
        
        self._updateMouseState(e)
        
        viewMousePosition = self.viewMousePos()
        
        self._animationDisplay.panTo(-viewMousePosition.x(), -viewMousePosition.y())
        
        ink = self._primaryInk if e.buttons() & Qt.LeftButton else self._secondaryInk
        
        self._currentTool.onMouseMove(self._spriteMousePosition, self._absoluteMousePosition)
        
        if not self._panning:
        
            if self._currentTool.isActive():
            
                self._painter.begin(self._currentDrawingSurface)
        
                self._currentTool.blit(self._painter, ink)
        
                self._painter.end()
        
        self.update()

    def mouseReleaseEvent(self, e):
        
        
        
        if self._currentSprite is None:
            return
        

        self._animationDisplay._stopRefreshing()

        self._updateMouseState(e)
        
        self._currentTool.setActive(False)
        
        self._currentTool.onMouseRelease(self, self._spriteMousePosition, e.button())
        
        ink = self._primaryInk if e.button() == Qt.LeftButton else self._secondaryInk
        
        ink.finish(self._painter)
        
        self.update()
        
        super().mouseReleaseEvent(e)
    
    def wheelEvent(self, e):
        
        super().wheelEvent(e)
        
    
    def enterEvent(self, e):
        
        if self._currentSprite is None:
            return
        
        self.setCursor(Qt.BlankCursor)
    
    def leaveEvent(self, e):
        
        if self._currentSprite is None:
            return
        
        self.setCursor(Qt.ArrowCursor)
        self._animationDisplay.resetView()
       
        

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
        
    
    
    def _updateMouseState(self, e):

        objectMousePosition = super().objectMousePos()

        objectMousePosition.setX(round(objectMousePosition.x(), 2))
        objectMousePosition.setY(round(objectMousePosition.y(), 2))
        
        self._spriteMousePosition = objectMousePosition
        
        self._absoluteMousePosition.setX(e.pos().x())
        self._absoluteMousePosition.setY(e.pos().y())
        

    def _updateDrawingSurface(self):

        if self._currentSprite is None:
            return

        self._currentDrawingSurface = self._currentSprite.currentAnimation().currentFrame().currentSurface().image()
        self.update()
        
