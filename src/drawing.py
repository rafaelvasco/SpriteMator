#-----------------------------------------------------------------------------------------------------------------------
# Name:        Drawing
# Purpose:     Common drawing operations used by Canvas
#
# Author:      Rafael Vasco
#
# Created:     31/03/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtGui import QPainter


def paste_image(image_to_paste, target_image):
    
    painter = QPainter()
    painter.begin(target_image)
    painter.drawImage(0, 0, image_to_paste)
    painter.end()


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
