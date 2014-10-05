import struct
import numpy as np
cimport numpy as np

cdef extern from "math.h":

    double floor(double x)


# -----------------------------------------------------------------------------

cpdef movePixels(object imageData, int w, int h, int shiftX, int shiftY):
    
    cdef int length = w * h * 4

    cdef np.uint8_t[::1] byteArray = np.frombuffer(imageData, np.uint8).reshape(length)

    cdef np.uint8_t[::1] auxByteArray = np.copy(byteArray)

    cdef Py_ssize_t colorIndex = 0
    cdef Py_ssize_t colorIndexAux = 0

    cdef int x = 0
    cdef int y = 0
    cdef int auxX = 0
    cdef int auxY = 0

    while x < w:

        auxX = x + shiftX
        
        if auxX >= w:
            auxX -= w

        y = 0

        while y < h:

            auxY = y + shiftY

            if auxY >= h:
                auxY -= h

            colorIndex = (x + y * w)*4
            colorIndexAux = (auxX + auxY * w)*4

            
            byteArray[colorIndexAux + 2] = auxByteArray[colorIndex + 2]
            byteArray[colorIndexAux + 1] = auxByteArray[colorIndex + 1]
            byteArray[colorIndexAux + 0] = auxByteArray[colorIndex + 0]
            byteArray[colorIndexAux + 3] = auxByteArray[colorIndex + 3]

            y += 1

        x += 1

# -----------------------------------------------------------------------------

cpdef blackWhite(object imageData, int w, int h):

    cdef int length = w * h * 4

    cdef Py_ssize_t i = 0

    cdef unsigned int grayScale = 0

    cdef np.uint8_t[::1] byteArray = np.frombuffer(imageData, np.uint8).reshape(length)

    while i < length:

        grayScale = <unsigned int>((byteArray[i + 2])*0.3 + (byteArray[i + 1])*0.59 + (byteArray[i])*0.11)

        byteArray[i + 2] = grayScale
        byteArray[i + 1] = grayScale
        byteArray[i] = grayScale

        i += 4

# -----------------------------------------------------------------------------

cpdef floodFill(object imageData, int x, int y, int w, int h, int r, int g, int b):
    
    cdef int length = w*h*4

    cdef int w4 = w*4

    cdef np.uint8_t[::1] byteArray = np.frombuffer(imageData, np.uint8).reshape(length)

    cdef Py_ssize_t colorIndex = (x + y * w)*4

    cdef unsigned int cr = byteArray[colorIndex + 2]
    cdef unsigned int cg = byteArray[colorIndex + 1]
    cdef unsigned int cb = byteArray[colorIndex]
    cdef unsigned int ca = byteArray[colorIndex + 3]


    if ca != 0 and r == cr and g == cg and b == cb:
        return

    cdef list stack = []

    cdef int left = 0
    cdef int right = 0

    cdef int leftBoundary = 0
    cdef int rightBoundary = 0

    stack.append(colorIndex)

    while len(stack) > 0:

        colorIndex = stack.pop()
        
        if byteArray[colorIndex + 2] == cr and byteArray[colorIndex + 1] == cg and byteArray[colorIndex] == cb and byteArray[colorIndex + 3] == ca:

            left = colorIndex - 4
            right = colorIndex + 4

            leftBoundary = <int>(floor(left / w4) * w4)
            rightBoundary = leftBoundary + w4

            if left > 0:

                while left > leftBoundary and byteArray[left + 2] == cr and byteArray[left + 1] == cg and byteArray[left] == cb and byteArray[left + 3] == ca:

                    left -= 4

            if right < length:

                while right < rightBoundary and byteArray[right + 2] == cr and byteArray[right + 1] == cg and byteArray[right] == cb and byteArray[right + 3] == ca:
                        
                    right += 4

            if byteArray[left + 2] != cr or byteArray[left + 1] != cg or byteArray[left] != cb or byteArray[left + 3] != ca:

                left += 4

            while left < right:
                
                byteArray[left + 2] = r
                byteArray[left + 1] = g
                byteArray[left] = b
                byteArray[left + 3] = 255

                colorIndex = left - w4

                if colorIndex >= 0 and byteArray[colorIndex + 2] == cr and byteArray[colorIndex + 1] == cg and byteArray[colorIndex] == cb and byteArray[colorIndex + 3] == ca:
        
                    stack.append(colorIndex)

                colorIndex = left + w4

                if colorIndex < length and byteArray[colorIndex + 2] == cr and byteArray[colorIndex + 1] == cg and byteArray[colorIndex] == cb and byteArray[colorIndex + 3] == ca:

                    stack.append(colorIndex)

                left += 4

# -----------------------------------------------------------------------------




