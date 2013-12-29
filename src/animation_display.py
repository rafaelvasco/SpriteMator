#--------------------------------------------------
# Name:             AnimationDisplay
# Purpose:          Display and animate a selected Animation from current Sprite
#
# Author:           Rafael Vasco
# Date:             07/07/13
# License:          
#--------------------------------------------------
from PyQt4.QtCore import QTimer, Qt, QSize
from PyQt4.QtGui import QColor, QPen, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QPainter, QIcon, QPixmap

from src.display import Display


class AnimationDisplay(Display):

    def __init__(self, parent=None):

        super(AnimationDisplay, self).__init__(parent)
        self._animation = None
        self._playing = False
        self._refreshing = False
        self._refreshSpeed = 16
        self._animationSpeed = 500
        self._loopEnabled = True
        self._pen = QPen()
        self._pen.setColor(QColor(10,10,10))
        self._pen.setWidth(2)
        self._pen.setJoinStyle(Qt.MiterJoin)
        self._currentFrame = 0

        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refreshEvent)
        self._refreshTimer.stop()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        self._animationTimer = QTimer()
        self._animationTimer.timeout.connect(self._animateEvent)
        self._animationTimer.stop()

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)


        self._controlsLayout = QHBoxLayout()

        self._goNextFrameBtn = QPushButton()
        self._goNextFrameBtn.clicked.connect(self.goToNextFrame)
        
        goNextFrameicon = QIcon()
        goNextFrameicon.addPixmap(QPixmap(":/icons/ico_next"))
        
        self._goNextFrameBtn.setIcon(goNextFrameicon)
        self._goNextFrameBtn.setIconSize(QSize(14,14))


        self._goPrevFrameBtn = QPushButton()
        self._goPrevFrameBtn.clicked.connect(self.goToPreviousFrame)
        
        
        goPrevFrameicon = QIcon()
        goPrevFrameicon.addPixmap(QPixmap(":/icons/ico_prev"))
        
        self._goPrevFrameBtn.setIcon(goPrevFrameicon)
        self._goPrevFrameBtn.setIconSize(QSize(14,14))
        

        self._playPauseBtn = QPushButton()
        self._playPauseBtn.clicked.connect(self.togglePlay)
        
        playFrameicon = QIcon()
        playFrameicon.addPixmap(QPixmap(":/icons/ico_play"))
        
        self._playPauseBtn.setIcon(playFrameicon)
        self._playPauseBtn.setIconSize(QSize(14,14))

        self._controlsLayout.addWidget(self._playPauseBtn)
        self._controlsLayout.addWidget(self._goPrevFrameBtn)
        self._controlsLayout.addWidget(self._goNextFrameBtn)

        self._layout.addLayout(self._controlsLayout)


    def isPlaying(self):
        return self._playing

    def isLooping(self):

        return self._loopEnabled if self._animation is not None else False



    def setLooping(self, value):

        if self._animation is None:
            return

        self._loopEnabled = value

    def animationSpeed(self):
        return self._animationSpeed

    def setAnimationSpeed(self, value):
        self._animationSpeed = value

    def _startRefreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def _stopRefreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False

    def _startAnimating(self):
        self._animationTimer.start(self._animationSpeed)
        self._playing = True

    def _stopAnimating(self):
        self._animationTimer.stop()
        self._playing = False



    def _refreshEvent(self):

        self.update()

    def _animateEvent(self):

        if self._animation is not None and self._playing:
            self._animate()



    def _animate(self):

        if self._animation is None:
            return

        self._currentFrame += 1
        frameCount = self._animation.frameCount()

        if self._currentFrame > frameCount - 1:

            if self._loopEnabled:
                self._currentFrame = 0
            else:
                self._currentFrame = frameCount - 1
                self.pause()

        self.update()

    def onDrawObject(self, event, painter):
        
        if self._animation is not None:

            layers = self._animation.frameAt(self._currentFrame).surfaces()

            for layer in layers:
                painter.drawImage(0, 0, layer.image())


    def setAnimation(self, animation):

        if self._animation is not None:
            self.unloadAnimation()

        self._animation = animation

        self.setObjectSize(self._animation.frameWidth(), self._animation.frameHeight())

        self._currentFrame = 0

        self.update()

    def unloadAnimation(self):


        self._animation = None

        self.setObjectSize(0, 0)

        self._playing = False
        self._refreshing = False
        self._refreshTimer.stop()
        self._animationTimer.stop()

        self.update()

    def togglePlay(self):

        if self._animation is None:
            return

        if not self._playing:
            self.play()
            self._playPauseBtn.setText('||')
        else:
            self.pause()
            self._playPauseBtn.setText('>')

    def play(self):

        if self._animation is None:
            return

        self._startAnimating()

        self.update()

    def pause(self):

        if self._animation is None:
            return

        self._stopAnimating()

        self.update()

    def goToFrame(self, index):

        if self._animation is None:
            return

        self._currentFrame = index

        self.update()

    def goToNextFrame(self):

        if self._animation is None:
            return

        frameCount = self._animation.frameCount()

        self._currentFrame += 1

        if self._currentFrame > frameCount - 1:
            self._currentFrame = frameCount - 1

        self.update()

    def goToPreviousFrame(self):

        if self._animation is None:
            return

        self._currentFrame -= 1

        if self._currentFrame < 0:
            self._currentFrame = 0

        self.update()


