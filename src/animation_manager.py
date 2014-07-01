#-----------------------------------------------------------------------------------------------------------------------
# Name:        AnimationManager
# Purpose:     Manages and displays current Sprite's animations;
#
# Author:      Rafael Vasco
#
# Created:     30/12/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

import math

from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QRect
from PyQt5.QtGui import QIcon, QPixmap, QPen, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton

import src.utils as utils
from src.sprite import Animation
from src.resources_cache import ResourcesCache


#-----------------------------------------------------------------------------------------------------------------------


class FrameStrip(QWidget):
    frameSelectedChanged = pyqtSignal(int)

    def __init__(self):

        super(FrameStrip, self).__init__()

        self._sprite = None

        self._frameList = None

        self._frameSize = 70

        self._max_frames_on_view = 6

        self._framePadding = 4

        self._horizontal_shift = 0

        self._pen = QPen(QColor(0, 179, 255))
        self._pen.setCapStyle(Qt.SquareCap)
        self._pen.setJoinStyle(Qt.MiterJoin)
        self._pen.setWidth(4.0)

        self.setContentsMargins(0, 0, 0, 0)



        self.setMinimumSize(self._frameSize + self._framePadding * 2, self._frameSize + self._framePadding * 2)
        self.setMaximumHeight(self._frameSize + self._framePadding * 2)

        self._checkerTile = ResourcesCache.get("CheckerTileLight")

    def set_sprite(self, sprite):

        self._sprite = sprite

        self.update_strip_layout()

    def frame_size(self):

        return self._frameSize

    def total_frame_size(self):

        return self._frameSize + self._framePadding*2

    def set_max_frames_on_view(self, v):

        self._horizontal_shift = 0
        self._max_frames_on_view = v
        self.update_strip_layout()

    def update_strip_layout(self):

        if self._sprite is None:
            self.setMinimumSize(self._frameSize + self._framePadding * 2, self._frameSize + self._framePadding * 2)
            return


        self.setMinimumSize((self._frameSize + self._framePadding * 2) * self._max_frames_on_view, self._frameSize + self._framePadding * 2)

        count = self._sprite.current_animation().frame_count()


        new_width = self._frameSize * count + self._framePadding * count * 2

        if count <= self._max_frames_on_view:
            if self._horizontal_shift != 0:
                self._horizontal_shift = 0

            self.setMinimumSize(new_width, self._frameSize + self._framePadding * 2)

        else:

            current_frame_index = self._sprite.current_animation().current_frame_index()

            if (current_frame_index + 1) > self._max_frames_on_view:
                self._horizontal_shift = ((current_frame_index+1) - self._max_frames_on_view) * (self._frameSize + 2 * self._framePadding)
            else:
                self._horizontal_shift = 0

        self.update()

    def mousePressEvent(self, e):

        pos = e.pos()

        clicked_index = int(math.floor((pos.x()+self._horizontal_shift) / (self._frameSize + self._framePadding*2)))
        current_index = self._sprite.current_animation().current_frame_index()

        if clicked_index != current_index:
            self.frameSelectedChanged.emit(clicked_index)

    def wheelEvent(self, e):

        delta = e.angleDelta().y()

        excedent_frames =  self._sprite.current_animation().frame_count() - self._max_frames_on_view

        if excedent_frames < 0:
            excedent_frames = 0

        total_frame_size = self._frameSize + 2 * self._framePadding

        if delta > 0:

            self._horizontal_shift += total_frame_size

            if self._horizontal_shift > excedent_frames * total_frame_size:
                self._horizontal_shift = excedent_frames * total_frame_size

            self.update()


        elif delta < 0:

            self._horizontal_shift -= self._frameSize + 2 * self._framePadding

            if self._horizontal_shift < -excedent_frames * total_frame_size + excedent_frames * total_frame_size:
                self._horizontal_shift = -excedent_frames * total_frame_size + excedent_frames * total_frame_size

            self.update()

    def paintEvent(self, e):

        p = QPainter(self)

        current_frame_index = self._sprite.current_animation().current_frame_index()

        frame_list = self._sprite.current_animation().frames()

        frame_size = self._frameSize
        frame_padding = self._framePadding
        half_padding = frame_padding // 2
        two_padding = frame_padding * 2

        if self._horizontal_shift != 0:

            p.translate(-self._horizontal_shift, 0)

        for frameIndex, frame in enumerate(frame_list):

            surfaces = frame.surfaces()

            frame_rect = QRect(
                frame_padding + frameIndex * frame_size + two_padding * frameIndex,
                frame_padding,
                frame_size,
                frame_size)



            if current_frame_index == frameIndex:
                p.setPen(self._pen)

                p.drawRect(frame_rect.adjusted(-half_padding, -half_padding, half_padding, half_padding))

                p.setPen(Qt.black)

                p.drawRect(frame_rect.adjusted(-1, -1, 0, 0))

            p.drawTiledPixmap(frame_rect, self._checkerTile)

            for surface in surfaces:
                p.drawImage(frame_rect, surface.image(), surface.image().rect())

            p.setPen(Qt.black)
            p.drawText(frame_rect.left() + two_padding, frame_rect.top() + two_padding*2, str(frameIndex+1))


    def sizeHint(self):

        return QSize(self._frameSize, self._frameSize)


