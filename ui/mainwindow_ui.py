# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Sep  8 12:04:27 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1024, 768)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 768))
        MainWindow.setStyleSheet(_fromUtf8("/*CUSTOM /////////////////////////////////////////////////////////////////////////////////////////////////*/\n"
"\n"
"QFrame#mainPanel\n"
"{\n"
"    background-color: #121417;\n"
"}\n"
"\n"
"/*THEME ////////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ----TOOLTIP------------------------------------------------------------------------------------------- */\n"
"\n"
"\n"
"*\n"
"{\n"
"    color: #ddd;\n"
"    \n"
"    \n"
"}\n"
"\n"
"QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background: #378CBE;\n"
"     opacity: 70;\n"
"}\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ------- WIDGET --------------------------------------------------------------------------------------- */\n"
"\n"
"\n"
"\n"
"/* BG */\n"
"\n"
"QWidget\n"
"{\n"
"    background: #222;\n"
"}\n"
"\n"
"QWidget#QTabWidget::pane\n"
"{\n"
"    background: red;\n"
"}\n"
"\n"
"/* Menubar -> Menu BG */\n"
"QWidget:disabled  \n"
"{\n"
"    \n"
"   background: #111;\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background: #1E1F21;\n"
"}\n"
"\n"
"\n"
"/* Menubar -> Item BG */\n"
"QWidget:item:selected\n"
"{\n"
"    background: #111;\n"
"}\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"\n"
"QFrame\n"
"{\n"
"    background: #111;\n"
"}\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ------ BUTTON --------------------------------------------------------------------------------------- */\n"
"\n"
"QPushButton\n"
"{\n"
"    \n"
"    background: #222;\n"
"    border: 1px solid #333;\n"
"    font-size: 10px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 5px;\n"
"    padding-bottom: 5px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background: #333;\n"
"    border: 1px solid #444;\n"
"    color: #6ED6FF;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background: #222;\n"
"    border: 1px solid #111;\n"
"    color: #4AA9CF;\n"
"}\n"
"\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    \n"
"    background: #2D3339;\n"
"    border: 1px solid black;\n"
"}\n"
"\n"
"QAbstractScrollArea\n"
"{\n"
"    background: #222;\n"
"    border: 1px solid #333;\n"
"    padding: 1px;\n"
"}\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* --- WINDOW ------------------------------------------------------------------------------------------- */\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"\n"
"/* ---- MENU -------------------------------------------------------------------------------------------- */\n"
"/* -------------------------------------------------------------------------------------------------------*/\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    background: #1D232D;\n"
"    border: 1px solid #333D4F;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    margin: 0;\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"}\n"
"\n"
"\n"
"QMenuBar\n"
"{\n"
"    padding: 0;\n"
"    background: #222;\n"
"    \n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #378CBE;\n"
"}\n"
"\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ---- TOOLBAR ----------------------------------------------------------------------------------------- */\n"
"\n"
"QToolBar\n"
"{\n"
"     background: #333;\n"
"     border-bottom: 1px solid #444;\n"
"}\n"
"\n"
"QToolBar > QWidget\n"
"{\n"
"    background: transparent;\n"
"    border: none;\n"
"    \n"
"    \n"
"}\n"
"\n"
"QToolBar > QWidget:hover\n"
"{\n"
"    color: #6ED6FF;\n"
"}\n"
"\n"
"QToolBar > QWidget:pressed\n"
"{\n"
"    color: #4AA9CF;\n"
"}\n"
"\n"
"/* -------------------------------------------------------------------------------------------------------*/\n"
"/* ---SCROLL AREA ----------------------------------------------------------------------------------------*/\n"
"\n"
"\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* --- SCROLL BAR --------------------------------------------------------------------------------------- */\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid black;\n"
"     background: #202123;\n"
"     height: 8px;\n"
"     margin: 0px 16px 0 16px;\n"
"    \n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: #2E2F33;\n"
"      border: 1px solid black;\n"
"      min-height: 20px;\n"
"\n"
"      \n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:pressed\n"
"{\n"
"    background: #378CBE;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid black;\n"
"      background: #2E2F33;\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid black;\n"
"      background: #2E2F33;\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 10px;\n"
"      height: 10px;\n"
"      background: #378CBE;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal:pressed, QScrollBar::left-arrow:horizontal:pressed\n"
"{\n"
"      background: #4BA4D8;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      background: #202123;;\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      \n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: #2E2F33;\n"
"      border: 1px solid black;\n"
"      min-height: 20px;\n"
"     \n"
"}\n"
"\n"
"QScrollBar::handle:vertical:pressed\n"
"{\n"
"      background: #378CBE;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      background: #2E2F33;\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"     border: 1px solid black;\n"
"      background: #2E2F33;\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 10px;\n"
"      height: 10px;\n"
"      background: #378CBE;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical:pressed, QScrollBar::down-arrow:vertical:pressed\n"
"{\n"
"      background: #4BA4D8;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical:pressed, QScrollBar::sub-page:vertical:pressed\n"
"{\n"
"      background: #4BA4D8;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* --- CHECK BOX ----------------------------------------------------------------------------------------- */\n"
"\n"
"QCheckBox\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QCheckBox:hover\n"
"{\n"
"    color: #6ED6FF;\n"
"}\n"
"\n"
" QCheckBox::indicator {\n"
"   \n"
"     width: 15px;\n"
"     height: 15px;\n"
"     background: #111;\n"
"     border: 1px solid #222;\n"
"  \n"
" }\n"
"\n"
"\n"
" QCheckBox::indicator:checked {\n"
"    \n"
"     \n"
"     background: #6ED6FF;\n"
" }\n"
"\n"
" QCheckBox::indicator:checked:hover {\n"
" \n"
"     background: #6ED6FF;\n"
" \n"
" }\n"
"\n"
" QCheckBox::indicator:checked:pressed {\n"
" \n"
"     background: #6ED6FF;\n"
" }\n"
"\n"
" QCheckBox::indicator:indeterminate {\n"
" \n"
"     background: #6ED6FF;\n"
" \n"
" }\n"
"\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* ----------------- RADIO BUTTON ----------------------------------------------------------------------- */\n"
"\n"
"QRadioButton\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QRadioButton:hover\n"
"{\n"
"    color: #6ED6FF;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"     width: 15px;\n"
"     height: 15px;\n"
"     background: #111;\n"
"     border: 1px solid #222;\n"
" }\n"
"\n"
"QRadioButton::indicator:hover\n"
"{\n"
"    background: #1F1F1F;\n"
"    border: 1px solid #2D2D2D;\n"
"}\n"
"\n"
" QRadioButton::indicator::checked {\n"
"     \n"
"     background: #6ED6FF;\n"
" }\n"
"\n"
" QRadioButton::indicator:checked:hover {\n"
"     \n"
"     background: #6ED6FF;\n"
" }\n"
"\n"
" QRadioButton::indicator:checked:pressed {\n"
" \n"
"    background: #6ED6FF;\n"
" }\n"
"\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* --- COMBO BOX --------------------------------------------------------------------------------------- */\n"
" \n"
"QComboBox\n"
"{\n"
"    background: #111;\n"
"      border: 1px solid #222;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    background: #1F1F1F;\n"
"      border: 1px solid 2D2D2D;\n"
"    selection-background-color: #378CBE;\n"
"    \n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"      border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     background: #6ED6FF;\n"
"    border: 1px solid #9CE3FF;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox::down-arrow:on\n"
"{\n"
"    background: #4AA9CF;\n"
"}\n"
"\n"
"/* ------------------------------------------------------------------------------------------------------ */\n"
"/* --- TEXT EDIT----------------------------------------------------------------------------------------- */\n"
"\n"
"QTextEdit\n"
"{\n"
"    background: #111;\n"
"    border: 1px solid #222;\n"
"    selection-background-color: #378CBE;\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 1px solid #378CBE;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background: #111;\n"
"    border: 1px solid #222;\n"
"    selection-background-color: #378CBE;\n"
"}\n"
"\n"
"QPlainTextEdit:focus\n"
"{\n"
"    border: 1px solid #378CBE;\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background: #111;\n"
"    border: 1px solid #222;\n"
"    selection-background-color: #378CBE;\n"
"}\n"
"\n"
"QLineEdit:focus\n"
"{\n"
"    border: 1px solid #378CBE;\n"
"}\n"
"\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* -----GROUP BOX------------------------------------------------------------------------------------- */\n"
"\n"
"QGroupBox\n"
"{\n"
"    background: #222;\n"
"    border: 1px solid #333;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"\n"
" QGroupBox::title {\n"
"\n"
"     subcontrol-origin: margin;\n"
"     subcontrol-position: top center; \n"
"     padding: 5px;\n"
"     background: #333;\n"
"     border: 1px solid #444;\n"
" }\n"
"\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* ----HEADER ---------------------------------------------------------------------------------------- */\n"
"\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* ---- DOCK ----------------------------------------------------------------------------------------- */\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: #333;\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: #555;\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #ddd;\n"
"}\n"
"\n"
"\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* -------- PROGRESS BAR ----------------------------------------------------------------------------- */\n"
"QProgressBar\n"
"{\n"
"    background: #202123;\n"
"    border: 1px solid black;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #378CBE;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* ------- TAB BAR ----------------------------------------------------------------------------------- */\n"
"\n"
"QTabWidget::pane {\n"
"    \n"
"\n"
"    border: 1px solid #333;   \n"
"\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"     left: 5px; /* move to the right by 5px */\n"
" }\n"
"\n"
"\n"
"QTabBar::tab {\n"
"    background: #222;\n"
"       border-right: 1px solid #333;    \n"
"    border-left: 1px solid #333;\n"
"    border-top: 1px solid #333;    \n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    min-width: 8ex;\n"
"    padding-top: 6px;\n"
"    padding-bottom: 6px;\n"
"    margin-right: -3px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
"     margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #aaa;\n"
"    \n"
"    \n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    margin-bottom: 0px;\n"
"    background: #333;\n"
"    border: 1px solid #444;\n"
"    color: #6ED6FF;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    padding-bottom: 3px;\n"
"    \n"
"}\n"
"\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"/* --------------------------------------------------------------------------------------------------- */\n"
"\n"
"QAbstractSpinBox\n"
"{\n"
"    padding-right: 15px; /* make room for the arrows */\n"
"    background: #202123;\n"
"    border: 1px solid black;\n"
"    selection-background-color: #378CBE;\n"
"}\n"
"\n"
"QAbstractSpinBox::up-button {\n"
"     subcontrol-origin: border;\n"
"     subcontrol-position: top right; /* position at the top right corner */\n"
"\n"
"     width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
"     background: #2E2F33;\n"
"     border: 1px solid black;\n"
" }\n"
"\n"
"\n"
"\n"
" QAbstractSpinBox::up-button:pressed\n"
" {\n"
"     background: #378CBE;\n"
" }\n"
"\n"
"\n"
" QAbstractSpinBox::down-button\n"
" {\n"
"     subcontrol-origin: border;\n"
"     subcontrol-position: bottom right; /* position at bottom right corner */\n"
"\n"
"     width: 16px;\n"
"     background: #2E2F33;\n"
"     border: 1px solid black;\n"
"     \n"
" }\n"
"\n"
"\n"
"\n"
" QAbstractSpinBox::down-button:pressed\n"
" {\n"
"     background: #378CBE;\n"
" }\n"
"\n"
"\n"
"\n"
"QSlider::handle:horizontal, QSlider::handle:vertical {\n"
"    \n"
"     background: #2E2F33;\n"
"     border: 1px solid black; \n"
"}\n"
"\n"
"QSlider::add-page:horizontal, QSlider::add-page:vertical\n"
" {\n"
"     background: #202123;\n"
"     border: 1px solid black; \n"
"}\n"
"\n"
" QSlider::sub-page:horizontal, QSlider::sub-page:vertical {\n"
"     background: #378CBE;\n"
"     border: 1px solid black;\n"
" }\n"
""))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.topDownSplitter = QtGui.QSplitter(self.centralwidget)
        self.topDownSplitter.setOrientation(QtCore.Qt.Vertical)
        self.topDownSplitter.setObjectName(_fromUtf8("topDownSplitter"))
        self.leftRightSplitter = QtGui.QSplitter(self.topDownSplitter)
        self.leftRightSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.leftRightSplitter.setObjectName(_fromUtf8("leftRightSplitter"))
        self.leftPanel = QtGui.QFrame(self.leftRightSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftPanel.sizePolicy().hasHeightForWidth())
        self.leftPanel.setSizePolicy(sizePolicy)
        self.leftPanel.setMinimumSize(QtCore.QSize(240, 400))
        self.leftPanel.setMaximumSize(QtCore.QSize(240, 16777215))
        self.leftPanel.setStyleSheet(_fromUtf8(""))
        self.leftPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.leftPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.leftPanel.setObjectName(_fromUtf8("leftPanel"))
        self.mainPanel = QtGui.QFrame(self.leftRightSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainPanel.sizePolicy().hasHeightForWidth())
        self.mainPanel.setSizePolicy(sizePolicy)
        self.mainPanel.setMinimumSize(QtCore.QSize(320, 240))
        self.mainPanel.setAutoFillBackground(False)
        self.mainPanel.setStyleSheet(_fromUtf8(""))
        self.mainPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.mainPanel.setObjectName(_fromUtf8("mainPanel"))
        self.rightPanel = QtGui.QFrame(self.leftRightSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightPanel.sizePolicy().hasHeightForWidth())
        self.rightPanel.setSizePolicy(sizePolicy)
        self.rightPanel.setMinimumSize(QtCore.QSize(200, 550))
        self.rightPanel.setMaximumSize(QtCore.QSize(450, 16777215))
        self.rightPanel.setStyleSheet(_fromUtf8(""))
        self.rightPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rightPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.rightPanel.setObjectName(_fromUtf8("rightPanel"))
        self.bottomPanel = QtGui.QFrame(self.topDownSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottomPanel.sizePolicy().hasHeightForWidth())
        self.bottomPanel.setSizePolicy(sizePolicy)
        self.bottomPanel.setMinimumSize(QtCore.QSize(0, 80))
        self.bottomPanel.setMaximumSize(QtCore.QSize(16777215, 100))
        self.bottomPanel.setStyleSheet(_fromUtf8(""))
        self.bottomPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottomPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.bottomPanel.setObjectName(_fromUtf8("bottomPanel"))
        self.horizontalLayout.addWidget(self.topDownSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.NoAntialias)
        self.actionNew.setFont(font)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionQuit = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionQuit.setFont(font)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionOpen = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionOpen.setFont(font)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionSave.setFont(font)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionSaveAs.setFont(font)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionClose = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionClose.setFont(font)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionExport = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionExport.setFont(font)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionImport = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Nokia Cellphone FC"))
        font.setPointSize(12)
        self.actionImport.setFont(font)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionClose)
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "SpriteMator", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionNew.setIconText(_translate("MainWindow", "New", None))
        self.actionNew.setToolTip(_translate("MainWindow", "New Sprite", None))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setToolTip(_translate("MainWindow", "Close Application", None))
        self.actionQuit.setShortcut(_translate("MainWindow", "Esc", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open Sprite", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave.setToolTip(_translate("MainWindow", "Save Sprite", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs", None))
        self.actionSaveAs.setToolTip(_translate("MainWindow", "Save Sprite with another name", None))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionClose.setToolTip(_translate("MainWindow", "Close Sprite", None))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionExport.setText(_translate("MainWindow", "Export", None))
        self.actionExport.setToolTip(_translate("MainWindow", "Export Sprite animations : Either as separate images or as a spritesheet", None))
        self.actionExport.setShortcut(_translate("MainWindow", "Ctrl+E", None))
        self.actionImport.setText(_translate("MainWindow", "Import", None))
        self.actionImport.setToolTip(_translate("MainWindow", "Create a Sprite from one or more images", None))
        self.actionImport.setShortcut(_translate("MainWindow", "Ctrl+I", None))

from . import resources_rc
