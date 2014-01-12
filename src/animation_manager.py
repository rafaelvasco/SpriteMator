'''
Created on 30/12/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, QSize, pyqtSignal

from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton, QIcon, QPixmap, QFrame, QPainter

from src.resources_cache import ResourcesCache

from src.sprite import Animation

class AnimationManager(QWidget):
    
    animationSelectedChanged = pyqtSignal(Animation)
    animationListChanged = pyqtSignal()
    
    frameSelectedChanged = pyqtSignal()
    frameListChanged = pyqtSignal()

    def __init__(self):

        super(AnimationManager, self).__init__()
        
        
        self._sprite = None
                
        mainLayout = QHBoxLayout()
        
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
        
        self.setFont(ResourcesCache.get("MedFont"))
        
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
        frameLayout.setContentsMargins(1, 1, 1, 1)
        frameLayout.setMargin(1)
        
        
        self._framesFrame = QWidget()
        self._framesFrame.setStyleSheet("background-color: blue;")
        self._framesFrame.setMinimumSize(70, 70)
        
        copyFrameIcon = QIcon()
        copyFrameIcon.addPixmap(QPixmap(":/icons/ico_copy_frame"))
        
        self._copyFrameButton = QPushButton()
        self._copyFrameButton.setObjectName('copy-frame-button')
        self._copyFrameButton.setIcon(copyFrameIcon)
        self._copyFrameButton.setIconSize(QSize(41,41))
        self._copyFrameButton.setMinimumSize(70,70)
        
        
        self._addFrameButton = QPushButton()
        self._addFrameButton.setIcon(addIcon)
        self._addFrameButton.setIconSize(QSize(6,6))
        self._addFrameButton.setMinimumSize(70, 70)
        
        self._removeFrameButton = QPushButton()
        self._removeFrameButton.setIcon(removeIcon)
        self._removeFrameButton.setIconSize(QSize(6,6))
        self._removeFrameButton.setMinimumSize(70, 70)
        
        #frameLayout.addWidget(self._framesFrame)
        frameLayout.addWidget(self._copyFrameButton)
        frameLayout.addWidget(self._addFrameButton)
        frameLayout.addWidget(self._removeFrameButton)
        
        mainLayout.addLayout(frameLayout)
        
        self.setLayout(mainLayout)
        
        
    def setSprite(self, sprite):
        
        self._sprite = sprite
        
        self._updateFramesFrameSize()
        
        self.refresh()
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
        
        
    
    def clear(self):
        
        self._sprite = None
        
        self._animationCombo.clear()
        
        self.update()
  
    def refresh(self):
        
        if self._sprite is None:
            return
        
        self._animationCombo.clear()
        
        for index, animation in enumerate(self._sprite.animations()):
            
            self._animationCombo.addItem(animation.name(), index)
            
        
        self._animationCombo.setCurrentIndex(self._sprite.currentAnimationIndex())
        
        
        self.update()
  
    def addAnimation(self):
        
        if self._sprite is None:
            return
        
        self._sprite.addAnimation()
  
        self.refresh()
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
  
  
    def setAnimation(self, index):
        
        if self._sprite is None:
            return
        
        self._sprite.setAnimation(index)
        
        self._updateFramesFrameSize()
        
        self.animationSelectedChanged.emit(self._sprite.currentAnimation())
  
    def removeCurrentAnimation(self):
        
        if self._sprite is None:
            return
        
        self._sprite.removeCurrentAnimation()
        
        self.refresh()
    
    
    def addFrame(self):

        if self._sprite is None:
            return
        
        currentAnimation = self._sprite.currentAnimation()

        currentAnimation.addEmptyFrame(currentAnimation.frameWidth(), currentAnimation.frameHeight())
        
        self._updateFramesFrameSize()

    
    def removeFrame(self, index=None):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.removeFrame(index)

        if animation.frameCount() == 0:

            self.addFrame()
            
        self._updateFramesFrameSize()

    def setFrame(self, index):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()
        
        animation.setFrame(index)
    
    
    def goToNextFrame(self):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnLastFrame():
            return

        animation.goToNextFrame()

    def goToPreviousFrame(self):

        if self._sprite is None:
            return
        
        animation = self._sprite.currentAnimation()

        if animation.isOnFirstFrame():
            return

        animation.goToPreviousFrame()
    
    
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
    
    def _updateFramesFrameSize(self):
        
        if self._sprite is None:
            return
        
        
        self._framesFrame.resize(QSize(self._sprite.currentAnimation().frameCount()*70, 70))
        
    
  
        
    
