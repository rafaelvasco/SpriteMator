'''
Created on 30/12/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt, QSize, pyqtSignal

from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton, QIcon, QPixmap

from src.resources_cache import ResourcesCache


class AnimationManager(QWidget):

    addClicked = pyqtSignal()
    removeClicked = pyqtSignal(int)
    animationIndexChanged = pyqtSignal(int)

    def __init__(self):

        super(AnimationManager, self).__init__()
        
        mainLayout = QVBoxLayout()
        
        self.setFont(ResourcesCache.get("MedFont"))
        
        label = QLabel('Animation')
        label.setAlignment(Qt.AlignCenter)
        
        mainLayout.addWidget(label)
        
        
        controlsLayout = QHBoxLayout()
        
        self._animationCombo = QComboBox()
        self._animationCombo.currentIndexChanged.connect(self._onAnimationIndexChanged)
        
        self._addButton = QPushButton()
        self._addButton.clicked.connect(self._onAddClicked)
        
        addButtonIcon = QIcon()
        addButtonIcon.addPixmap(QPixmap(":/icons/ico_small_plus"))
        self._addButton.setIcon(addButtonIcon)
        self._addButton.setIconSize(QSize(6,6))
        
        self._removeButton = QPushButton()
        self._removeButton.clicked.connect(self._onRemoveClicked)
        
        removeButtonIcon = QIcon()
        removeButtonIcon.addPixmap(QPixmap(":/icons/ico_small_minus"))
        self._removeButton.setIcon(removeButtonIcon)
        self._removeButton.setIconSize(QSize(6,6))
        
        controlsLayout.addWidget(self._animationCombo)
        controlsLayout.addWidget(self._addButton)
        controlsLayout.addWidget(self._removeButton)
        
        mainLayout.addLayout(controlsLayout)
        
        self.setLayout(mainLayout)
        
    
    def addItem(self, animationName, animationIndex):
        
        self._animationCombo.addItem(animationName, animationIndex)
        self._animationCombo.setCurrentIndex(self._animationCombo.count() - 1)
        
    def _onAddClicked(self):
        
        self.addClicked.emit()
        
    def _onRemoveClicked(self):
        
        self.removeClicked.emit(self._animationCombo.itemData(self._animationCombo.currentIndex()))
        
    def _onAnimationIndexChanged(self, index):
        
        self.animationIndexChanged.emit(index)