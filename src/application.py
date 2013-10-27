#--------------------------------------------------
# Name:             application    
# Purpose:          
#
# Author:           Rafael Vasco
# Date:             10/08/13
# License:          
#--------------------------------------------------

import sys

from PyQt4.QtCore import Qt, QEvent
from PyQt4.QtGui import QApplication, QFontDatabase, QFont

from src.main_window import MainWindow
from src.sprite import Sprite
from src.resources_cache import ResourcesCache


import src.utils as utils

class Application(QApplication):
    
    resources = {}
    
    def __init__(self, args):
        
        super(Application, self).__init__(args)
        
        self._loadFonts()
        
        self._view = MainWindow()
                
        self.setQuitOnLastWindowClosed(True)
        
        self._currentSprite = None
        
        self._loadedSprites = []

        self._connectWithView()
        
        self._view.show()
        
        
        
        sys.exit(self.exec_())

        # --------------------------------------------------------------------------------------------------------------


    def newSprite(self):

        if self._currentSprite is not None:
            self.closeSprite()

        sprite = Sprite.create(640, 480)

        self._loadedSprites.append(sprite)

        self.setSprite(sprite)

    def setSprite(self, sprite):

        self._currentSprite = sprite
        self._view.canvas().setSprite(self._currentSprite)

    def loadSprite(self):

        spriteFile = utils.showOpenFileDialog('Open Sprite:', 'Sprite (*.spr)')

        if spriteFile:
            sprite = Sprite.loadFromFile(spriteFile)

            self.setSprite(sprite)

    def importSprite(self):
        pass
        # imageFiles = Utils.showOpenFilesDialog('Select one or more images:', 'Image (*.png)')

        # if len(imageFiles) > 0:

            # sprite = self._spriteManager.importSprite(imageFiles)

            # if sprite:

                # self._setSprite(sprite)
                #
                # print('Imported sprite from files: ', imageFiles)


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
        pass

    def closeSprite(self):
        # TODO Save Sprite Before Close Test
        self._view.canvas().unloadSprite()
        self._view.animationDisplay().unloadAnimation()
        self._view.layerList().clear()
        self._currentSprite = None


    def terminate(self):

        self.closeSprite()
        self._loadedSprites.clear()
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
    
    def _onKeyPressed(self, event):
        
        key = event.key()
        
        if key == Qt.Key_Space:
            
            self._view.colorPicker().switchActiveColor()
        
        elif key == Qt.Key_C:
            
            self._view.canvas().clear()
    
    def _onMousePressed(self, event):
        pass
    
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
        
        
        if event.type() == QEvent.MouseButtonPress:
            self._onMousePressed(event)
        
        if event.type() == QEvent.KeyPress and not event.isAutoRepeat():
            self._onKeyPressed(event)
        
        if event.type() == QEvent.Wheel:
            self._onMouseWheel(event)
            
        return super(Application, self).notify(receiver, event)
        
        
    def _loadFonts(self):
        
        QFontDatabase.addApplicationFont(":/fonts/font_nokia")
        
        nokiaFont = QFont("Nokia Cellphone FC")
        nokiaFont.setPointSize(12)
        
        
        ResourcesCache.registerResource("NokiaFont", nokiaFont)
        
# ======================================================================================================================

if __name__ == '__main__':
    
    application = Application(sys.argv)

    