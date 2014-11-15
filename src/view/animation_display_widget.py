# ----------------------------------------------------------------------------
# Name:        Animation Dispaly
# Purpose:     Display and animate a selected Animation from current Sprite
#
# Author:      Rafael Vasco
#
# Created:     07/07/2013
# Copyright:   (c) Rafael 2013
# Licence:
# ------------------------------------------------------------------------------

import math

from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QColor, QPen, QIcon, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSlider, \
    QLabel, QFrame

from src.view.display_base_widget import Display

# -----------------------------------------------------------------------------


class AnimationDisplay(Display):
    def __init__(self):

        super(AnimationDisplay, self).__init__()

        self.background_color = QColor(220, 220, 220)

        self._playing = False

        style_sheet = \
            """
            QPushButton
            {
                background: rgba(30,30,30,50);
                border: 1px solid rgba(30,30,30,10);
            }

            QPushButton:hover
            {
                background: rgba(30,30,30,200);
                border: 1px solid rgba(30,30,30,200);
            }



        """

        self.setStyleSheet(style_sheet)

        self._animationFrameInterval = 60

        self._loopEnabled = True

        self._pen = QPen()
        self._pen.setColor(QColor(10, 10, 10))
        self._pen.setWidth(2)
        self._pen.setJoinStyle(Qt.MiterJoin)

        self._animationTimer = QTimer()
        self._animationTimer.timeout.connect(self._animate_event)
        self._animationTimer.stop()

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)

        self._buttonsLayout = QHBoxLayout()

        self._goNextFrameBtn = QPushButton()
        self._goNextFrameBtn.setFixedHeight(20)
        self._goNextFrameBtn.clicked.connect(self.go_to_next_frame)

        go_next_frame_icon = QIcon()
        go_next_frame_icon.addPixmap(QPixmap(":/icons/ico_next"))

        self._goNextFrameBtn.setIcon(go_next_frame_icon)
        self._goNextFrameBtn.setIconSize(QSize(14, 14))

        self._goPrevFrameBtn = QPushButton()
        self._goPrevFrameBtn.setFixedHeight(20)
        self._goPrevFrameBtn.clicked.connect(self.go_to_previous_frame)

        go_prev_frame_icon = QIcon()
        go_prev_frame_icon.addPixmap(QPixmap(":/icons/ico_prev"))

        self._goPrevFrameBtn.setIcon(go_prev_frame_icon)
        self._goPrevFrameBtn.setIconSize(QSize(14, 14))

        self._playPauseBtn = QPushButton()
        self._playPauseBtn.setFixedHeight(20)
        self._playPauseBtn.setCheckable(True)
        self._playPauseBtn.clicked.connect(self.toggle_playing)

        play_frame_icon = QIcon()
        play_frame_icon.addPixmap(QPixmap(":/icons/ico_play"), QIcon.Normal,
                                  QIcon.Off)
        play_frame_icon.addPixmap(QPixmap(":/icons/ico_pause"), QIcon.Normal,
                                  QIcon.On)

        self._playPauseBtn.setIcon(play_frame_icon)
        self._playPauseBtn.setIconSize(QSize(14, 14))

        self._buttonsLayout.addWidget(self._playPauseBtn)
        self._buttonsLayout.addWidget(self._goPrevFrameBtn)
        self._buttonsLayout.addWidget(self._goNextFrameBtn)

        # ----------------------------------------------------

        self._frameRatePanel = QFrame()
        self._frameRatePanel.setStyleSheet(
            "background: #333; border: 1px solid #4d4d4d;")

        self._frameRateLayout = QHBoxLayout()
        self._frameRateLayout.setContentsMargins(2, 2, 2, 2)

        self._frameRatePanel.setLayout(self._frameRateLayout)

        self._frameRateLabel = QLabel('Frame Rate (FPS): ')
        self._frameRateLabel.setStyleSheet("border: none;")

        self._frameRateValueLabel = QLabel('')
        self._frameRateValueLabel.setStyleSheet("border: none;")
        self._frameRateValueLabel.setMinimumWidth(14)

        self._frameRateSlider = QSlider(Qt.Horizontal)
        self._frameRateSlider.setMinimum(1)
        self._frameRateSlider.setMaximum(60)
        self._frameRateSlider.valueChanged.connect(
            self._on_animation_rate_changed)

        self._frameRateSlider.setValue(16)

        self._frameRateLayout.addWidget(self._frameRateLabel)
        self._frameRateLayout.addWidget(self._frameRateSlider)
        self._frameRateLayout.addWidget(self._frameRateValueLabel)

        self._layout.addLayout(self._buttonsLayout)
        self._layout.addWidget(self._frameRatePanel)

    @property
    def is_playing(self):
        return self._playing

    @property
    def looping_enabled(self):
        return self._loopEnabled if self._spriteObject is not None else False

    @looping_enabled.setter
    def looping_enabled(self, value):
        self._loopEnabled = value

    @property
    def animation_speed(self):
        return self._animationFrameInterval

    @animation_speed.setter
    def animation_speed(self, value):
        self._animationFrameInterval = value

    def start_animating(self):
        self._animationTimer.start(self._animationFrameInterval)
        self._playing = True

    def stop_animating(self):
        self._animationTimer.stop()
        self._playing = False

    def reset(self):

        self._playing = False
        self._animationTimer.stop()
        self._playPauseBtn.setChecked(False)

    def _animate_event(self):
        if self._spriteObject is not None and self._playing:
            self._animate()

    def _on_animation_rate_changed(self, v):

        self._frameRateValueLabel.setText(str(v))
        self._animationFrameInterval = int(math.floor((1 / v) * 1000))

        if self.is_playing:
            self._animationTimer.stop()
            self._animationTimer.start(self._animationFrameInterval)

    def _animate(self):
        if self._spriteObject is None:
            return

        self._spriteObject.display_frame_index += 1

        frame_count = self._spriteObject.sprite.current_animation.frame_count

        if self._spriteObject.display_frame_index > frame_count - 1:

            if self._loopEnabled:
                self._spriteObject.display_frame_index = 0
            else:
                self._spriteObject.display_frame_index = frame_count - 1
                self.pause()

        self.scene().update()

    def set_sprite(self, sprite):

        if not self._spriteObject.is_empty:
            self.unload_sprite()

        self._spriteObject.set_sprite(sprite)

        self.update_viewport()

        self._spriteObject.display_frame_index = 0

        self.scene().update()

    def unload_sprite(self):

        super(AnimationDisplay, self).unload_sprite()

        self.reset()

    def toggle_playing(self):
        if self._spriteObject is None:
            return

        if not self._playing:
            self._playPauseBtn.setChecked(True)
            self.play()
        else:
            self.pause()
            self._playPauseBtn.setChecked(False)

    def play(self):
        if self._spriteObject is None:
            return

        self.start_animating()

        self.scene().update()

    def pause(self):
        if self._spriteObject is None:
            return

        self.stop_animating()

        self.scene().update()

    def go_to_frame(self, index):
        if self._spriteObject is None or self._playing:
            return

        self._spriteObject.display_frame_index = index

        self.scene().update()

    def go_to_next_frame(self):
        if self._spriteObject is None or self._playing:
            return

        frame_count = self._spriteObject.sprite.current_animation.frame_count

        self._spriteObject.display_frame_index += 1

        if self._spriteObject.display_frame_index > frame_count - 1:
            self._spriteObject.display_frame_index = frame_count - 1

        self.scene().update()

    def go_to_previous_frame(self):

        if self._spriteObject is None or self._playing:
            return

        self._spriteObject.display_frame_index -= 1

        if self._spriteObject.display_frame_index < 0:
            self._spriteObject.display_frame_index = 0

        self.scene().update()
