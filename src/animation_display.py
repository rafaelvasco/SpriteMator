#-----------------------------------------------------------------------------------------------------------------------
# Name:        Animation Dispaly
# Purpose:     Display and animate a selected Animation from current Sprite
#
# Author:      Rafael Vasco
#
# Created:     07/07/2013
# Copyright:   (c) Rafael 2013
# Licence:
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QColor, QPen, QIcon, QPixmap
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton

from src.display import Display

# ----------------------------------------------------------------------------------------------------------------------


class AnimationDisplay(Display):
    def __init__(self, parent=None):

        super(AnimationDisplay, self).__init__(parent)
        self._animation = None
        self._playing = False
        self._refreshing = False
        self._refreshSpeed = 16
        self._animationSpeed = 60
        self._loopEnabled = True
        self._pen = QPen()
        self._pen.setColor(QColor(10, 10, 10))
        self._pen.setWidth(2)
        self._pen.setJoinStyle(Qt.MiterJoin)
        self._currentFrame = 0

        self._refreshTimer = QTimer()
        self._refreshTimer.timeout.connect(self._refresh_event)
        self._refreshTimer.stop()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._animationTimer = QTimer()
        self._animationTimer.timeout.connect(self._animate_event)
        self._animationTimer.stop()

        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignBottom)

        self._controlsLayout = QHBoxLayout()

        self._goNextFrameBtn = QPushButton()
        self._goNextFrameBtn.clicked.connect(self.go_to_next_frame)

        go_next_frame_icon = QIcon()
        go_next_frame_icon.addPixmap(QPixmap(":/icons/ico_next"))

        self._goNextFrameBtn.setIcon(go_next_frame_icon)
        self._goNextFrameBtn.setIconSize(QSize(14, 14))

        self._goPrevFrameBtn = QPushButton()
        self._goPrevFrameBtn.clicked.connect(self.go_to_previous_frame)

        go_prev_frame_icon = QIcon()
        go_prev_frame_icon.addPixmap(QPixmap(":/icons/ico_prev"))

        self._goPrevFrameBtn.setIcon(go_prev_frame_icon)
        self._goPrevFrameBtn.setIconSize(QSize(14, 14))

        self._playPauseBtn = QPushButton()
        self._playPauseBtn.setCheckable(True)
        self._playPauseBtn.clicked.connect(self.toggle_playing)

        play_frame_icon = QIcon()
        play_frame_icon.addPixmap(QPixmap(":/icons/ico_play"), QIcon.Normal, QIcon.Off)
        play_frame_icon.addPixmap(QPixmap(":/icons/ico_pause"), QIcon.Normal, QIcon.On)

        self._playPauseBtn.setIcon(play_frame_icon)
        self._playPauseBtn.setIconSize(QSize(14, 14))

        self._controlsLayout.addWidget(self._playPauseBtn)
        self._controlsLayout.addWidget(self._goPrevFrameBtn)
        self._controlsLayout.addWidget(self._goNextFrameBtn)

        self._layout.addLayout(self._controlsLayout)

    def is_playing(self):
        return self._playing

    def is_looping(self):
        return self._loopEnabled if self._animation is not None else False

    def set_looping(self, value):
        if self._animation is None:
            return

        self._loopEnabled = value

    def animation_speed(self):
        return self._animationSpeed

    def set_animation_speed(self, value):
        self._animationSpeed = value

    def start_refreshing(self):
        self._refreshTimer.start(self._refreshSpeed)
        self._refreshing = True

    def stop_refreshing(self):
        self._refreshTimer.stop()
        self._refreshing = False

    def start_animating(self):
        self._animationTimer.start(self._animationSpeed)
        self._playing = True

    def stop_animating(self):
        self._animationTimer.stop()
        self._playing = False

    def _refresh_event(self):
        self.update()

    def _animate_event(self):
        if self._animation is not None and self._playing:
            self._animate()

    def _animate(self):
        if self._animation is None:
            return

        self._currentFrame += 1
        frame_count = self._animation.frame_count()

        if self._currentFrame > frame_count - 1:

            if self._loopEnabled:
                self._currentFrame = 0
            else:
                self._currentFrame = frame_count - 1
                self.pause()

        self.update()

    def on_draw_object(self, event, painter):
        if self._animation is not None and self._animation.frame_count() > 0:

            layers = self._animation.frame_at(self._currentFrame).surfaces()

            for layer in layers:
                painter.drawImage(0, 0, layer.image())

    def set_animation(self, animation):
        if self._animation is not None:
            self.unload_animation()

        self._animation = animation

        self.set_object_size(self._animation.sprite().width(), self._animation.sprite().height())

        self._currentFrame = 0

        self.update()

    def unload_animation(self):
        self._animation = None
        self.set_object_size(0, 0)
        self._playing = False
        self._refreshing = False
        self._refreshTimer.stop()
        self._animationTimer.stop()
        self._playPauseBtn.setChecked(False)
        self._currentFrame = 0

        self.update()

    def toggle_playing(self):
        if self._animation is None:
            return

        if not self._playing:
            self._playPauseBtn.setChecked(True)
            self.play()
        else:
            self.pause()
            self._playPauseBtn.setChecked(False)

    def play(self):
        if self._animation is None:
            return

        self.start_animating()

        self.update()

    def pause(self):
        if self._animation is None:
            return

        self.stop_animating()

        self.update()

    def go_to_frame(self, index):
        if self._animation is None or self._playing:
            return

        self._currentFrame = index

        self.update()

    def go_to_next_frame(self):
        if self._animation is None or self._playing:
            return

        frame_count = self._animation.frame_count()

        self._currentFrame += 1

        if self._currentFrame > frame_count - 1:
            self._currentFrame = frame_count - 1

        self.update()

    def go_to_previous_frame(self):
        if self._animation is None or self._playing:
            return

        self._currentFrame -= 1

        if self._currentFrame < 0:
            self._currentFrame = 0

        self.update()
