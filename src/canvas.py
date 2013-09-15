#--------------------------------------------------
# Name:             Canvas
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             30/03/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import Qt, pyqtSignal, QPoint
from PyQt4.QtGui import QPainter, QPushButton, QVBoxLayout, QSizePolicy, QHBoxLayout, QColor

from src.display import  Display
from src.sprite import Frame
import src.tools as Tools
import src.inks as Inks
import src.utils as Utils

class Canvas(Display):

    frameChanged = pyqtSignal(Frame)

    def __init__(self, animationDisplay):

        Display.__init__(self)

        self._currentSprite = None
        self._animationDisplay = animationDisplay
        self._currentDrawingSurface = None
        self._currentCompositionMode = QPainter.CompositionMode_SourceOver
        self._painter = QPainter()
        self._currentTool = Tools.Pen
        self._primaryInk = Inks.Solid()
        self._secondaryInk = Inks.Solid()
        self._active = False
        self._mousePosition = QPoint()
        
        
        
        self._mainLayout = QVBoxLayout(self)
        self._mainLayout.setAlignment(Qt.AlignBottom)
        self._controlsLayout = QHBoxLayout()

        self._addFrameBtn = QPushButton('Add Frame')
        self._addFrameBtn.clicked.connect(self.addFrame)

        self._delFrameBtn = QPushButton('Remove Frame')
        self._delFrameBtn.clicked.connect(self.onDelFrameButtonClicked)


        self._goToNextFrameBtn = QPushButton('>')
        self._goToNextFrameBtn.clicked.connect(self.goToNextFrame)

        self._goToPrevFrameBtn = QPushButton('<')
        self._goToPrevFrameBtn.clicked.connect(self.goToPreviousFrame)

        self._controlsLayout.addWidget(self._addFrameBtn)
        self._controlsLayout.addWidget(self._delFrameBtn)
        self._controlsLayout.addWidget(self._goToPrevFrameBtn)
        self._controlsLayout.addWidget(self._goToNextFrameBtn)


        self._mainLayout.addLayout(self._controlsLayout)


        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(320)
        self.setMinimumHeight(240)




    # TODO: Do get sets of Tools and Inks


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





    def unloadSprite(self):

        self.resetView()
        self.setObjectSize(0, 0)
        self._currentDrawingSurface = None
        self._currentSprite = None
        self.update()


    def addAnimation(self):

        if self._currentSprite is None:
            return

        self._currentSprite.addAnimation()

        self._updateDrawingSurface()

        self._animationDisplay.setAnimation(self._currentSprite.currentAnimation())

        self.frameChanged.emit(self._currentSprite.currentAnimation().currentFrame())


    def setAnimation(self, index):

        if self._currentSprite is None:
            return

        self._currentSprite.setAnimation(index)

        self._updateDrawingSurface()

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

        painter = QPainter()

        painter.begin(self._currentDrawingSurface)

        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.fillRect(0, 0, self._currentDrawingSurface.width(), self._currentDrawingSurface.height(), Qt.white)

        painter.end()


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

        painter.setPen(QColor(255,0,0))

        painter.resetMatrix()

        painter.drawText(10,50, "Current Animation: {0}, Current Frame: {1}, Current Surface: {2}"
                .format(self._currentSprite.currentAnimation().name(),
                        self._currentSprite.currentAnimation().currentFrameIndex(),
                        self._currentSprite.currentAnimation().currentFrame().currentSurfaceIndex()))

        painter.drawText(10, 70, "Current Layer Stack: ")

        layers = self.currentFrame().surfaces()
        index = 0
        for layer in layers:

            painter.drawText( 10, 20 * (index) + 100, "Index: " + str(index) + ", Name: " + layer.name())
            index += 1

    def onDelFrameButtonClicked(self):

        self.removeFrame()


    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if self._currentSprite is None:
            return

        button = e.button()

        if button != Qt.LeftButton and button != Qt.RightButton:
            return

        self._animationDisplay._startRefreshing()

        self._active = True

        self._processMouseEvent(e)

        self._painter.begin(self._currentDrawingSurface)

        self._currentTool.onMousePress(self, self._mousePosition, e.button())

        self._painter.end()

        self.update()

    def mouseMoveEvent(self, e):

        super().mouseMoveEvent(e)

        if self._currentSprite is None:
            return

        if not self._active:
            return

        self._processMouseEvent(e)

        self._painter.begin(self._currentDrawingSurface)

        if self._currentTool.isActive():
            self._currentTool.onMouseMove(self, self._mousePosition, e.buttons())

        self._painter.end()

        self.update()

    def mouseReleaseEvent(self, e):

        super().mouseReleaseEvent(e)

        if self._currentSprite is None:
            return

        self._animationDisplay._stopRefreshing()

        self._processMouseEvent(e)

        self._painter.begin(self._currentDrawingSurface)

        self._currentTool.onMouseRelease(self, self._mousePosition, e.button())

        self._painter.end()

        self.update()

        self._active = False


    # ---- PRIVATE METHODS ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def _processMouseEvent(self, e):

        spriteLocalMouse = super().objectMousePos()

        spriteLocalMouse.setX(round(spriteLocalMouse.x(), 2))
        spriteLocalMouse.setY(round(spriteLocalMouse.y(), 2))
        
        self._mousePosition = spriteLocalMouse

    def _updateDrawingSurface(self):

        if self._currentSprite is None:
            return

        self._currentDrawingSurface = self._currentSprite.currentAnimation().currentFrame().currentSurface().image()
        self.update()