#-----------------------------------------------------------------------------------------------------------------------
# Name:        Application
# Purpose:
#
# Author:      Rafael Vasco
#
# Created:     10/08/2013
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

import sys
import logging

from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtGui import QFontDatabase, QFont, QKeySequence, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QShortcut, QMessageBox, QStyle

from src.main_window import MainWindow
from src.sprite import Sprite
from src.resources_cache import ResourcesCache
import src.appdata as appdata
import src.utils as utils


class Application(QApplication):

    resources = {}

    #TODO add indication if file is modified / saved
    #TODO Decide on resizing logistic
    #TODO Add tolerance to Filler
    #TODO Layers: Add Change Opacity, Visibility
    #TODO Add Import from Spritesheets
    #TODO Finish Basic Ink Functionality
    #TODO Finish Color Palette

    #TODO [Post 1.0] Add Effects Support
    #TODO [Post 1.0] Add More Tools : Move, Square, Circle, Line, Color Replacer, Text
    #TODO [Post 1.0] Add More Inks: Add, Bright, Dark, Tile, Grain, H. Grad, V. Grad, Jumnble, Sweep

    def __init__(self, args):

        super(Application, self).__init__(args)

        logging.basicConfig(

            filename='log.txt',
            filemode='w',
            format='%(asctime)s :: %(levelname)s :: %(message)s',
            level=logging.DEBUG
        )

        self._loadAssets()

        self._mainWindow = MainWindow()

        # Activate MainWindow's global event filter
        self.installEventFilter(self._mainWindow)

        # Open window on screen center
        self._mainWindow.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self._mainWindow.size(), self.desktop().availableGeometry()))

        self._shortCuts = {}

        self._initializeShortcuts()

        self.setQuitOnLastWindowClosed(True)

        self._currentSprite = None

        self._connectWithWindowInterface()

        # Load Stylesheet
        style_file = QFile(':/styles/style')
        style_file.open(QIODevice.ReadOnly)

        if style_file.isOpen():
            self.setStyleSheet(str(style_file.readAll(), encoding='ascii'))

        style_file.close()

        self.setFont(ResourcesCache.get('SmallFont'))

        self._mainWindow.show()

        self._updateTopMenu()

        sys.exit(self.exec_())

        # --------------------------------------------------------------------------------------------------------------

    def newSprite(self):

        if self._mainWindow.newSpriteDialog.exec_() == QDialog.Accepted:
            result = self._mainWindow.newSpriteDialog.result()

            if self._currentSprite is not None:
                self.closeSprite()

            sprite = Sprite.create(result.choosen_width, result.choosen_height)

            self.setSprite(sprite)
            self._updateTopMenu()

    def setSprite(self, sprite):

        self._currentSprite = sprite
        self._mainWindow.canvas.setSprite(self._currentSprite)
        self._mainWindow.animationDisplay.setSprite(self._currentSprite)
        self._mainWindow.animationManager.setSprite(self._currentSprite)
        self._mainWindow.layerManager.setSprite(self._currentSprite)

        self._mainWindow.showWorkspace()

    def loadSprite(self):

        sprite_file = utils.showOpenFileDialog('Open Sprite:', 'Sprite (*.spr)')
        if sprite_file:
            sprite = Sprite.loadFromFile(sprite_file)

            self.setSprite(sprite)

            self._updateTopMenu()

    def importSprite(self):

        image_files = utils.showOpenFilesDialog('Select one or more images:', 'PNG Image (*.png)')

        if len(image_files) > 0:

            sprite = Sprite.importFromImageFiles(image_files)
            if sprite:
                self.setSprite(sprite)

                self._updateTopMenu()

    def saveSprite(self):

        if self._currentSprite is None:
            return

        if self._currentSprite.filePath:

            save_path = self._currentSprite.filePath

        else:

            save_path = utils.showSaveFileDialog('Save Sprite...', 'Sprite (*.spr)')

        if save_path is not None and len(save_path) > 0:
            Sprite.save(self._currentSprite, save_path)

    def saveSpriteAs(self):

        if self._currentSprite is None:
            return

        new_save_path = utils.showSaveFileDialog('Save Sprite As...', 'Sprite (*.spr)')

        if new_save_path:
            Sprite.save(self._currentSprite, new_save_path)

            self.closeSprite()

            new_sprite = Sprite.loadFromFile(new_save_path)

            self.setSprite(new_sprite)

    def exportSprite(self):

        if self._currentSprite is None:
            return

        target_folder = utils.showSaveToFolderDialog('Choose a folder to save Sprite animations:')

        if target_folder:

            try:

                #Sprite.export(self._current_sprite, target_folder)
                Sprite.exportToSpritesheet(self._currentSprite, target_folder)

            except Exception as e:

                self._raise_error('exportSprite', e)
                return

            utils.showInfoMessage(self._mainWindow, 'Info', 'Sprite Exported Successfuly.')

    def closeSprite(self):

        # TODO Save Sprite Before Close Test
        self._mainWindow.canvas.unloadSprite()
        self._mainWindow.animationDisplay.unloadSprite()
        self._mainWindow.layerManager.clear()
        self._mainWindow.animationManager.clear()
        self._currentSprite = None

        self._mainWindow.hideWorkspace()

        self._updateTopMenu()

    def terminate(self):

        self.removeEventFilter(self._mainWindow)
        self.closeSprite()
        self._mainWindow.close()

    def toggleLuminosity(self):

        self._mainWindow.canvas.toggleBacklight()

    # ------------------------------------------------------------------------------------------------------------------

    def _connectWithWindowInterface(self):

        self._mainWindow.actionNew.triggered.connect(self.newSprite)
        self._mainWindow.actionOpen.triggered.connect(self.loadSprite)
        self._mainWindow.actionImport.triggered.connect(self.importSprite)
        self._mainWindow.actionSave.triggered.connect(self.saveSprite)
        self._mainWindow.actionSaveAs.triggered.connect(self.saveSpriteAs)
        self._mainWindow.actionExport.triggered.connect(self.exportSprite)
        self._mainWindow.actionClose.triggered.connect(self.closeSprite)
        self._mainWindow.actionQuit.triggered.connect(self.terminate)

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _loadAssets():

        # Fonts #

        QFontDatabase.addApplicationFont(":/fonts/font_nokia")
        QFontDatabase.addApplicationFont(":/fonts/font_flx")

        default_font = QFont("Nokia Cellphone FC")
        default_font.setPointSize(12)

        small_font = QFont("flxpixl")
        small_font.setPointSize(12)

        ResourcesCache.registerResource("BigFont", default_font)
        ResourcesCache.registerResource("SmallFont", small_font)

        # Pixmaps #

        checker_tile_light = utils.generateCheckerboardTile(8, QColor(238, 238, 238), QColor(255, 255, 255))
        checker_tile_dark = utils.generateCheckerboardTile(8, QColor(59, 59, 59), QColor(63, 63, 63))

        ResourcesCache.registerResource("CheckerTileLight", checker_tile_light)
        ResourcesCache.registerResource("CheckerTileDark", checker_tile_dark)

        tool_cursor_1 = QPixmap(':/images/tool_cursor_1')

        ResourcesCache.registerResource('ToolCursor1', tool_cursor_1)

    def _initializeShortcuts(self):

        shortcut_data = appdata.shortcuts

        for holder, shortCutGroup in shortcut_data.items():

            self._shortCuts[holder] = {}

            for shortCutName, shortCutText in shortCutGroup.items():
                shortCut = self._shortCuts[holder][shortCutName] = QShortcut(QKeySequence(shortCutText), self._mainWindow)
                shortCut.setAutoRepeat(False)
                shortCut.activated.connect(
                    lambda h=holder, n=shortCutName: self._onShortcutActivated(h, n))

    def _onShortcutActivated(self, holder, shortcut_name):

        # APPLICATION

        if holder == 'APPLICATION':

            target = self

            if shortcut_name == 'TOGGLE_LUMINOSITY':

                target.toggleLuminosity()

        # CANVAS

        elif holder == 'CANVAS':

            target = self._mainWindow.canvas

            if shortcut_name == 'TOGGLE_VIEW':

                target.toggleView()

            elif shortcut_name == 'TOGGLE_FIT_IN_VIEW':

                target.toggleFitInView()

            elif shortcut_name == 'CLEAR':

                target.clear()

        # ANIMATION MANAGER

        elif holder == 'ANIMATION_MANAGER':

            target = self._mainWindow.animationManager

            if shortcut_name == 'GO_PREV_FRAME':

                target.goToPreviousFrame()

            elif shortcut_name == 'GO_NEXT_FRAME':

                target.goToNextFrame()

        # COLOR PICKER

        elif holder == 'COLORPICKER':

            target = self._mainWindow.colorPicker

            if shortcut_name == 'SWITCH_COLOR':
                target.switch_active_color()

        # TOOLBOX

        elif holder == 'TOOLBOX':

            target = self._mainWindow.canvas.tool_box()

            if shortcut_name == 'TOOL_SLOT_0':
                target.switch_tool_slot(0)
            elif shortcut_name == 'TOOL_SLOT_1':
                target.switch_tool_slot(1)
            elif shortcut_name == 'TOOL_SLOT_2':
                target.switch_tool_slot(2)

    def _raise_error(self, source, exception):

        message = str(exception)
        logging.error('[{0}] {1}'.format(source, message))

        QMessageBox.warning(self._mainWindow, 'Warning', '[{0}] An error has ocurred: {1}'.format(source, message))

    def _updateTopMenu(self):

        if self._currentSprite is not None:

            self._mainWindow.actionNew.setEnabled(True)
            self._mainWindow.actionClose.setEnabled(True)
            self._mainWindow.actionSave.setEnabled(True)
            self._mainWindow.actionSaveAs.setEnabled(True)
            self._mainWindow.actionOpen.setEnabled(True)
            self._mainWindow.actionImport.setEnabled(True)
            self._mainWindow.actionExport.setEnabled(True)

        else:

            self._mainWindow.actionNew.setEnabled(True)
            self._mainWindow.actionClose.setEnabled(False)
            self._mainWindow.actionSave.setEnabled(False)
            self._mainWindow.actionSaveAs.setEnabled(False)
            self._mainWindow.actionOpen.setEnabled(True)
            self._mainWindow.actionImport.setEnabled(True)
            self._mainWindow.actionExport.setEnabled(False)

# ======================================================================================================================

if __name__ == '__main__':

    application = Application(sys.argv)
    ResourcesCache.dispose()
