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

    def __init__(self, canvas):

        super(ToolBox, self).__init__(canvas)

        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.setFont(ResourcesCache.get("BigFont"))

        self._registered_tools = {}
        self._registered_inks = {}

        self._tool_slots = []
        self._ink_slots = []

        self._current_active_toolslot = None
        self._last_active_toolslot = None

        self._subpanel_expanded = False

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

        self._toolbar_sub_panel = None
        self._tools_list_widget = None
        self._tools_options_panel = None

        self._initialize_subpanel()

        self._add_ink_slot(0)
        self._add_ink_slot(1)

        self.resize(0, 50)

    def get_tool_by_name(self, name):

        return self._registered_tools[name]

    def go_back_to_last_tool(self):
        self.switch_tool_slot(self._last_active_toolslot)

    def register_tool(self, tool, is_default=None):

        if tool.name() not in self._registered_tools:

            slot_index = self._add_tool_slot(is_default)

            self._registered_tools[tool.name()] = tool
            self._tools_list_widget.addItem(tool.name())

            if is_default is True:
                self._tools_list_widget.setCurrentRow(0)

            self._build_tool_options_pane(tool)

            if len(self._tool_slots) < 5:
                self._assign_tool_to_slot(tool, slot_index)

    def register_ink(self, ink, slot):

        if not ink.name() in self._registered_inks:
            self._registered_inks[ink.name()] = ink
            self._assign_ink_to_slot(ink, slot)

    def switch_tool_slot(self, slot):

        self._last_active_toolslot = self._current_active_toolslot

        self._current_active_toolslot = slot

        tool_name = self._tool_slots[slot]['id']

        self._tool_slots[slot]['button'].setChecked(True)

        self.toolChanged.emit(tool_name)

        correspondend_tool_list_item = self._tools_list_widget.findItems(tool_name, Qt.MatchExactly)[0]

        if correspondend_tool_list_item is not None:
            self._tools_list_widget.setCurrentItem(correspondend_tool_list_item)

    def _add_tool_slot(self, selected=None):

        slot_button = Button()
        slot_button.setCheckable(True)

        index = len(self._tool_slots)

        if selected is not None and selected is True:
            slot_button.setChecked(True)

        slot_button.activated.connect(self._tool_slot_triggered)

        slot = {

            'id': None,
            'button': slot_button
        }

        if selected:
            self._current_active_toolslot = index

        self._tool_slots.append(slot)

        self._toolsButtonGroup.addButton(slot_button, index)

        self._toolsLayout.addWidget(slot_button)

        return index

    def _add_ink_slot(self, slot_number):

        slot_button = Button()
        slot_button.setFont(self.font())
        slot_button.setStyleSheet("border-color: rgb(56,56,56); background-color: rgb(17,17,17); font-size: 12pt;")
        slot_button.clicked.connect(self._ink_slot_clicked)

        index = len(self._ink_slots)

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

        self._ink_slots.append(slot)

        self._inksLayout.addWidget(slot_button)

        return index

    def _assign_tool_to_slot(self, tool, slot):

        if slot < 0 or slot > len(self._tool_slots) - 1:
            raise Exception('[ToolBox] > _assignToolToSlot : invalid slot parameter')

        self._tool_slots[slot]['id'] = tool.name()

        icon = tool.icon()

        if icon is not None:
            tool_button = self._tool_slots[slot]['button']
            tool_button.setIcon(tool.icon())
            tool_button.setTooltip(tool.name())

    def _assign_ink_to_slot(self, ink, slot):

        if slot != 0 and slot != 1:
            raise Exception('[ToolBox] > _assignInkToSlot : invalid slot parameter')

        ink_name = ink.name()
        self._ink_slots[slot]['id'] = ink_name
        self._ink_slots[slot]['button'].setText(ink_name)

    def _initialize_subpanel(self):

        self._toolbar_sub_panel = QStackedWidget()

        # 1. Initialize Tools Control Panel

        self._tools_list_widget = QListWidget()

        self._tools_list_widget.currentRowChanged.connect(lambda v: self._tools_options_panel.setCurrentIndex(v))

        self._tools_list_widget.setMaximumSize(QSize(150, 200))

        self._tools_list_widget.itemClicked.connect(self._tool_list_item_clicked)

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

        tools_list_sublayout.addWidget(self._tools_list_widget)

        tools_control_panel_layout.addLayout(tools_list_sublayout)

        # Tools Options

        tools_options_sublayout = QVBoxLayout()

        tools_options_sublayout.setAlignment(Qt.AlignTop)

        tools_control_panel_layout.addLayout(tools_options_sublayout)

        self._tools_options_panel = QStackedWidget()

        tools_options_sublayout.addWidget(QLabel("Tools Options"))

        tools_options_sublayout.addWidget(self._tools_options_panel)

        self._toolbar_sub_panel.addWidget(tools_control_panel)

        self._layout.addWidget(self._toolbar_sub_panel)

        self._toolbar_sub_panel.setVisible(False)

    def _build_tool_options_pane(self, tool):

        pane = QWidget()

        pane_layout = QVBoxLayout()
        pane_layout.setAlignment(Qt.AlignTop)
        pane.setLayout(pane_layout)

        for prop in tool.properties().values():
            field_layout = QHBoxLayout()

            field_layout.addWidget(QLabel(prop.description()))

            prop_widget = prop.buildPropertyWidget()

            field_layout.addWidget(prop_widget)

            pane_layout.addLayout(field_layout)

        self._tools_options_panel.addWidget(pane)

    def mousePressEvent(self, e):
        if not self._subpanel_expanded:
            self._subpanel_expanded = True
            self.resize(self.width(), 300)
            self._toolbar_sub_panel.setVisible(True)

        else:
            self._subpanel_expanded = False
            self.resize(self.width(), 50)
            self._toolbar_sub_panel.setVisible(False)

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

        if self._current_active_toolslot == self._last_active_toolslot:
            return

        self.switch_tool_slot(triggered_slot)

        self.update()

    def _tool_list_item_clicked(self, new_item):

        new_item_name = new_item.text()
        self._assign_tool_to_slot(self.get_tool_by_name(new_item_name), self._current_active_toolslot)
        self.toolChanged.emit(new_item_name)

    def _ink_slot_clicked(self):

        pass