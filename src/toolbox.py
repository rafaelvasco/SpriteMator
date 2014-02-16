#-----------------------------------------------------------------------------------------------------------------------
# Name:        ToolBox
# Purpose:     Represents Canvas Toolbox. Manages Canvas Tools and Inks
#
# Author:      Rafael Vasco
#
# Created:     06/10/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QButtonGroup, QMenu

from src.resources_cache import ResourcesCache
from src.widgets import Button


class ToolBox(QWidget):
    mouseEntered = pyqtSignal()
    mouseLeft = pyqtSignal()

    toolChanged = pyqtSignal(str)
    primaryInkChanged = pyqtSignal(str)
    secondaryInkChanged = pyqtSignal(str)

    def __init__(self, canvas):

        super(ToolBox, self).__init__(canvas)

        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.setFont(ResourcesCache.get("BigFont"))

        self._registeredTools = []
        self._registeredInks = []

        self._freeToolsIds = []

        self._toolSlots = []
        self._inkSlots = []

        self._backgroundColor = QColor(40, 40, 40)
        self._toolLabelColor = QColor(112, 231, 255)

        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignCenter)
        self._layout.setContentsMargins(4, 4, 4, 4)

        self._toolsLayout = QHBoxLayout()
        self._inksLayout = QHBoxLayout()

        self._toolsLayout.setContentsMargins(0, 0, 0, 0)
        self._toolsLayout.setAlignment(Qt.AlignLeft)

        self._inksLayout.setContentsMargins(0, 0, 0, 0)
        self._inksLayout.setAlignment(Qt.AlignLeft)

        self._layout.addLayout(self._toolsLayout)
        self._layout.addLayout(self._inksLayout)

        self._toolsButtonGroup = QButtonGroup()

        self._toolsMenu = QMenu()

        self._toolsMenu.addAction("Test1")
        self._toolsMenu.addAction("Test2")

        self.setLayout(self._layout)

        self._create_ink_slot(0)
        self._create_ink_slot(1)

        self.resize(0, 50)

    def register_tool(self, tool, is_default=None):

        if tool.name() not in self._registeredTools:

            slot_index = self._create_tool_slot(is_default)

            self._registeredTools.append(tool.name())

            if len(self._toolSlots) < 5:

                self._assign_tool_to_slot(tool, slot_index)

            else:

                self._freeToolsIds.append(tool.name())

    def register_ink(self, ink, slot=None):

        if not ink.name() in self._registeredInks:

            self._registeredInks.append(ink.name())

            if slot is not None:

                if slot == 0 or slot == 1:
                    self._assign_ink_to_slot(ink, slot)

    def select_tool_slot(self, slot):

        self._toolSlots[slot]['button'].setChecked(True)
        self.toolChanged.emit(self._toolSlots[slot]['id'])

    def _create_tool_slot(self, selected=None):

        slot_button = Button()
        slot_button.setCheckable(True)

        index = len(self._toolSlots)

        if selected is not None and selected is True:
            slot_button.setChecked(True)

        slot_button.activated.connect(self._tool_slot_triggered)

        self._toolSlots.append({'button': slot_button})

        self._toolsButtonGroup.addButton(slot_button, index)

        self._toolsLayout.addWidget(slot_button)

        return index

    def _create_ink_slot(self, slot_number):

        slot_button = Button()
        slot_button.setFont(self.font())
        slot_button.setStyleSheet("border-color: rgb(56,56,56); background-color: rgb(17,17,17); font-size: 12pt;")

        index = len(self._inkSlots)

        if slot_number == 0:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button1"), QIcon.Normal, QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(18, 23)

        elif slot_number == 1:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button2"), QIcon.Normal, QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(18, 23)

        self._inkSlots.append({'button': slot_button})

        self._inksLayout.addWidget(slot_button)

        return index

    def _assign_tool_to_slot(self, tool, slot):

        if slot < 0 or slot > len(self._toolSlots) - 1:
            raise Exception('[ToolBox] > _assignToolToSlot : invalid slot parameter')

        self._toolSlots[slot]['id'] = tool.name()

        icon = tool.icon()

        if icon is not None:

            tool_button = self._toolSlots[slot]['button']
            tool_button.setIcon(tool.icon())
            tool_button.set_tooltip(tool.name())

    def _assign_ink_to_slot(self, ink, slot):

        if slot != 0 and slot != 1:
            raise Exception('[ToolBox] > _assignInkToSlot : invalid slot parameter')

        label = ink.name()
        self._inkSlots[slot]['id'] = label

        self._inkSlots[slot]['button'].setText(label)

    ####### EVENTS ###################################################################

    def mousePressEvent(self, e):

        e.accept()

    def wheelEvent(self, e):

        e.accept()

    def enterEvent(self, e):

        self.mouseEntered.emit()
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, e):

        self.mouseLeft.emit()

    def paintEvent(self, e):

        p = QPainter(self)

        rect = e.rect()

        p.setPen(self._backgroundColor.lighter())
        p.drawRect(rect.adjusted(0, 0, -1, -1))

        p.fillRect(rect.adjusted(1, 1, -1, -1), self._backgroundColor)

    def _tool_slot_triggered(self):

        triggered_slot = self._toolsButtonGroup.checkedId()

        self.toolChanged.emit(self._toolSlots[triggered_slot]['id'])

        ##################################################################################
