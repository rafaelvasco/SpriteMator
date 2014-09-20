"""
Rectangle packer using an algorithm by Javier Arevalo.
http://www.flipcode.com/archives/Rectangle_Placement.shtml
http://kossovsky.net/index.php/2009/07/cshar-rectangle-packing/

You have a bunch of rectangular pieces. You need to arrange them in a rectangular surface
so that they don't overlap, keeping the total area of the rectangle as small as possible.
This is fairly common when arranging characters in a bitmapped font, lightmaps for a 3D
engine, and I guess other situations as well.

The idea of self.algorithm is that, as we add rectangles, we can pre-select "interesting"
places where we can try to add the next rectangles. For optimal results, the rectangles
should be added in order. I initially tried using area as a sorting criteria, but it
didn't work well with very tall or very flat rectangles. I then tried using the longest
dimension as a selector, and it worked much better. So much for intuition... These
"interesting" places are just to the right and just below the currently added rectangle.
The first rectangle, obviously, goes at the top left, the next one would go either to the
right or below self.one, and so on. It is a weird way to do it, but it seems to work very
nicely. The way we search here is fairly brute-force, the fact being that for most
off-line purposes the performance seems more than adequate. I have generated a japanese
font with around 8500 characters and all the time was spent generating the bitmaps. Also,
for all we care, we could grow the parent rectangle in a different way than power of two.
It just happens that power of 2 is very convenient for graphics hardware textures. I'd be
interested in hearing of other approaches to self.problem. Make sure to post them on
http:#www.flipcode.com

Original code by Javier Arevalo (jare at iguanademos dot com). Rewritten
to C# / .NET by Markus Ewald (cygon at nuclex dot org).

C# code translated to Python and improved by leonardo maffi, V.1.0, Jul 12 2009.
This version is faster for few large rectangles.

-----------------

Nuclex Framework
Copyright (C) 2002-2009 Nuclex Development Labs

This library is free software; you can redistribute it and/or
modify it under the terms of the IBM Common Public License as
published by the IBM Corporation; either version 1.0 of the
License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
IBM Common Public License for more details.

You should have received a copy of the IBM Common Public
License along with self.library
"""

from bisect import insort
from array import array


