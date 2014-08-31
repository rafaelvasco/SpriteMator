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

from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QButtonGroup, QStackedWidget, QLabel, \
    QListWidget

from src.resources_cache import ResourcesCache
from src.widgets import Button


class ToolBox(QWidget):
    mouseEntered = pyqtSignal()
    mouseLeft = pyqtSignal()

    toolChanged = pyqtSignal(str)
    primaryInkChanged = pyqtSignal(str)
    secondaryInkChanged = pyqtSignal(str)

    def __init__(self):

        super(ToolBox, self).__init__()

        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.setFont(ResourcesCache.get("BigFont"))

        self._registeredTools = {}
        self._registeredInks = {}

        self._toolSlots = []
        self._inkSlots = []

        self._currentActiveToolSlot = None
        self._previousActiveToolSlot = None

        self._subPanelExpanded = False

        self._backgroundColor = QColor(40, 40, 40)
        self._toolLabelColor = QColor(112, 231, 255)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.setContentsMargins(4, 4, 4, 4)

        top_layout = QHBoxLayout()

        self._layout.addLayout(top_layout)

        self._toolsLayout = QHBoxLayout()
        self._inksLayout = QHBoxLayout()

        self._toolsLayout.setContentsMargins(0, 0, 0, 0)
        self._toolsLayout.setAlignment(Qt.AlignLeft)

        self._inksLayout.setContentsMargins(0, 0, 0, 0)
        self._inksLayout.setAlignment(Qt.AlignRight)

        top_layout.addLayout(self._toolsLayout)
        top_layout.addLayout(self._inksLayout)

        self._toolsButtonGroup = QButtonGroup()

        self.setLayout(self._layout)

        self._toolbarSubPanel = None
        self._toolsListWidget = None
        self._toolsOptionsPanel = None

        self._initSubPanel()

        self._addInkSlot(0)
        self._addInkSlot(1)

        self.resize(0, 50)

    def getToolByName(self, name):

        return self._registeredTools[name]

    def _goBackToLastTool(self):
        self.switchToolSlot(self._previousActiveToolSlot)

    def registerTool(self, tool, is_default=None):

        if tool.name not in self._registeredTools:

            slot_index = self._addToolSlot(is_default)

            self._registeredTools[tool.name] = tool
            self._toolsListWidget.addItem(tool.name)

            if is_default is True:
                self._toolsListWidget.setCurrentRow(0)

            self._buildToolsOptionsPane(tool)

            if len(self._toolSlots) < 5:
                self._assignToolToSlot(tool, slot_index)

    def registerInk(self, ink, slot):

        if not ink.name in self._registeredInks:
            self._registeredInks[ink.name] = ink
            self._assignInkToSlot(ink, slot)

    def switchToolSlot(self, slot):

        self._previousActiveToolSlot = self._currentActiveToolSlot

        self._currentActiveToolSlot = slot

        tool_name = self._toolSlots[slot]['id']

        self._toolSlots[slot]['button'].setChecked(True)

        self.toolChanged.emit(tool_name)

        correspondent_tool_list_item = self._toolsListWidget.findItems(tool_name, Qt.MatchExactly)[0]

        if correspondent_tool_list_item is not None:
            self._toolsListWidget.setCurrentItem(correspondent_tool_list_item)

    def _addToolSlot(self, selected=None):

        slot_button = Button()
        slot_button.setCheckable(True)

        index = len(self._toolSlots)

        if selected is not None and selected is True:
            slot_button.setChecked(True)

        slot_button.activated.connect(self._tool_slot_triggered)

        slot = {

            'id': None,
            'button': slot_button
        }

        if selected:
            self._currentActiveToolSlot = index

        self._toolSlots.append(slot)

        self._toolsButtonGroup.addButton(slot_button, index)

        self._toolsLayout.addWidget(slot_button)

        return index

    def _addInkSlot(self, slot_number):

        slot_button = Button()
        slot_button.setFont(self.font())
        slot_button.setStyleSheet("border-color: rgb(56,56,56); background-color: rgb(17,17,17); font-size: 12pt;")
        slot_button.clicked.connect(self._ink_slot_clicked)

        index = len(self._inkSlots)

        if slot_number == 0:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button1"), QIcon.Normal, QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(QSize(18, 23))

        elif slot_number == 1:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button2"), QIcon.Normal, QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(QSize(18, 23))

        slot = {

            id: None,
            'button': slot_button
        }

        self._inkSlots.append(slot)

        self._inksLayout.addWidget(slot_button)

        return index

    def _assignToolToSlot(self, tool, slot):

        if slot < 0 or slot > len(self._toolSlots) - 1:
            raise Exception('[ToolBox] > _assignToolToSlot : invalid slot parameter')

        self._toolSlots[slot]['id'] = tool.name

        icon = tool.icon

        if icon is not None:
            tool_button = self._toolSlots[slot]['button']
            tool_button.setIcon(tool.icon)
            tool_button.setTooltip(tool.name)

    def _assignInkToSlot(self, ink, slot):

        if slot != 0 and slot != 1:
            raise Exception('[ToolBox] > _assignInkToSlot : invalid slot parameter')

        ink_name = ink.name
        self._inkSlots[slot]['id'] = ink_name
        self._inkSlots[slot]['button'].setText(ink_name)

    def _initSubPanel(self):

        self._toolbarSubPanel = QStackedWidget()

        # 1. Initialize Tools Control Panel

        self._toolsListWidget = QListWidget()

        self._toolsListWidget.currentRowChanged.connect(lambda v: self._toolsOptionsPanel.setCurrentIndex(v))

        self._toolsListWidget.setMaximumSize(QSize(150, 200))

        self._toolsListWidget.itemClicked.connect(self._tool_list_item_clicked)

        # Tools Subpanel

        tools_control_panel = QWidget()

        tools_control_panel_layout = QHBoxLayout()

        tools_control_panel.setLayout(tools_control_panel_layout)

        tools_control_panel_layout.setAlignment(Qt.AlignLeft)

        # Tools List

        tools_list_sublayout = QVBoxLayout()

        tools_list_sublayout.setAlignment(Qt.AlignTop)

        tools_list_sublayout.setContentsMargins(0, 0, 0, 0)

        tools_list_sublayout.addWidget(QLabel("Tools"))

        tools_list_sublayout.addWidget(self._toolsListWidget)

        tools_control_panel_layout.addLayout(tools_list_sublayout)

        # Tools Options

        tools_options_sublayout = QVBoxLayout()

        tools_options_sublayout.setAlignment(Qt.AlignTop)

        tools_control_panel_layout.addLayout(tools_options_sublayout)

        self._toolsOptionsPanel = QStackedWidget()

        tools_options_sublayout.addWidget(QLabel("Tools Options"))

        tools_options_sublayout.addWidget(self._toolsOptionsPanel)

        self._toolbarSubPanel.addWidget(tools_control_panel)

        self._layout.addWidget(self._toolbarSubPanel)

        self._toolbarSubPanel.setVisible(False)

    def _buildToolsOptionsPane(self, tool):

        pane = QWidget()

        pane_layout = QVBoxLayout()
        pane_layout.setAlignment(Qt.AlignTop)
        pane.setLayout(pane_layout)

        for prop in tool.properties.values():
            field_layout = QHBoxLayout()

            field_layout.addWidget(QLabel(prop.description))

            prop_widget = prop.buildPropertyWidget()

            field_layout.addWidget(prop_widget)

            pane_layout.addLayout(field_layout)

        self._toolsOptionsPanel.addWidget(pane)

    def mousePressEvent(self, e):
        if not self._subPanelExpanded:
            self._subPanelExpanded = True
            self.resize(self.width(), 300)
            self._toolbarSubPanel.setVisible(True)

        else:
            self._subPanelExpanded = False
            self.resize(self.width(), 50)
            self._toolbarSubPanel.setVisible(False)

        self.update()

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

        if self._currentActiveToolSlot == self._previousActiveToolSlot:
            return

        self.switchToolSlot(triggered_slot)

        self.update()

    def _tool_list_item_clicked(self, new_item):

        new_item_name = new_item.text()
        self._assignToolToSlot(self.getToolByName(new_item_name), self._currentActiveToolSlot)
        self.toolChanged.emit(new_item_name)

    def _ink_slot_clicked(self):

        pass