#--------------------------------------------------
# Name:             Display
# Purpose:
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:
#--------------------------------------------------


from PyQt4.QtCore import QPointF, QPoint, Qt, QSize
from PyQt4.QtGui import QWidget, QPainter, QImage, QPixmap, QMatrix, QColor


import src.utils as utils
from src.input_manager import InputManager

class Display(QWidget):


    def __init__(self):

        QWidget.__init__(self, None)

        self._viewportTransform = QMatrix()
        self._translationTransform = QMatrix()
        self._scaleTransform = QMatrix()
        self._combinedTransform = QMatrix()
        self._invertedCombinedTransform = QMatrix()
        self._backgroundColor = QColor(15,15,15)
        self._fitInView = False
        self._maintainAspectRatio = True
        self._panning = False
        self._zoom = 1.0
        self._globalMousePos = QPointF()
        self._lastPanPoint = QPointF()
        self._currentFocusPoint = QPointF()
        self._keyTranslationVector = QPoint()
        self._currentObjectSize = QSize()

        self._checkerTile = self._generateCheckerboardTile(16, QColor(222,222,222), QColor(253,253,253))

        self.setMouseTracking(True)
        self.resetOrigin()


    def globalMousePos(self):
        return self._globalMousePos

    def objectMousePos(self):
        return self._invertedCombinedTransform.map(self._globalMousePos)


    def isFitInView(self):
        return self._fitInView


    def setFitInView(self, fit):
        if self._fitInView != fit:
            self._fitInView = fit
            self._translationTransform.reset()
            self._scaleTransform.reset()
            self.update()


    def currentObjectSize(self):

        return self._currentObjectSize


    def setObjectSize(self, width, height):

        self._currentObjectSize.setWidth(width)
        self._currentObjectSize.setHeight(height)


    def resetView(self):
        self._fitInView = False
        self._zoom = 1.0
        self.resetOrigin()
        self._translationTransform.reset()
        self._scaleTransform.reset()
        self.update()


    def toggleFitInView(self):

        self.setFitInView(not self._fitInView)


    def resetOrigin(self):
        self._currentFocusPoint.setX(self.rect().center().x())
        self._currentFocusPoint.setY(self.rect().center().y())


    def isMaintainAspectRatio(self):
        return self._maintainAspectRatio


    def setMaintainAspectRatio(self, maintain):
        if self._maintainAspectRatio != maintain:
            self._maintainAspectRatio = maintain
            self.update()


    def zoom(self, factor, origin):

        self._zoom *= factor

        if self._fitInView:

            self._fitInView = False
            self.update()

        if self._zoom < 1.0:
            self._zoom = 1.0
            return

        if self._zoom > 30.0:
            self._zoom = 30.0
            return

        x,y = origin.x(), origin.y()

        scaleTransform = QMatrix()

        scaleTransform.translate(x, y)
        scaleTransform.scale(factor, factor)


        scaleTransform.translate(-x, -y)

        self._scaleTransform = utils.multiplyMatrix(self._scaleTransform, scaleTransform)

        self.update()


    def zoomTo(self, targetZoom):

        self.resetView()

        self._zoom = targetZoom

        if self._zoom < 0.0:
            self._zoom = 0.0


        ox, oy = self._currentFocusPoint.x(), self._currentFocusPoint.y()

        self._scaleTransform.translate(ox, oy)
        self._scaleTransform.scale(self._zoom, self._zoom)
        self._scaleTransform.translate(-ox, -oy)

        self.update()


    def pan(self, dx, dy):

        if self._fitInView:

            self._fitInView = False

        self._translationTransform.translate(dx, dy)
        self.update()


    # def resizeEvent(self, e):

        # self.update()



    def onDrawObject(self, event):
        pass


    def paintEvent(self, event):

        painter = QPainter()

        painter.begin(self)

        painter.fillRect(self.rect(), self._backgroundColor)

        if not self._currentObjectSize.isValid():
            return


        viewWidth = self.width()
        viewHeight = self.height()


        objectWidth = self._currentObjectSize.width()
        objectHeight = self._currentObjectSize.height()

        self._viewportTransform.reset()

        if not self._fitInView:

            centerTranslateX = round(viewWidth / 2 - objectWidth / 2)
            centerTranslateY = round(viewHeight / 2 - objectHeight / 2)

            self._viewportTransform.translate(centerTranslateX, centerTranslateY)
        else:
            finalScaleX = viewWidth / objectWidth
            finalScaleY = viewHeight / objectHeight

            if self._maintainAspectRatio:

                finalScale = (min(finalScaleX, finalScaleY))

                if finalScaleX > finalScaleY:
                    centerTranslateX = round(viewWidth / 2 - (objectWidth*finalScale) / 2)
                    self._viewportTransform.translate(centerTranslateX, 0)

                elif finalScaleX < finalScaleY:
                    centerTranslateY = round(viewHeight / 2 - (objectHeight*finalScale) / 2)
                    self._viewportTransform.translate(0, centerTranslateY)

                finalScaleX = finalScaleY = finalScale

            self._viewportTransform.scale(finalScaleX, finalScaleY)


        self._combinedTransform = self._viewportTransform * self._translationTransform * self._scaleTransform
        self._invertedCombinedTransform = self._combinedTransform.inverted()[0]

        painter.setMatrix(self._combinedTransform)

        painter.drawTiledPixmap(0, 0, objectWidth, objectHeight, self._checkerTile)
        
        self.onDrawObject(event)

    def mousePressEvent(self, e):

        if e.button() == Qt.MiddleButton:

            self._panning = True
            self._lastPanPoint = e.pos()
            self.setCursor(Qt.ClosedHandCursor)


    def mouseMoveEvent(self, e):

        self._globalMousePos.setX(e.pos().x())
        self._globalMousePos.setY(e.pos().y())

        if not self._panning:
            return

        delta = e.pos() - self._lastPanPoint

        if self._zoom != 1.0:
            self.pan((delta.x()), (delta.y()))
        else:
            self.pan(delta.x(), delta.y())

        self._lastPanPoint = e.pos()


    def wheelEvent(self, e):
        
        if (InputManager.instance().isKeyPressed(Qt.Key_Control) or 
            InputManager.instance().isKeyPressed(Qt.Key_Alt)):
            return
        
        scaleFactor = 2.0

        if e.delta() > 0:
            self.zoom(scaleFactor, self._globalMousePos)
        else:
            self.zoom(1.0 / scaleFactor, self._globalMousePos)
            
        



    def mouseReleaseEvent(self, e):

        if self._panning and e.button() == Qt.MiddleButton:

            self._panning = False
            self.setCursor(Qt.ArrowCursor)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Left:

            self.pan(round(-1), 0)

        elif e.key() == Qt.Key_Right:

            self.pan(round(1), 0)

        elif e.key() == Qt.Key_Up:

            self.pan(0, round(-1))

        elif e.key() == Qt.Key_Down:

            self.pan(0, round(1))

        elif e.key() == Qt.Key_F:

            self.toggleFitInView()

        elif e.key() == Qt.Key_A:

            self.setMaintainAspectRatio(not self._maintainAspectRatio)

        elif e.key() == Qt.Key_R:

            self.resetView()

        elif e.key() == Qt.Key_1:

            self.zoomTo(1.0)

        elif e.key() == Qt.Key_2:

            self.zoomTo(2.0)

        elif e.key() == Qt.Key_3:

            self.zoomTo(3.0)

        elif e.key() == Qt.Key_4:

            self.zoomTo(4.0)

        elif e.key() == Qt.Key_5:

            self.zoomTo(5.0)


    def _generateCheckerboardTile(self, size, color1, color2):

        tileSize = size * 2

        tile = QImage(tileSize, tileSize, QImage.Format_ARGB32_Premultiplied)

        painter = QPainter()

        painter.begin(tile)

        painter.fillRect(0, 0, tileSize, tileSize, color1)
        painter.fillRect(0, 0, size, size, color2)
        painter.fillRect(size,size,size,size, color2)

        painter.end()

        tilePixmap = QPixmap.fromImage(tile)

        return tilePixmap








