from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class OptionsBar(QWidget):
    def __init__(self):
        super(OptionsBar, self).__init__()

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignLeft)
        self._backgroundColor = QColor(10, 10, 10)

        self._toggleGridButton = QPushButton()

        self._initialize_components()

        self.setLayout(self._layout)

    def _initialize_components(self):

        # --- Toggle Grid Button ----------------------

        self._toggleGridButton.setText("GRID")
        self._toggleGridButton.setFlat(True)
        self._toggleGridButton.setCheckable(True)

        style_sheet = """

            background: #222;
            border: none;
            font-size: 16px;

        """

        self._toggleGridButton.setStyleSheet(style_sheet)

        self._layout.addWidget(self._toggleGridButton)

        # ---------------------------------------------

    def paintEvent(self, e):

        painter = QPainter(self)

        painter.setOpacity(0.5)
        painter.fillRect(self.rect(), self._backgroundColor)

    def sizeHint(self):
        return QSize(0, 26)