# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Jan 25 15:23:22 2014
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
        MainWindow.setStyleSheet(_fromUtf8(""))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.topDownSplitter = QtGui.QSplitter(self.centralwidget)
        self.topDownSplitter.setOrientation(QtCore.Qt.Vertical)
        self.topDownSplitter.setOpaqueResize(True)
        self.topDownSplitter.setHandleWidth(5)
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
        self.leftPanel.setMinimumSize(QtCore.QSize(245, 550))
        self.leftPanel.setMaximumSize(QtCore.QSize(245, 16777215))
        self.leftPanel.setStyleSheet(_fromUtf8(""))
        self.leftPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.leftPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.leftPanel.setObjectName(_fromUtf8("leftPanel"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.leftPanel)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.colorPickerFrame = QtGui.QFrame(self.leftPanel)
        self.colorPickerFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.colorPickerFrame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.colorPickerFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.colorPickerFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.colorPickerFrame.setObjectName(_fromUtf8("colorPickerFrame"))
        self.verticalLayout_2.addWidget(self.colorPickerFrame)
        self.verticalLayout_2.setStretch(0, 5)
        self.mainPanel = QtGui.QFrame(self.leftRightSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainPanel.sizePolicy().hasHeightForWidth())
        self.mainPanel.setSizePolicy(sizePolicy)
        self.mainPanel.setMinimumSize(QtCore.QSize(32, 32))
        self.mainPanel.setAutoFillBackground(False)
        self.mainPanel.setStyleSheet(_fromUtf8(""))
        self.mainPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mainPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.mainPanel.setObjectName(_fromUtf8("mainPanel"))
        self.verticalLayout = QtGui.QVBoxLayout(self.mainPanel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.canvasFrame = QtGui.QFrame(self.mainPanel)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvasFrame.sizePolicy().hasHeightForWidth())
        self.canvasFrame.setSizePolicy(sizePolicy)
        self.canvasFrame.setStyleSheet(_fromUtf8(""))
        self.canvasFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.canvasFrame.setObjectName(_fromUtf8("canvasFrame"))
        self.verticalLayout.addWidget(self.canvasFrame)
        self.verticalLayout.setStretch(0, 12)
        self.rightPanel = QtGui.QFrame(self.leftRightSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightPanel.sizePolicy().hasHeightForWidth())
        self.rightPanel.setSizePolicy(sizePolicy)
        self.rightPanel.setMinimumSize(QtCore.QSize(200, 550))
        self.rightPanel.setMaximumSize(QtCore.QSize(380, 16777215))
        self.rightPanel.setStyleSheet(_fromUtf8(""))
        self.rightPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        self.rightPanel.setFrameShadow(QtGui.QFrame.Raised)
        self.rightPanel.setObjectName(_fromUtf8("rightPanel"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.rightPanel)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.previewFrame = QtGui.QFrame(self.rightPanel)
        self.previewFrame.setStyleSheet(_fromUtf8(""))
        self.previewFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.previewFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.previewFrame.setObjectName(_fromUtf8("previewFrame"))
        self.verticalLayout_3.addWidget(self.previewFrame)
        self.layerListFrame = QtGui.QFrame(self.rightPanel)
        self.layerListFrame.setStyleSheet(_fromUtf8(""))
        self.layerListFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.layerListFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.layerListFrame.setObjectName(_fromUtf8("layerListFrame"))
        self.verticalLayout_3.addWidget(self.layerListFrame)
        self.animationBarFrame = QtGui.QFrame(self.topDownSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.animationBarFrame.sizePolicy().hasHeightForWidth())
        self.animationBarFrame.setSizePolicy(sizePolicy)
        self.animationBarFrame.setMinimumSize(QtCore.QSize(0, 100))
        self.animationBarFrame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.animationBarFrame.setStyleSheet(_fromUtf8(""))
        self.animationBarFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.animationBarFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.animationBarFrame.setObjectName(_fromUtf8("animationBarFrame"))
        self.horizontalLayout.addWidget(self.topDownSplitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionImport = QtGui.QAction(MainWindow)
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
