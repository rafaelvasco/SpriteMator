#------------------------------------------------------------------------------
# Name:             Utilitarian functions
# Purpose:          
#
# Author:           Rafael
# Date:             24/03/13
# License:          
#------------------------------------------------------------------------------

import os
import math

from PyQt4.QtCore import Qt, QDir, QByteArray, QBuffer, QIODevice
from PyQt4.QtGui import QImage, QFileDialog, QMatrix



def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

# -----------------------------------------------------------------------------

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# -----------------------------------------------------------------------------

def sign(v):
    return cmp(v, 0)

# -----------------------------------------------------------------------------

def cmp(a, b):
    return (a > b) - (a < b)

# -----------------------------------------------------------------------------

def snap(value, increment):
    return int(math.floor(value // increment) * increment)


def snapPoint(point, increment):

    point.setX(round(math.floor(point.x() / increment) * increment))
    point.setY(round(math.floor(point.y() / increment) * increment))

# -----------------------------------------------------------------------------

def createImage(width, height):
    newImage = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    newImage.fill(Qt.transparent)
    return newImage

# -----------------------------------------------------------------------------

def loadImage(file):
    newImage = QImage(file)
    return newImage.convertToFormat(QImage.Format_ARGB32_Premultiplied)

# -----------------------------------------------------------------------------

def getFileExtension(filePath):
    return os.path.splitext(filePath)[1].lower()

# -----------------------------------------------------------------------------

def showOpenFileDialog(label, nameFilter):
    return QFileDialog.getOpenFileName(caption = label,
                                       directory = QDir.currentPath(),
                                       filter = nameFilter)

def showOpenFilesDialog(label, nameFilter):
    return QFileDialog.getOpenFileNames(caption = label,
                                        directory = QDir.currentPath(),
                                        filter = nameFilter)


# -----------------------------------------------------------------------------

def showSaveFileDialog(label, nameFilter):
    return QFileDialog.getSaveFileName(caption = label,
                                       directory = QDir.currentPath(),
                                       filter = nameFilter)

# -----------------------------------------------------------------------------

def imageToByteArray(image):
    byteArray = QByteArray()
    buffer = QBuffer(byteArray)
    buffer.open(QIODevice.WriteOnly)
    image.save(buffer, 'png')
    buffer.close()
    return  byteArray

# -----------------------------------------------------------------------------

def byteArrayToImage(byteArray):
    image = QImage()
    image.loadFromData(byteArray, 'png')
    return image

# -----------------------------------------------------------------------------

def multiplyMatrix(m1, m2):

    m1_11 = m1.m11()
    m1_12 = m1.m12()
    m1_21 = m1.m21()
    m1_22 = m1.m22()
    m1_dx = m1.dx()
    m1_dy = m1.dy()

    m2_11 = m2.m11()
    m2_12 = m2.m12()
    m2_21 = m2.m21()
    m2_22 = m2.m22()
    m2_dx = m2.dx()
    m2_dy = m2.dy()

    return QMatrix(	m1_11 * m2_11 + m1_21 * m2_12,
					m1_12 * m2_11 + m1_22 * m2_12,
					m1_11 * m2_21 + m1_21 * m2_22,
					m1_12 * m2_21 + m1_22 * m2_22,
					round(m1_dx *m2_11 + m1_dy * m2_12 + m2_dx),
					round(m1_dx * m2_21 + m1_dy * m2_22 + m2_dy))

# -----------------------------------------------------------------------------