class AnimationManager(QWidget):
    animationSelectedChanged = pyqtSignal(Animation)
    frameSelectedChanged = pyqtSignal(int)

    def __init__(self):

        super(AnimationManager, self).__init__()

        self.setAcceptDrops(True)

        self._sprite = None

        self._frameStrip = FrameStrip()
        self._frameStrip.frameSelectedChanged.connect(self._on_framestrip_frame_selected_changed)

        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignLeft)

        self._refreshSpeed = 16

        self._refreshing = False

        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refresh_event)
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
                        
        """)

        label = QLabel('Animation')
        label.setAlignment(Qt.AlignCenter)

        animation_layout = QVBoxLayout()

        animation_layout.addWidget(label)

        controls_layout = QHBoxLayout()

        self._animationCombo = QComboBox()
        #self._animationCombo.setEditable(True)
        #self._animationCombo.setDuplicatesEnabled(False)
        #self._animationCombo.setInsertPolicy(QComboBox.InsertAtCurrent)
        #self._animationCombo.editTextChanged.connect(self._onAnimationComboEdited)
        self._animationCombo.activated.connect(self._on_animation_index_changed)

        icon_add = QIcon()
        icon_add.addPixmap(QPixmap(":/icons/ico_small_plus"))
        icon_remove = QIcon()
        icon_remove.addPixmap(QPixmap(":/icons/ico_small_minus"))

        self._addAnimationButton = QPushButton()
        self._addAnimationButton.clicked.connect(self._on_add_animation_clicked)

        self._addAnimationButton.setIcon(icon_add)
        self._addAnimationButton.setIconSize(QSize(6, 6))

        self._removeAnimationButton = QPushButton()
        self._removeAnimationButton.clicked.connect(self._on_remove_animation_clicked)

        self._removeAnimationButton.setIcon(icon_remove)
        self._removeAnimationButton.setIconSize(QSize(6, 6))

        controls_layout.addWidget(self._animationCombo)
        controls_layout.addWidget(self._addAnimationButton)
        controls_layout.addWidget(self._removeAnimationButton)

        animation_layout.addLayout(controls_layout)

        main_layout.addLayout(animation_layout)

        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)

        icon_copy_frame = QIcon()
        icon_copy_frame.addPixmap(QPixmap(":/icons/ico_copy_frame"))

        strip_frame_size = self._frameStrip.frame_size()

        self._copyFrameButton = QPushButton()
        self._copyFrameButton.clicked.connect(self._on_copy_frame_clicked)
        self._copyFrameButton.setObjectName('copy-frame-button')
        self._copyFrameButton.setIcon(icon_copy_frame)
        self._copyFrameButton.setIconSize(QSize(41, 41))
        self._copyFrameButton.setMinimumSize(strip_frame_size, strip_frame_size)

        self._addFrameButton = QPushButton()
        self._addFrameButton.clicked.connect(self._on_add_frame_clicked)
        self._addFrameButton.setIcon(icon_add)
        self._addFrameButton.setIconSize(QSize(6, 6))
        self._addFrameButton.setMinimumSize(strip_frame_size, strip_frame_size)

        self._removeFrameButton = QPushButton()
        self._removeFrameButton.clicked.connect(self._on_remove_frame_clicked)
        self._removeFrameButton.setIcon(icon_remove)
        self._removeFrameButton.setIconSize(QSize(6, 6))
        self._removeFrameButton.setMinimumSize(strip_frame_size, strip_frame_size)

        frame_layout.addWidget(self._frameStrip)
        frame_layout.addWidget(self._copyFrameButton)
        frame_layout.addWidget(self._addFrameButton)
        frame_layout.addWidget(self._removeFrameButton)

        main_layout.addLayout(frame_layout)

        self.setLayout(main_layout)

    def set_sprite(self, sprite):

        self._sprite = sprite

        self._update_animation_combo()

        self.animationSelectedChanged.emit(self._sprite.current_animation())

        self._frameStrip.set_sprite(sprite)

    def clear(self):

        self._sprite = None

        self._animationCombo.clear()

        self._frameStrip.set_sprite(None)

    def add_animation(self):

        if self._sprite is None:
            return

        self._sprite.add_animation()

        self._update_animation_combo()

        self._frameStrip.update_strip_layout()

        self.animationSelectedChanged.emit(self._sprite.current_animation())

    def set_animation(self, index):

        if self._sprite is None:
            return

        self._sprite.set_animation(index)

        self._frameStrip.update_strip_layout()

        self.animationSelectedChanged.emit(self._sprite.current_animation())

    def remove_current_animation(self):

        if self._sprite is None:
            return

        self._sprite.remove_current_animation()

        self._update_animation_combo()

        self._frameStrip.update_strip_layout()

        self.animationSelectedChanged.emit(self._sprite.current_animation())

    def add_frame(self):

        if self._sprite is None:
            return

        current_animation = self._sprite.current_animation()

        current_animation.add_empty_frame()

        self._frameStrip.update_strip_layout()

        self.frameSelectedChanged.emit(current_animation.current_frame_index())

    def remove_frame(self, index=None):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        animation.remove_frame(index)

        if animation.frame_count() == 0:
            self.add_frame()

        self._frameStrip.update_strip_layout()

        self.frameSelectedChanged.emit(self._sprite.current_animation().current_frame_index())

    def copy_frame(self, index=None):

        if self._sprite is None:
            return

        current_animation = self._sprite.current_animation()

        current_animation.copy_frame(index)

        self._frameStrip.update_strip_layout()

        self.frameSelectedChanged.emit(current_animation.current_frame_index())

    def set_frame(self, index):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        animation.set_frame(index)

        self.update()

        self.frameSelectedChanged.emit(index)

    def go_to_next_frame(self):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        if animation.is_on_last_frame():
            return

        animation.go_to_next_frame()

        self.update()

        self.frameSelectedChanged.emit(animation.current_frame_index())

    def go_to_previous_frame(self):

        if self._sprite is None:
            return

        animation = self._sprite.current_animation()

        if animation.is_on_first_frame():
            return

        animation.go_to_previous_frame()

        self.update()

        self.frameSelectedChanged.emit(animation.current_frame_index())

    def start_refreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def stop_refreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False


    def on_window_resize(self, size):

        frame_strip_max_frames = int(math.floor((size.width() - (488)) / (self._frameStrip.total_frame_size())))
        self._frameStrip.set_max_frames_on_view(frame_strip_max_frames)


    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):

        super(AnimationManager, self).dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():

            current_animation = self._sprite.current_animation()

            for url in e.mimeData().urls():

                image = utils.load_image(url.toLocalFile())

                current_animation.add_frame(image)

            self._frameStrip.update_strip_layout()

            self.frameSelectedChanged.emit(current_animation.current_frame_index())

            self.update()

    def _on_add_animation_clicked(self):

        self.add_animation()

    def _on_remove_animation_clicked(self):

        self.remove_current_animation()

    def _on_animation_index_changed(self, index):

        if self._sprite is None:
            return

        if self._sprite.current_animation_index() != index:
            self.set_animation(index)

    def _on_animation_combo_edited(self, new_text):

        if self._sprite is None:
            return

        self._sprite.current_animation().set_name(new_text)

    def _on_add_frame_clicked(self):

        self.add_frame()

    def _on_remove_frame_clicked(self):

        self.remove_frame()

    def _on_copy_frame_clicked(self):

        self.copy_frame()

    def _on_framestrip_frame_selected_changed(self, index):

        self.set_frame(index)

    def _refresh_event(self):

        self.update()

    def _check_strip_size(self):

        if self._frameStrip.width() > self.width():
            self._frameStrip.advance_view()

    def _update_animation_combo(self):

        if self._sprite is None:
            return

        self._animationCombo.clear()

        for index, animation in enumerate(self._sprite.animations()):
            self._animationCombo.addItem(animation.name(), index)

        self._animationCombo.setCurrentIndex(self._sprite.current_animation_index())

        self.update()