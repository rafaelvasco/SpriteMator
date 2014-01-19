'''
Created on 30/12/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, QSize, pyqtSignal, QTimer, QRect

from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton, QIcon, QPixmap, QPen, QPainter, QColor

import math

from src.sprite import Animation

from src.resources_cache import ResourcesCache


class FrameStrip(QWidget):
    
    frameSelectedChanged = pyqtSignal(int)
    
    def __init__(self):
        
        super(FrameStrip, self).__init__()
        
        self._sprite = None
        
        self._frameList = None
        
        self._frameSize = 70
        
        self._framePadding = 4
        
        self._pen = QPen(QColor(0, 179, 255))
        self._pen.setCapStyle(Qt.SquareCap)
        self._pen.setJoinStyle(Qt.MiterJoin)
        self._pen.setWidth(4.0)
        
        self.setContentsMargins(0, 0, 0, 0)
        
        self.setMinimumSize(self._frameSize + self._framePadding*2, self._frameSize + self._framePadding*2)
        self.setMaximumHeight(self._frameSize + self._framePadding*2)
        
        self._checkerTile = ResourcesCache.get("CheckerTileLight")
        
    def setSprite(self, sprite):
        
        self._sprite = sprite
        
        self.updateSize()
        
        self.update()
    
    def updateSize(self):
        
        if self._sprite is None:
            self.setMinimumSize(self._frameSize + self._framePadding * 2, self._frameSize + self._framePadding * 2)
            return
        
        count = self._sprite.currentAnimation().frameCount()
        
        self.setMinimumSize(self._frameSize * count + self._framePadding * count * 2 , self._frameSize + self._framePadding * 2)
    
    
    def mousePressEvent(self, e):
        
        pos = e.pos()
        
        clickedIndex = int(math.floor(pos.x() / (self._frameSize + self._framePadding)))
        
        currentIndex = self._sprite.currentAnimation().currentFrameIndex()
        
        if clickedIndex != currentIndex:
        
            self.frameSelectedChanged.emit(clickedIndex)
        
        
    def paintEvent(self, e):
        
        p = QPainter(self)
        
        frameIndex = 0
        
        currentFrameIndex = self._sprite.currentAnimation().currentFrameIndex()
        
        frameList = self._sprite.currentAnimation().frames()
        
        frameSize = self._frameSize
        framePadding = self._framePadding
        halfPadding = framePadding // 2
        twoPadding = framePadding * 2
        
        for frame in frameList:
            
            for surface in frame.surfaces():
                
                frameRect = QRect(
                                  framePadding + frameIndex * frameSize + twoPadding * frameIndex , 
                                  framePadding, 
                                  frameSize, 
                                  frameSize)
                
                if currentFrameIndex == frameIndex:
                    
                    p.setPen(self._pen)
                    
                    p.drawRect(frameRect.adjusted(-halfPadding, -halfPadding, halfPadding, halfPadding))
                    
                    p.setPen(Qt.black)
                    
                    p.drawRect(frameRect.adjusted(-1,-1,0,0))
                
                p.drawTiledPixmap(frameRect, self._checkerTile)
                
                p.drawImage(frameRect, surface.image(), surface.image().rect())
                
                
                
                
            frameIndex += 1
    
    def sizeHint(self):
        
        return QSize(self._frameSize,self._frameSize)

class AnimationManager(QWidget):
    
    animationSelectedChanged = pyqtSignal(Animation)
    frameSelectedChanged = pyqtSignal(int)

    def __init__(self):

        super(AnimationManager, self).__init__()
        
        self._sprite = None
        
        self._frameStrip = FrameStrip()    
        self._frameStrip.frameSelectedChanged.connect(self._onFrameStripFrameSelectedChanged)
        
        mainLayout = QHBoxLayout()
        
        self._refreshSpeed = 16
        
        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refreshEvent)
        self._refreshTimer.stop()
        
        self.setStyleSheet("""
                    
                    QPushButton
                    {
                        background-color: #2F4A60;
                        border: 1px solid #65ACE3;
                    }
                    
                    QPushButton:hover
                    {
                        background-color: #487193;
                        border: 1px solid #A5CEEE;
                    }
                    
                    QPushButton:pressed
                    {
                        background-color: #273D4F;
                        border: 1px solid #0B273C;
                    }
                        
        """);
        
        
        label = QLabel('Animation')
        label.setAlignment(Qt.AlignCenter)
        
        animationLayout = QVBoxLayout()
        
        animationLayout.addWidget(label)
        
        controlsLayout = QHBoxLayout()
        
        self._animationCombo = QComboBox()
        #self._animationCombo.setEditable(True)
        #self._animationCombo.setDuplicatesEnabled(False)
        #self._animationCombo.setInsertPolicy(QComboBox.InsertAtCurrent)
        #self._animationCombo.editTextChanged.connect(self._onAnimationComboEdited)
        self._animationCombo.activated.connect(self._onAnimationIndexChanged)
        
        
        addIcon = QIcon()
        addIcon.addPixmap(QPixmap(":/icons/ico_small_plus"))
        removeIcon = QIcon()
        removeIcon.addPixmap(QPixmap(":/icons/ico_small_minus"))
        
        
        self._addAnimationButton = QPushButton()
        self._addAnimationButton.clicked.connect(self._onAddAnimationClicked)
        
        
        self._addAnimationButton.setIcon(addIcon)
        self._addAnimationButton.setIconSize(QSize(6,6))
        
        self._removeAnimationButton = QPushButton()
        self._removeAnimationButton.clicked.connect(self._onRemoveAnimationClicked)
        
        
        self._removeAnimationButton.setIcon(removeIcon)
        self._removeAnimationButton.setIconSize(QSize(6,6))
        
        controlsLayout.addWidget(self._animationCombo)
        controlsLayout.addWidget(self._addAnimationButton)
        controlsLayout.addWidget(self._removeAnimationButton)
        
        animationLayout.addLayout(controlsLayout)
        
        mainLayout.addLayout(animationLayout)
        
        frameLayout = QHBoxLayout()
        frameLayout.setContentsMargins(0, 0, 0, 0)
        frameLayout.setMargin(0)
        
        copyFrameIcon = QIcon()
        copyFrameIcon.addPixmap(QPixmap(":/icons/ico_copy_frame"))
        
        self._copyFrameButton = QPushButton()
        self._copyFrameButton.clicked.connect(self._onCopyFrameClicked)
        self._copyFrameButton.setObjectName('copy-frame-button')
        self._copyFrameButton.setIcon(copyFrameIcon)
        self._copyFrameButton.setIconSize(QSize(41,41))
        self._copyFrameButton.setMinimumSize(70,70)
        
        
        self._addFrameButton = QPushButton()
        self._addFrameButton.clicked.connect(self._onAddFrameClicked)
        self._addFrameButton.setIcon(addIcon)
        self._addFrameButton.setIconSize(QSize(6,6))
        self._addFrameButton.setMinimumSize(70, 70)
        
        self._removeFrameButton = QPushButton()
        self._removeFrameButton.clicked.connect(self._onRemoveFrameClicked)
        self._removeFrameButton.setIcon(removeIcon)
        self._removeFrameButton.setIconSize(QSize(6,6))
        self._removeFrameButton.setMinimumSize(70, 70)
        
        frameLayout.addWidget(self._frameStrip)
        frameLayout.addWidget(self._copyFrameButton)
        frameLayout.addWidget(self._addFrameButton)
        frameLayout.addWidget(self._removeFrameButton)
        
        mainLayout.addLayout(frameLayout)
        
        self.setLayout(mainLayout)
        
        
    def setSprite(self, sprite):
        
        self._sprite = sprite
        
        self._updateAnimationCombo()
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
        
        self._frameStrip.setSprite(sprite)
        
    
    def clear(self):
        
        self._sprite = None
        
        self._animationCombo.clear()
        
        self._frameStrip.setSprite(None)
        
        self._frameStrip.updateSize()
        
        self.update()
  
   
  
    def addAnimation(self):
        
        if self._sprite is None:
            return
        
        self._sprite.addAnimation()
  
        self._updateAnimationCombo()
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
  
  
    def setAnimation(self, index):
        
        if self._sprite is None:
            return
        
        self._sprite.setAnimation(index)
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
  
    def removeCurrentAnimation(self):
        
        if self._sprite is None:
            return
        
        self._sprite.removeCurrentAnimation()
        
        self._updateAnimationCombo()
    
    
    def addFrame(self):
        print('Add Frame')
        if self._sprite is None:
            return
        
        currentAnimation = self._sprite.currentAnimation()

        currentAnimation.addEmptyFrame(currentAnimation.frameWidth(), currentAnimation.frameHeight())
        
        self._frameStrip.updateSize()
        
        self.update()
        
        self.frameSelectedChanged.emit(currentAnimation.currentFrame())
    
    def removeFrame(self, index=None):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.removeFrame(index)

        if animation.frameCount() == 0:

            self.addFrame()
        
        self._frameStrip.updateSize()
        
        self.update()
        
        self.frameSelectedChanged.emit(self._sprite.currentAnimation().currentFrame())
        
        
    def setFrame(self, index):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.setFrame(index)
        
        self.update()
        
        self.frameSelectedChanged.emit(index)
    
    def goToNextFrame(self):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnLastFrame():
            return

        animation.goToNextFrame()
        
        self.update()
        
        self.frameSelectedChanged.emit(animation.currentFrame())
        

    def goToPreviousFrame(self):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnFirstFrame():
            return

        animation.goToPreviousFrame()
    
        self.update()
        
        self.frameSelectedChanged.emit(animation.currentFrame())
    
    def _startRefreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def _stopRefreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False
    
    
    def _onAddAnimationClicked(self):
        
        self.addAnimation()
        
    def _onRemoveAnimationClicked(self):
        
        self.removeCurrentAnimation()
        
        
    def _onAnimationIndexChanged(self, index):
        
        if self._sprite is None:
            return
        
        if self._sprite.currentAnimationIndex() != index:
            
            self.setAnimation(index)
      
    
    def _onAnimationComboEdited(self, newText):
        
        if self._sprite is None:
            return
        
        print('Edited to: ', newText)
        self._sprite.currentAnimation().setName(newText)
    
    def _onAddFrameClicked(self):
        
        self.addFrame()
    
    def _onRemoveFrameClicked(self):
        
        self.removeFrame()
    
    def _onCopyFrameClicked(self):
        
        pass
    
    def _onFrameStripFrameSelectedChanged(self, index):
        
        self.setFrame(index)
    
    def _refreshEvent(self):
        
        self.update()
        
    def _updateAnimationCombo(self):
        
        if self._sprite is None:
            return
        
        self._animationCombo.clear()
        
        for index, animation in enumerate(self._sprite.animations()):
            
            self._animationCombo.addItem(animation.name(), index)
            
        
        self._animationCombo.setCurrentIndex(self._sprite.currentAnimationIndex())
        
        self.update()