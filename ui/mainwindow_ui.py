

from PyQt5.QtCore import QSize, Qt, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QFrame, QSizePolicy, QToolBar, QAction

class Ui_MainWindow(object):

    def setupUi(self, main_window):

        main_window.setObjectName("mainWindow")
        main_window.resize(1024, 768)
        main_window.setMinimumSize(QSize(1024, 768))
        main_window.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.horizontalLayout = QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.topDownSplitter = QSplitter(self.central_widget)
        self.topDownSplitter.setOrientation(Qt.Vertical)
        self.topDownSplitter.setOpaqueResize(True)
        self.topDownSplitter.setHandleWidth(5)
        self.topDownSplitter.setObjectName("topDownSplitter")

        self.leftRightSplitter = QSplitter(self.topDownSplitter)
        self.leftRightSplitter.setOrientation(Qt.Horizontal)
        self.leftRightSplitter.setObjectName("leftRightSplitter")

        self.leftPanel = QFrame(self.leftRightSplitter)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftPanel.sizePolicy().hasHeightForWidth())

        self.leftPanel.setSizePolicy(sizePolicy)
        self.leftPanel.setMinimumSize(QSize(245, 550))
        self.leftPanel.setMaximumSize(QSize(245, 16777215))
        self.leftPanel.setFrameShape(QFrame.StyledPanel)
        self.leftPanel.setFrameShadow(QFrame.Raised)
        self.leftPanel.setObjectName("leftPanel")

        self.leftPanelVLayout = QVBoxLayout(self.leftPanel)
        self.leftPanelVLayout.setObjectName("leftPanelVLayout")

        self.colorPickerFrame = QFrame(self.leftPanel)
        self.colorPickerFrame.setMinimumSize(QSize(0, 0))
        self.colorPickerFrame.setMaximumSize(QSize(16777215, 16777215))
        self.colorPickerFrame.setFrameShape(QFrame.StyledPanel)
        self.colorPickerFrame.setFrameShadow(QFrame.Raised)
        self.colorPickerFrame.setObjectName("colorPickerFrame")

        self.leftPanelVLayout.addWidget(self.colorPickerFrame)
        self.leftPanelVLayout.setStretch(0, 5)

        self.mainPanel = QFrame(self.leftRightSplitter)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainPanel.sizePolicy().hasHeightForWidth())

        self.mainPanel.setSizePolicy(sizePolicy)
        self.mainPanel.setMinimumSize(QSize(320, 240))
        self.mainPanel.setAutoFillBackground(False)
        self.mainPanel.setFrameShape(QFrame.StyledPanel)
        self.mainPanel.setFrameShadow(QFrame.Raised)
        self.mainPanel.setObjectName("mainPanel")

        self.verticalLayout = QVBoxLayout(self.mainPanel)
        self.verticalLayout.setObjectName("verticalLayout")

        self.canvasFrame = QFrame(self.mainPanel)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvasFrame.sizePolicy().hasHeightForWidth())

        self.canvasFrame.setSizePolicy(sizePolicy)
        self.canvasFrame.setMinimumSize(310, 230)
        self.canvasFrame.setFrameShape(QFrame.StyledPanel)
        self.canvasFrame.setFrameShadow(QFrame.Raised)
        self.canvasFrame.setObjectName("canvasFrame")

        self.verticalLayout.addWidget(self.canvasFrame)
        self.verticalLayout.setStretch(0, 12)

        self.rightPanel = QFrame(self.leftRightSplitter)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightPanel.sizePolicy().hasHeightForWidth())

        self.rightPanel.setSizePolicy(sizePolicy)
        self.rightPanel.setMinimumSize(QSize(245, 550))
        self.rightPanel.setMaximumSize(QSize(340, 16777215))
        self.rightPanel.setFrameShape(QFrame.StyledPanel)
        self.rightPanel.setFrameShadow(QFrame.Raised)
        self.rightPanel.setObjectName("rightPanel")

        self.rightPanelLayout = QVBoxLayout(self.rightPanel)
        self.rightPanelLayout.setObjectName("rightPanelLayout")

        self.previewFrame = QFrame(self.rightPanel)
        self.previewFrame.setMaximumSize(320, 500)
        self.previewFrame.setFrameShape(QFrame.StyledPanel)
        self.previewFrame.setFrameShadow(QFrame.Raised)
        self.previewFrame.setObjectName("previewFrame")

        self.rightPanelLayout.addWidget(self.previewFrame)

        self.layerListFrame = QFrame(self.rightPanel)
        self.layerListFrame.setFrameShape(QFrame.StyledPanel)
        self.layerListFrame.setFrameShadow(QFrame.Raised)
        self.layerListFrame.setObjectName("layerListFrame")

        self.rightPanelLayout.addWidget(self.layerListFrame)

        self.animationBarFrame = QFrame(self.topDownSplitter)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.animationBarFrame.sizePolicy().hasHeightForWidth())

        self.animationBarFrame.setSizePolicy(sizePolicy)
        self.animationBarFrame.setMinimumSize(QSize(600, 100))
        self.animationBarFrame.setMaximumSize(QSize(16777215, 100))
        self.animationBarFrame.setFrameShape(QFrame.StyledPanel)
        self.animationBarFrame.setFrameShadow(QFrame.Raised)
        self.animationBarFrame.setObjectName("animationBarFrame")

        self.horizontalLayout.addWidget(self.topDownSplitter)

        main_window.setCentralWidget(self.central_widget)

        self.toolBar = QToolBar(main_window)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())

        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")

        main_window.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.actionNew = QAction(main_window)
        self.actionNew.setObjectName("actionNew")

        self.actionQuit = QAction(main_window)
        self.actionQuit.setObjectName("actionQuit")

        self.actionOpen = QAction(main_window)
        self.actionOpen.setObjectName("actionOpen")

        self.actionSave = QAction(main_window)
        self.actionSave.setObjectName("actionSave")

        self.actionSaveAs = QAction(main_window)
        self.actionSaveAs.setObjectName("actionSaveAs")

        self.actionClose = QAction(main_window)
        self.actionClose.setObjectName("actionClose")

        self.actionExport = QAction(main_window)
        self.actionExport.setObjectName("actionExport")

        self.actionImport = QAction(main_window)
        self.actionImport.setObjectName("actionImport")

        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionClose)
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(main_window)
        QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):

        _translate = QCoreApplication.translate

        main_window.setWindowTitle(_translate("MainWindow", "SpriteMator"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))

        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setIconText(_translate("MainWindow", "New"))
        self.actionNew.setToolTip(_translate("MainWindow", "New Sprite"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Close Application"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Esc"))

        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open Sprite"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save Sprite"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))

        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs"))
        self.actionSaveAs.setToolTip(_translate("MainWindow", "Save Sprite with another name"))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))

        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setToolTip(_translate("MainWindow", "Close Sprite"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q"))

        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionExport.setToolTip(_translate("MainWindow", "Export Sprite animations : Either as separate images or as a spritesheet"))
        self.actionExport.setShortcut(_translate("MainWindow", "Ctrl+E"))

        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setToolTip(_translate("MainWindow", "Create a Sprite from one or more images"))
        self.actionImport.setShortcut(_translate("MainWindow", "Ctrl+I"))


import ui.resources_rc