class Anchor(object):

    """
        Anchoring points are potential locations for the placement of new rectangles.
        Each time a rectangle is inserted, an anchor point is generated on its upper
        right end and another one at its lower left end. The anchor points are kept
        in a list that is ordered by their closeness to the upper left corner of the
        packing area (their 'rank') so the packer favors positions that are closer to
        the upper left for new rectangles.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x + self.y < other.x + other.y


class RectanglePacker(object):
    def __init__(self, max_width, max_height):

        """
        max_width, max_height: maximum width,height of the packing area.
        """

        self._max_packing_area_width = max_width
        self._max_packing_area_height = max_height

        # Rectangles contained in the packing area
        self._rectangles = []

        # Anchoring points where new rectangles can potentially be placed
        self._anchors = [Anchor(0, 0)]

        # Current width,height of the packing area
        self._actual_packing_area_width = 1
        self._actual_packing_area_height = 1

        # matrix of bits, to store where it's covered by rectangles
        self._bitmatrix = array("B", [0]) * (max_width * max_height)

    def actual_packing_area_width(self):
        return self._actual_packing_area_width

    def actual_packing_area_height(self):
        return self._actual_packing_area_height

    def pack(self, rect_width, rect_height):

        """
        Tries to allocate space for a rectangle in the packing area.
        rect_width, rect_height: width,height of the rectangle to allocate.
        returns: an Anchor that represents the placement, if a space can be found.
          Or None if no placement can be found.
        """

        # Try to find an anchor where the rectangle fits in, enlarging the packing
        # area and repeating the search recursively until it fits or the
        # maximum allowed size is exceeded.
        anchor_idx = self._select_anchor(rect_width, rect_height, self._actual_packing_area_width,
                                         self._actual_packing_area_height)

        # No anchor could be found at which the rectangle did fit in
        if anchor_idx == -1:
            return None

        placement = self._anchors[anchor_idx]

        # Move the rectangle either to the left or to the top until it collides with
        # a neightbouring rectangle. This is done to combat the effect of lining up
        # rectangles with gaps to the left or top of them because the anchor that
        # would allow placement there has been blocked by another rectangle
        self._optimize_placement(placement, rect_width, rect_height)

        # Remove the used anchor and add new anchors at the upper right and lower left
        # positions of the new rectangle

        # The anchor is only removed if the placement optimization didn't
        # move the rectangle so far that the anchor isn't blocked anymore
        if ((placement.x + rect_width) > self._anchors[anchor_idx].x) and \
                ((placement.y + rect_height) > self._anchors[anchor_idx].y):
            del self._anchors[anchor_idx]

        # Add new anchors at the upper right and lower left coordinates of the rectangle
        insort(self._anchors, Anchor(placement.x + rect_width, placement.y))
        insort(self._anchors, Anchor(placement.x, placement.y + rect_height))

        # Finally, we can add the rectangle to our packed rectangles list
        self._rectangles.append([placement.x, placement.y, rect_width, rect_height])

        shift = placement.y * self._max_packing_area_width
        for y in range(rect_height):
            start_line_pos = placement.x + shift
            shift += self._max_packing_area_width
            for i in range(start_line_pos, rect_width + start_line_pos):
                self._bitmatrix[i] = 1

        return placement

    def _optimize_placement(self, placement, rect_width, rect_height):

        """
        Optimizes the rectangle's placement by moving it either left or up to fill
        any gaps resulting from rectangles blocking the anchors of the most optimal
        placements.

        placement: Placement to be optimized.
        rect_width,rect_height: width,height of the rectangle to be optimized.
        """
        rect = [placement.x, placement.y, rect_width, rect_height]

        # Try to move the rectangle to the left as far as possible
        left_most = placement.x
        while self._is_free(rect, self._max_packing_area_width, self._max_packing_area_height):
            left_most = rect[0]
            rect[0] -= 1  # looks slow, there can be a way to move faster

        # Reset rectangle to original position
        rect[0] = placement.x

        # Try to move the rectangle upwards as far as possible
        top_most = placement.y
        while self._is_free(rect, self._max_packing_area_width, self._max_packing_area_height):
            top_most = rect[1]
            rect[1] -= 1  # looks slow, there can be a way to move faster

        # Use the dimension in which the rectangle could be moved farther
        if placement.x - left_most > placement.y - top_most:
            placement.x = left_most
        else:
            placement.y = top_most

    def _select_anchor(self, rect_width, rect_height, total_packing_area_width,
                       total_packing_area_height):
        """
        Searches for a free anchor and recursively enlarges the packing area
        if none can be found.

        rect_width,rect_height: width,height of the rectangle to be placed.
        total_packing_area_width,total_packing_area_height: width,height of the tested packing area.
        Return: ondex of the anchor the rectangle is to be placed at or -1 if the rectangle
        does not fit in the packing area anymore.
        """
        # Try to locate an anchor powhere the rectangle fits in
        free_anchor_idx = self._find_anchor(rect_width, rect_height,
                                            total_packing_area_width, total_packing_area_height)

        # If a the rectangle fits without resizing packing area (any further in case
        # of a recursive call), take over the new packing area size and return the
        # anchor at which the rectangle can be placed.
        if free_anchor_idx != -1:
            self._actual_packing_area_width = total_packing_area_width
            self._actual_packing_area_height = total_packing_area_height
            return free_anchor_idx

        # If we reach self.point, the rectangle did not fit in the current packing
        # area and our only choice is to try and enlarge the packing area.

        # For readability, determine whether the packing area can be enlarged
        # any further in its width and in its height
        can_enlarge_width = total_packing_area_width < self._max_packing_area_width
        can_enlarge_height = total_packing_area_height < self._max_packing_area_height
        should_enlarge_height = (not can_enlarge_width) or (total_packing_area_height <
                                                            total_packing_area_width)

        # Try to enlarge the smaller of the two dimensions first (unless the smaller
        # dimension is already at its maximum size). 'shouldEnlargeHeight' is True
        # when the height was the smaller dimension or when the width is maxed out.
        if can_enlarge_height and should_enlarge_height:
            # Try to double the height of the packing area
            return self._select_anchor(rect_width, rect_height, total_packing_area_width,
                                       min(total_packing_area_height * 2,
                                           self._max_packing_area_height))
        elif can_enlarge_width:
            # Try to double the width of the packing area
            return self._select_anchor(rect_width, rect_height,
                                       min(total_packing_area_width * 2,
                                           self._max_packing_area_width),
                                       total_packing_area_height)
        else:
            # Both dimensions are at their maximum sizes and the rectangle still
            # didn't fit. We give up!
            return -1

    def _find_anchor(self, rect_width, rect_height, total_packing_area_width,
                     total_packing_area_heigh):
        """
        Locates the first free anchor at which the rectangle fits.

        rect_width,rect_height: width,height of the rectangle to be placed.
        total_packing_area_width,total_packing_area_heigh: total width,height of the packing area.
        returns: the index of the first free anchor or -1 if none is found.
        """
        possible_pos = [0, 0, rect_width, rect_height]

        # Walk over all anchors (which are ordered by their distance to the
        # upper left corner of the packing area) until one is discovered that
        # can house the new rectangle.
        self_anchors = self._anchors
        self_is_free = self._is_free
        for i in range(len(self_anchors)):  # low level loop for Psyco
            possible_pos[0] = self_anchors[i].x
            possible_pos[1] = self_anchors[i].y

            # See if the rectangle would fit in at self.anchor point
            if self_is_free(possible_pos, total_packing_area_width, total_packing_area_heigh):
                return i

        # No anchor points were found where the rectangle would fit in
        return -1

    def _is_free(self, rect, total_packing_area_width, total_packing_area_height):
        """
        Determines whether the rectangle can be placed in the packing area
        at its current location.

        rect: Rectangle whose position to check.
        total_packing_area_width,total_packing_area_height: total width,height of the packing area.
        returns: True if the rectangle can be placed at its current position.
        """
        # If the rectangle is partially or completely outside of the packing
        # area, it can't be placed at its current location
        if (rect[0] < 0) or (rect[1] < 0) or \
                ((rect[0] + rect[2]) > total_packing_area_width) or \
                ((rect[1] + rect[3]) > total_packing_area_height):
            return False

        # Brute-force search whether the rectangle touches any of the other
        # rectangles already in the packing area
        # return not any(r.intersects(rect) for r in self._rectangles) #slower

        # quick test, this eliminates 99%+ rects
        self_bitmatrix = self._bitmatrix
        pos = rect[0] + rect[1] * self._max_packing_area_width
        if self_bitmatrix[pos] or self_bitmatrix[pos + rect[2] - 1] or \
                self_bitmatrix[rect[0] + (rect[1] + rect[3] - 1) * self._max_packing_area_width] or \
                self_bitmatrix[rect[0] + rect[2] - 1 + (rect[1] + rect[3] - 1) *
                        self._max_packing_area_width]:
            return False

        # full test
        shift = rect[1] * self._max_packing_area_width
        for y in range(rect[3]):
            start_line_pos = rect[0] + shift
            shift += self._max_packing_area_width
            for i in range(start_line_pos, rect[2] + start_line_pos):
                if self_bitmatrix[i]:
                    return False

        # Success! The rectangle is inside the packing area and doesn't overlap
        # with any other rectangles that have already been packed.
        return True