# ------------------------------------------------------------------------------
# Name:        CanvasOverlay
# Purpose:     Represents canvas overlay where tools icon, selection, etc is drawn on;
#
# Author:      Rafael Vasco
#
# Created:     21/09/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#------------------------------------------------------------------------------
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QWidget

#------------------------------------------------------------------------------


class CanvasOverlay(QWidget):
    def __init__(self, canvas):
        super(CanvasOverlay, self).__init__(canvas)
        self._canvas = canvas
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def sizeHint(self):
        return QSize(self._canvas.width(), self._canvas.height())

    def paintEvent(self, e):
        if self._canvas.current_tool is None:
            return

        painter = QPainter(self)

        self._canvas.draw_overlay(painter)

