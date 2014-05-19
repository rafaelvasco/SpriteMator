import struct



import numpy as np
cimport numpy as np

cdef extern from "math.h":

	double floor(double x)


from libc.stdlib cimport malloc, free


cpdef flipX(object imageData, int w, int h):
	
	#cdef np.uint8_t[:,:] byteArray = np.frombuffer(imageData, np.uint8).reshape((w*4,h))

	record = [('b','u1'), ('g','u1'), ('r','u1'), ('a','u1')]

	cdef byteArray = np.ndarray(shape=(h,w), dtype=record, buffer=imageData)

	np.fliplr(byteArray)


cpdef blackWhite(object imageData, int w, int h):

	cdef int length = w * h * 4

	cdef int i = 0

	cdef unsigned int grayScale = 0

	cdef np.uint8_t[::1] byteArray = np.frombuffer(imageData, np.uint8).reshape(length)

	while i < length:

		grayScale = <unsigned int>((byteArray[i + 2])*0.3 + (byteArray[i + 1])*0.59 + (byteArray[i])*0.11)

		byteArray[i + 2] = grayScale
		byteArray[i + 1] = grayScale
		byteArray[i] = grayScale

		i += 4




cpdef floodFill(object imageData, int x, int y, int w, int h, int r, int g, int b):
	
	cdef int length = w*h*4

	cdef int w4 = w*4

	cdef np.uint8_t[::1] byteArray = np.frombuffer(imageData, np.uint8).reshape(length)

	cdef int colorIndex = (x + y * w)*4

	cdef int i = 0


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




