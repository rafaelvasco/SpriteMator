#--------------------------------------------------
# Name:             application    
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             10/08/13
# License:          
#--------------------------------------------------

import sys
import logging

from time import gmtime, strftime
from PyQt4.QtCore import Qt, QEvent, QFile
from PyQt4.QtGui import QApplication, QFontDatabase, QFont, QDialog, QShortcut, QKeySequence, QColor, QPixmap, QMessageBox



from src.main_window import MainWindow
from src.sprite import Sprite
from src.resources_cache import ResourcesCache

import src.appdata as appdata

import src.utils as utils
from PyQt4 import QtCore

class Application(QApplication):
    
    resources = {}
    
    def __init__(self, args):
        
        super(Application, self).__init__(args)
        
        self._loadAssets()
        
        self._view = MainWindow()
        
        self._shortCuts = {}
        
        self._initializeShortcuts()
        
        self.setQuitOnLastWindowClosed(True)
        
        self._currentSprite = None
        
        self._connectWithView()
        
        styleFile = QFile(':/styles/style')
        styleFile.open(QtCore.QIODevice.ReadOnly)
        
        if styleFile.isOpen():
            
            self.setStyleSheet(str(styleFile.readAll(), encoding='ascii'))
        
        styleFile.close()
        
        self.setFont(ResourcesCache.get('SmallFont'))
        
        self._view.show()
        
        self._updateTopMenu()
        
        sys.exit(self.exec_())

        
        
        # --------------------------------------------------------------------------------------------------------------


    def newSprite(self):

        if self._view.newSpriteDialog().exec_() == QDialog.Accepted:
            result = self._view.newSpriteDialog().result()
            
            if self._currentSprite is not None:
                self.closeSprite()
            
            sprite = Sprite.create(result.choosenWidth, result.choosenHeight)
            
            self.setSprite(sprite)
            
            
            
            self._updateTopMenu()
    
    def setSprite(self, sprite):

        self._currentSprite = sprite
        self._view.canvas().setSprite(self._currentSprite)
        self._view.animationManager().setSprite(self._currentSprite)
        self._view.layerManager().setSprite(self._currentSprite)
        
        self._view.showWorkspace()

    def loadSprite(self):

        spriteFile = utils.showOpenFileDialog('Open Sprite:', 'Sprite (*.spr)')

        if spriteFile:
            sprite = Sprite.loadFromFile(spriteFile)

            self.setSprite(sprite)
            
            self._updateTopMenu()

    def importSprite(self):
        pass
        imageFiles = utils.showOpenFilesDialog('Select one or more images:', 'PNG Image (*.png)')

        if len(imageFiles) > 0:

            sprite = Sprite.importFromImageFiles(imageFiles)
            if sprite:

                self.setSprite(sprite)
                
                print('Imported sprite from files: ', imageFiles)
                
                self._updateTopMenu()


    def saveSprite(self):

        if self._currentSprite is None:
            return


        if self._currentSprite.filePath():

            print('Saving sprite to path: ', self._currentSprite.filePath())
            savePath = self._currentSprite.filePath()

        else:

            print('Saving new sprite...')
            savePath = utils.showSaveFileDialog('Save Sprite...', 'Sprite (*.spr)')

        if savePath is not None and len(savePath) > 0:

            Sprite.save(self._currentSprite, savePath)

            print('Saved to: ', savePath)

    def saveSpriteAs(self):

        if self._currentSprite is None:
            return

        newSavePath = utils.showSaveFileDialog('Save Sprite As...', 'Sprite (*.spr)')

        print('Saving to new path: ', newSavePath)

        if newSavePath:

            Sprite.save(self._currentSprite, newSavePath)

            print('Saved to new path')

            self.closeSprite()

            print('Unloaded current sprite')

            newSprite = Sprite.loadFromFile(newSavePath)

            print('Loaded new sprite with new file path')

            self.setSprite(newSprite)

    def exportSprite(self):
        
        if self._currentSprite is None:
            return
        
        targetFolder = utils.showSaveToFolderDialog('Choose a folder to save Sprite animations:')
        
        if targetFolder:
            
            try:
            
                Sprite.export(self._currentSprite, targetFolder)
                
            except Exception as e:
                
                self._raiseError('exportSprite', e)
                return
            
            utils.showInfoMessage(self._view, 'Info', 'Sprite Exported Successfuly.')

    def closeSprite(self):
        # TODO Save Sprite Before Close Test
        self._view.canvas().unloadSprite()
        self._view.animationDisplay().unloadAnimation()
        self._view.layerManager().clear()
        self._view.animationManager().clear()
        self._currentSprite = None
        
        self._view.hideWorkspace()
        
        self._updateTopMenu()


    def terminate(self):

        self.closeSprite()
        self._view.close()

    # ------------------------------------------------------------------------------------------------------------------

    def _connectWithView(self):

        self._view.actionNew.triggered.connect(self.newSprite)
        self._view.actionOpen.triggered.connect(self.loadSprite)
        self._view.actionImport.triggered.connect(self.importSprite)
        self._view.actionSave.triggered.connect(self.saveSprite)
        self._view.actionSaveAs.triggered.connect(self.saveSpriteAs)
        self._view.actionExport.triggered.connect(self.exportSprite)
        self._view.actionClose.triggered.connect(self.closeSprite)
        self._view.actionQuit.triggered.connect(self.terminate)

    # GLOBAL INPUT EVENTS ------------------------------------------------------------------------------------------------
    
    def _onMouseWheel(self, event):
        
        if event.modifiers() & Qt.ControlModifier:
            
            if event.delta() > 0:
                self._view.colorPicker().selectNextColorOnPalette()
            elif event.delta() < 0:
                self._view.colorPicker().selectPreviousColorOnPalette()
        
        elif event.modifiers() & Qt.AltModifier:
            
            if event.delta() > 0:
                self._view.colorPicker().selectNextRampOnPalette()
            elif event.delta() < 0:
                self._view.colorPicker().selectPreviousRampOnPalette()
            
    # ------------------------------------------------------------------------------------------------------------------
    
    def notify(self, receiver, event):
        
       
        if event.type() == QEvent.Wheel:
            self._onMouseWheel(event)
            
        return super(Application, self).notify(receiver, event)
        
        
    def _loadAssets(self):
        
        # Fonts #
        
        QFontDatabase.addApplicationFont(":/fonts/font_nokia")
        QFontDatabase.addApplicationFont(":/fonts/font_flx")
        
        defaultFont = QFont("Nokia Cellphone FC")
        defaultFont.setPointSize(12)
        
        smallFont = QFont("flxpixl")
        smallFont.setPointSize(12)
        
        ResourcesCache.registerResource("BigFont", defaultFont)
        ResourcesCache.registerResource("SmallFont", smallFont)
    
        # Pixmaps #
        
        checkerTileLight = utils.generateCheckerTile(8, QColor(222,222,222), QColor(253,253,253))
        
        ResourcesCache.registerResource("CheckerTileLight", checkerTileLight)
        
        toolCursor1 = QPixmap(':/images/tool_cursor_1')
        
        ResourcesCache.registerResource('ToolCursor1', toolCursor1)
        
        
    
    def _initializeShortcuts(self):
        
        shortCutData = appdata.shortcuts
        
        
        for holder, shortCutGroup in shortCutData.items():
            
            self._shortCuts[holder] = {}
            
            for shortCutName, shortCutText in shortCutGroup.items():
                
                self._shortCuts[holder][shortCutName] = QShortcut(QKeySequence(shortCutText), self._view)
                self._shortCuts[holder][shortCutName].activated.connect(lambda h=holder, n=shortCutName : self._onShortCutActivated(h, n))
                
                
    def _onShortCutActivated(self, holder, shortCutName):
        
        target = None
        
        # CANVAS =============
        
        if holder == 'CANVAS':
            
            target = self._view.canvas()
        
            if shortCutName == 'RESET':
                
                target.resetView()
                
            elif shortCutName == 'CLEAR':
                
                target.clear()
                
            elif shortCutName == 'ZOOM1':
                
                target.zoomTo(1.0)
                
            elif shortCutName == 'ZOOM2':
                
                target.zoomTo(2.0)
                
            elif shortCutName == 'ZOOM3':
                
                target.zoomTo(3.0)
                
            elif shortCutName == 'ZOOM4':
                
                target.zoomTo(4.0)
                
                
        
        # COLORPICKER
        
        elif holder == 'COLORPICKER':
            
            target = self._view.colorPicker()
            
            if shortCutName == 'SWITCH_COLOR':
                
                target.switchActiveColor()
            
    def _raiseError(self, source, exception):

        message = str(exception)
        logging.warning('[{0}] {1}'.format(source, message))
        
        QMessageBox.warning(self._view, 'Warning', '[{0}] An error has ocurred: {1}'.format(source, message))        
                
    
    def _updateTopMenu(self):
        
        
        
        if self._currentSprite is not None:
            
            self._view.actionNew.setEnabled(True)
            self._view.actionClose.setEnabled(True)
            self._view.actionSave.setEnabled(True)
            self._view.actionSaveAs.setEnabled(True)
            self._view.actionOpen.setEnabled(True)
            self._view.actionImport.setEnabled(True)
            self._view.actionExport.setEnabled(True)
        
        else:
            
            self._view.actionNew.setEnabled(True)
            self._view.actionClose.setEnabled(False)
            self._view.actionSave.setEnabled(False)
            self._view.actionSaveAs.setEnabled(False)
            self._view.actionOpen.setEnabled(True)
            self._view.actionImport.setEnabled(True)
            self._view.actionExport.setEnabled(False)
# ======================================================================================================================

if __name__ == '__main__':
    
    application = Application(sys.argv)
    
    ResourcesCache.dispose()

    