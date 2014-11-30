from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class OptionsBar(QWidget):

    toggledGrid = pyqtSignal(bool)
    toggledOnionSkin = pyqtSignal(bool)
    toggledLights = pyqtSignal(bool)

    def __init__(self, canvas):
        super(OptionsBar, self).__init__()

        self._layout = QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self._layout.setAlignment(Qt.AlignLeft)
        self._backgroundColor = QColor(10, 10, 10)

        self._toggleGridButton = QPushButton()
        self._toggleOnionSkinButton = QPushButton()
        self._toggleLightsButton = QPushButton()

        self._initialize_components(canvas)
        self._initialize_style()

        self.setLayout(self._layout)

    def _initialize_components(self, canvas):

        # --- Toggle Grid Button ----------------------

        self._toggleGridButton.setText("GRID")
        self._toggleGridButton.setFlat(True)
        self._toggleGridButton.setCheckable(True)
        self._toggleGridButton.setChecked(canvas.grid_enabled)
        self._toggleGridButton.toggled.connect(lambda checked: self.toggledGrid.emit(checked))

        self._layout.addWidget(self._toggleGridButton)

        # --- Toggle Onion Skin Button

        self._toggleOnionSkinButton.setText("ONION SKIN")
        self._toggleOnionSkinButton.setFlat(True)
        self._toggleOnionSkinButton.setCheckable(True)
        self._toggleOnionSkinButton.setChecked(canvas.sprite_object.enable_onion_skin)
        self._toggleOnionSkinButton.toggled.connect(
            lambda checked: self.toggledOnionSkin.emit(checked))

        self._layout.addWidget(self._toggleOnionSkinButton)

        # --- Toggle Lights Button

        self._toggleLightsButton.setText("LIGHTS")
        self._toggleLightsButton.setFlat(True)
        self._toggleLightsButton.setCheckable(True)
        self._toggleLightsButton.setChecked(canvas.backlight_enabled)
        self._toggleLightsButton.toggled.connect(
            lambda checked: self.toggledLights.emit(checked))

        self._layout.addWidget(self._toggleLightsButton)

    def _initialize_style(self):

        style_sheet = """

            QPushButton
            {
                background: #222;
                border: none;
                font-size: 16px;
                color: white;
            }

            QPushButton:checked
            {
                background: #44859E;

            }

        """

        self.setStyleSheet(style_sheet)

        # ---------------------------------------------

    def paintEvent(self, e):

        painter = QPainter(self)

        painter.setOpacity(0.5)
        painter.fillRect(self.rect(), self._backgroundColor)

    def sizeHint(self):
        return QSize(0, 26)