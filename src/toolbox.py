# -------------------------------------------------------------------------------------------------
# Name:        ToolBox
# Purpose:     Represents Canvas Toolbox. Manages Canvas Tools and Inks
#
# Author:      Rafael Vasco
#
# Created:     06/10/13
# Copyright:   (c) Rafael Vasco 2014
# -------------------------------------------------------------------------------------------------

from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QButtonGroup, \
    QStackedWidget, QLabel, \
    QListWidget, QPushButton

from src.resources_cache import ResourcesCache


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

        self._currentEditedInkSlot = None
        self._previousEditedInkSlot = None

        self._editMode = False

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
        self._toolsButtonGroup.buttonClicked.connect(
            self._on_tool_slot_triggered)

        self._inksButtonGroup = QButtonGroup()
        self._inksButtonGroup.setExclusive(False)
        self._inksButtonGroup.buttonClicked.connect(self._on_ink_slot_triggered)

        self.setLayout(self._layout)

        self._toolbarSubPanel = None
        self._toolsListWidget = None
        self._toolsOptionsPanel = None

        self._init_edit_panel()

        self._add_ink_slot(0)
        self._add_ink_slot(1)

        self.resize(0, 50)

    # -------------------------------------------------------------------------

    def get_tool_by_name(self, name):

        return self._registeredTools[name]

    def register_tool(self, tool, is_default=None):

        if tool.name not in self._registeredTools:

            self._registeredTools[tool.name] = tool
            self._toolsListWidget.addItem(tool.name)

            if is_default is True:
                self._toolsListWidget.setCurrentRow(0)

            self._build_tool_options_pane(tool)

            if len(self._toolSlots) < 3:
                slot_index = self._add_tool_slot(is_default)
                self._assign_tool_to_slot(tool, slot_index)

    def register_ink(self, ink, slot):

        if not ink.name in self._registeredInks:
            self._registeredInks[ink.name] = ink

            self._inksListWidget.addItem(ink.name)

            self._build_ink_options_pane(ink)

            if self._inkSlots[slot]['id'] is None:
                self._assign_ink_to_slot(ink, slot)

    def switch_tool_slot(self, slot):

        self._previousActiveToolSlot = self._currentActiveToolSlot

        self._currentActiveToolSlot = slot

        if self._currentActiveToolSlot == self._previousActiveToolSlot:
            return

        tool_name = self._toolSlots[slot]['id']

        self._toolSlots[slot]['button'].setChecked(True)

        self.toolChanged.emit(tool_name)

        self._select_tool_on_list(tool_name)

    # -------------------------------------------------------------------------

    def _go_back_to_last_tool(self):
        self.switch_tool_slot(self._previousActiveToolSlot)

    def _add_tool_slot(self, selected=None):

        slot_button = QPushButton()
        slot_button.setCheckable(True)

        index = len(self._toolSlots)

        if selected is not None and selected is True:
            slot_button.setChecked(True)

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

    def _add_ink_slot(self, slot_number):

        slot_button = QPushButton()
        slot_button.setFont(self.font())
        slot_button.setStyleSheet(
            "border-color: rgb(56,56,56); background-color: rgb(17,17,"
            "17); font-size: 12pt;")

        index = len(self._inkSlots)

        if slot_number == 0:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button1"), QIcon.Normal,
                           QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(QSize(18, 23))

        elif slot_number == 1:

            icon = QIcon()
            icon.addPixmap(QPixmap(":/icons/ico_mouse_button2"), QIcon.Normal,
                           QIcon.Off)

            slot_button.setIcon(icon)
            slot_button.setIconSize(QSize(18, 23))

        slot = {

            'id': None,
            'button': slot_button
        }

        self._inkSlots.append(slot)

        self._inksButtonGroup.addButton(slot_button)

        self._inksButtonGroup.setId(slot_button, index)

        self._inksLayout.addWidget(slot_button)

        return index

    def _assign_tool_to_slot(self, tool, slot):

        if slot < 0 or slot > len(self._toolSlots) - 1:
            raise Exception(
                '[ToolBox] > _assignToolToSlot : invalid slot parameter')

        self._toolSlots[slot]['id'] = tool.name

        icon = tool.icon

        if icon is not None:
            tool_button = self._toolSlots[slot]['button']
            tool_button.setIcon(tool.icon)
            tool_button.setIconSize(QSize(24, 24))

    def _assign_ink_to_slot(self, ink, slot):

        if slot != 0 and slot != 1:
            raise Exception(
                '[ToolBox] > _assignInkToSlot : invalid slot parameter')

        ink_name = ink.name

        self._inkSlots[slot]['id'] = ink_name
        self._inkSlots[slot]['button'].setText(ink_name)

        if slot == 0:
            self.primaryInkChanged.emit(ink_name)
        elif slot == 1:
            self.secondaryInkChanged.emit(ink_name)

    def _init_edit_panel(self):

        self._toolbarSubPanel = QStackedWidget()

        # 1. Initialize Tools Control Panel -----------------------------------

        self._toolsListWidget = QListWidget()

        self._toolsListWidget.currentRowChanged.connect(
            lambda v: self._toolsOptionsPanel.setCurrentIndex(v))

        self._toolsListWidget.setMaximumSize(QSize(150, 200))

        self._toolsListWidget.itemClicked.connect(
            self._on_tool_list_item_clicked)

        # Tools Subpanel ------------------------------------------------------

        tools_control_panel = QWidget()

        tools_control_panel_layout = QHBoxLayout()

        tools_control_panel.setLayout(tools_control_panel_layout)

        tools_control_panel_layout.setAlignment(Qt.AlignLeft)

        # Tools List ----------------------------------------------------------

        tools_list_sublayout = QVBoxLayout()

        tools_list_sublayout.setAlignment(Qt.AlignTop)

        tools_list_sublayout.setContentsMargins(0, 0, 0, 0)

        tools_list_sublayout.addWidget(QLabel("Tools"))

        tools_list_sublayout.addWidget(self._toolsListWidget)

        tools_control_panel_layout.addLayout(tools_list_sublayout)

        # Tools Options -------------------------------------------------------

        tools_options_sublayout = QVBoxLayout()

        tools_options_sublayout.setAlignment(Qt.AlignTop)

        tools_control_panel_layout.addLayout(tools_options_sublayout)

        self._toolsOptionsPanel = QStackedWidget()

        tools_options_sublayout.addWidget(QLabel("Tools Options"))

        tools_options_sublayout.addWidget(self._toolsOptionsPanel)

        self._toolbarSubPanel.addWidget(tools_control_panel)

        # 2. Initialize Inks Control Panel ------------------------------------

        self._inksListWidget = QListWidget()

        self._inksListWidget.currentRowChanged.connect(
            lambda v: self._inksOptionsPanel.setCurrentIndex(v))

        self._inksListWidget.setMaximumSize(QSize(150, 200))

        self._inksListWidget.itemClicked.connect(self._on_ink_list_item_clicked)

        # Inks Subpanel -------------------------------------------------------

        inks_control_panel = QWidget()

        inks_control_panel_layout = QHBoxLayout()

        inks_control_panel.setLayout(inks_control_panel_layout)

        inks_control_panel_layout.setAlignment(Qt.AlignLeft)

        # Inks List -----------------------------------------------------------

        inks_list_sublayout = QVBoxLayout()

        inks_list_sublayout.setAlignment(Qt.AlignTop)

        inks_list_sublayout.setContentsMargins(0, 0, 0, 0)

        inks_list_sublayout.addWidget(QLabel("Inks"))

        inks_list_sublayout.addWidget(self._inksListWidget)

        inks_control_panel_layout.addLayout(inks_list_sublayout)

        # Inks Options --------------------------------------------------------

        inks_options_sublayout = QVBoxLayout()

        inks_options_sublayout.setAlignment(Qt.AlignTop)

        inks_control_panel_layout.addLayout(inks_options_sublayout)

        self._inksOptionsPanel = QStackedWidget()

        inks_options_sublayout.addWidget(QLabel("Inks Options"))

        inks_options_sublayout.addWidget(self._inksOptionsPanel)

        self._toolbarSubPanel.addWidget(inks_control_panel)

        # ---------------------------------------------------------------------

        self._layout.addWidget(self._toolbarSubPanel)

        self._toolbarSubPanel.setVisible(False)

    def _build_tool_options_pane(self, tool):

        pane = QWidget()

        pane_layout = QVBoxLayout()
        pane_layout.setAlignment(Qt.AlignTop)
        pane.setLayout(pane_layout)

        for prop in tool.properties.values():
            field_layout = QHBoxLayout()

            field_layout.addWidget(QLabel(prop.description))

            prop_widget = prop.build_property_widget()

            field_layout.addWidget(prop_widget)

            pane_layout.addLayout(field_layout)

        self._toolsOptionsPanel.addWidget(pane)

    def _build_ink_options_pane(self, ink):

        pane = QWidget()

        pane_layout = QVBoxLayout()
        pane_layout.setAlignment(Qt.AlignTop)
        pane.setLayout(pane_layout)

        for prop in ink.properties.values():
            field_layout = QHBoxLayout()
            field_layout.addWidget(QLabel(prop.description))

            prop_widget = prop.build_property_widget()

            field_layout.addWidget(prop_widget)

            pane_layout.addLayout(field_layout)

        self._inksOptionsPanel.addWidget(pane)

    def _select_tool_on_list(self, tool_name):

        tool_list_item = \
            self._toolsListWidget.findItems(tool_name, Qt.MatchExactly)[0]

        if tool_list_item is not None:
            self._toolsListWidget.setCurrentItem(tool_list_item)

    def _select_ink_on_list(self, ink_name):

        ink_list_item = \
            self._inksListWidget.findItems(ink_name, Qt.MatchExactly)[0]

        if ink_list_item is not None:
            self._inksListWidget.setCurrentItem(ink_list_item)

    # -------------------------------------------------------------------------

    def mousePressEvent(self, e):
        if not self._editMode:
            self._editMode = True
            self.resize(self.width(), 300)
            self._toolbarSubPanel.setVisible(True)

        else:
            self._editMode = False
            self.resize(self.width(), 50)
            self._toolbarSubPanel.setVisible(False)

            if self._currentEditedInkSlot is not None:
                self._inksButtonGroup.button(self._currentEditedInkSlot).\
                    setStyleSheet("border-color: rgb(56,56,56);")
                self._currentEditedInkSlot = None
                self._previousEditedInkSlot = None
                self._inksListWidget.setCurrentRow(0)
                self._toolbarSubPanel.setCurrentIndex(0)

        self.update()

        e.accept()

    def wheelEvent(self, e):

        e.accept()

    def enterEvent(self, e):

        self.mouseEntered.emit()
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, e):

        self.mouseLeft.emit()

    def _on_tool_slot_triggered(self):

        self._toolbarSubPanel.setCurrentIndex(0)

        triggered_slot = self._toolsButtonGroup.checkedId()

        self.switch_tool_slot(triggered_slot)

        self.update()

    def _on_ink_slot_triggered(self, slot_button):

        if not self._editMode:
            return

        triggered_slot_id = self._inksButtonGroup.id(slot_button)

        self._previousEditedInkSlot = self._currentEditedInkSlot

        self._currentEditedInkSlot = triggered_slot_id

        if self._previousEditedInkSlot is not None:
            self._inksButtonGroup.\
                button(self._previousEditedInkSlot).\
                setStyleSheet("border-color: rgb(56,56,56);")

        slot_button.setStyleSheet("border-color: rgb(255,0,0);")

        self._toolbarSubPanel.setCurrentIndex(1)

        ink_name = self._inkSlots[triggered_slot_id]['id']

        self._select_ink_on_list(ink_name)

        if triggered_slot_id == 0:
            self.primaryInkChanged.emit(ink_name)
        elif triggered_slot_id == 1:
            self.secondaryInkChanged.emit(ink_name)

    def _on_tool_list_item_clicked(self, new_item):

        new_item_name = new_item.text()
        self._assign_tool_to_slot(self.get_tool_by_name(new_item_name),
                                  self._currentActiveToolSlot)
        self.toolChanged.emit(new_item_name)
        self._toolbarSubPanel.update()

    def _on_ink_list_item_clicked(self, item):

        item_name = item.text()

        ink = self._registeredInks[item_name]

        if ink is not None:
            self._assign_ink_to_slot(ink, self._currentEditedInkSlot)