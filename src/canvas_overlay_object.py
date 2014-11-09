from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtWidgets import QGraphicsItem


class CanvasOverlayObject(QGraphicsItem):
    def __init__(self, canvas):

        super(CanvasOverlayObject, self).__init__()

        self._boundingRect = QRectF()

        self._canvas = canvas

        self.update_bounding_rect()

    def boundingRect(self):
        return self._canvas.sprite_object.boundingRect()

    def update_bounding_rect(self):

        sprite_width = self._canvas.sprite_object.width
        sprite_height = self._canvas.sprite_object.height

        if (self._boundingRect.width() != sprite_width or
                self._boundingRect.height() != sprite_height):

            self.prepareGeometryChange()
            self._boundingRect = QRectF(-sprite_width / 2, -sprite_height / 2,
                                        sprite_width, sprite_height)

    def paint(self, painter, option, widget=None):

        if self._canvas.grid_enabled and self._canvas.zoom >= 8.0:

            self._draw_grid(painter)

        if self._canvas.current_tool is not None:
            self._canvas.current_tool.draw_transformed(painter)

    def _draw_grid(self, painter):
        pen = QPen()
        pen.setWidth(0)
        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.setOpacity(0.3)

        painter.setCompositionMode(QPainter.CompositionMode_Difference)

        scene_rect = self._canvas.sceneRect()

        for x in range(int(scene_rect.left()), int(scene_rect.right())):

            painter.drawLine(x, scene_rect.top(), x, scene_rect.bottom())

        for y in range(int(scene_rect.top()), int(scene_rect.bottom())):

            painter.drawLine(scene_rect.left(), y, scene_rect.right(), y)

        painter.setOpacity(1.0)
