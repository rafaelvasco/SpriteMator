# -------------------------------------------------------------------------------------------------
# Name:        Inks
# Purpose:     Inks module used by Canvas. An Ink is a visual representation of a tool acting
#              on the Canvas
# Author:      Rafael Vasco
#
# Created:     28/04/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#--------------------------------------------------------------------------------------------------

from src.model.properties import PropertyHolder

import src.helpers.drawing as drawing


class Ink(PropertyHolder):
    def __init__(self):
        super(Ink, self).__init__()

        self._name = ''

    @property
    def name(self):
        return self._name

    def blit(self, x, y, w, h, color, painter):
        return


class Solid(Ink):
    def __init__(self):
        super(Solid, self).__init__()
        self._name = 'Solid'
        self.add_property(prop_name='Test', prop_value=True, prop_description='Test Property')

    def blit(self, x, y, w, h, color, painter):
        painter.fillRect(x, y, w, h, color)


class Eraser(Ink):
    def __init__(self):
        super(Eraser, self).__init__()
        self._name = 'Eraser'

    def blit(self, x, y, w, h, color, painter):

        drawing.erase_area_painter_ready(x, y, w, h, painter)
