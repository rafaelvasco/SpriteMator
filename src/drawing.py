# --------------------------------------------------------------------------------------------------
# Name:        Drawing
# Purpose:     Common drawing operations used by Canvas
#
# Author:      Rafael Vasco
#
# Created:     31/03/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


def erase_area(image, x, y, w, h):

    painter = QPainter()
    painter.begin(image)
    painter.setCompositionMode(QPainter.CompositionMode_Clear)
    painter.fillRect(x, y, w, h, Qt.transparent)
    painter.end()


def erase_area_painter_ready(x, y, w, h, painter):

    if painter.compositionMode() != QPainter.CompositionMode_Clear:
        painter.setCompositionMode(QPainter.CompositionMode_Clear)

    painter.setCompositionMode(QPainter.CompositionMode_Clear)
    painter.fillRect(x, y, w, h, Qt.transparent)


def draw_line(start, end, size, ink, color, painter):
    x1 = start.x()
    y1 = start.y()
    x2 = end.x()
    y2 = end.y()

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = size if (x1 < x2) else -size
    sy = size if (y1 < y2) else -size

    err = dx - dy

    while True:

        ink.blit(x1, y1, size, size, color, painter)

        if x1 == x2 and y1 == y2:
            break

        e2 = err * 2

        if e2 >= -dy:
            err -= dy
            x1 += sx

        if e2 <= dx:
            err += dx
            y1 += sy
