from PyQt5 import Qt
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QButtonGroup


class PixelSizeWidget(QWidget):

    pixelSizeChanged = pyqtSignal(int)

    def __init__(self):

        super(PixelSizeWidget, self).__init__()

        self._layout = QHBoxLayout()

        self._button_group = QButtonGroup()
        self._button_group.buttonClicked.connect(self._onButtonChecked)

        self._1pxButton = QPushButton()
        self._1pxButton.setCheckable(True)
        self._1pxButton.setProperty("pixel_size", 1)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/ico_1px"), QIcon.Normal, QIcon.Off)

        self._1pxButton.setIcon(icon)
        self._1pxButton.setIconSize(QSize(21, 21))


        self._2pxButton = QPushButton()
        self._2pxButton.setCheckable(True)
        self._2pxButton.setProperty("pixel_size", 2)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/ico_2px"), QIcon.Normal, QIcon.Off)

        self._2pxButton.setIcon(icon)
        self._2pxButton.setIconSize(QSize(21, 21))

        self._4pxButton = QPushButton()
        self._4pxButton.setCheckable(True)
        self._4pxButton.setProperty("pixel_size", 4)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icons/ico_4px"), QIcon.Normal, QIcon.Off)

        self._4pxButton.setIcon(icon)
        self._4pxButton.setIconSize(QSize(21, 21))

        self._button_group.addButton(self._1pxButton, 0)
        self._button_group.addButton(self._2pxButton, 1)
        self._button_group.addButton(self._4pxButton, 2)

        self._layout.addWidget(self._1pxButton)
        self._layout.addWidget(self._2pxButton)
        self._layout.addWidget(self._4pxButton)

        self._1pxButton.setChecked(True)

        self.setLayout(self._layout)


    def _onButtonChecked(self):

        pixelSizeChosen = self._button_group.checkedButton().property("pixel_size")
        self.pixelSizeChanged.emit(pixelSizeChosen)