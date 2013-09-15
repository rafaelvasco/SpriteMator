#--------------------------------------------------
# Purpose:          Drawing Helpers.
#
# Author:           Rafael Vasco
# Date:             31/03/13
# License:          
#--------------------------------------------------




def drawLine(start, end, size, ink, painter):

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

        ink.blit(x1, y1, size, size, painter)

        if x1 == x2 and y1 == y2:
            break

        e2 = err * 2

        if e2 >= -dy:
            err -= dy
            x1 += sx

        if e2 <= dx:
            err += dx
            y1 += sy
