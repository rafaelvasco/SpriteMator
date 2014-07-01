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
    #TODO Add Import and Export from Spritesheets

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

        self._load_assets()

        self._view = MainWindow()

        self.installEventFilter(self._view)

        self._view.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, self._view.size(), self.desktop().availableGeometry()))

        self._shortCuts = {}

        self._initialize_shortcuts()

        self.setQuitOnLastWindowClosed(True)

        self._current_sprite = None

        self._connect_with_view()

        style_file = QFile(':/styles/style')
        style_file.open(QIODevice.ReadOnly)

        if style_file.isOpen():
            self.setStyleSheet(str(style_file.readAll(), encoding='ascii'))

        style_file.close()

        self.setFont(ResourcesCache.get('SmallFont'))

        self._view.show()

        self._update_top_menu()

        sys.exit(self.exec_())

        # --------------------------------------------------------------------------------------------------------------

    def new_sprite(self):

        if self._view.new_sprite_dialog().exec_() == QDialog.Accepted:
            result = self._view.new_sprite_dialog().result()

            if self._current_sprite is not None:
                self.close_sprite()

            sprite = Sprite.create(result.choosen_width, result.choosen_height)

            self.set_sprite(sprite)
            self._update_top_menu()

    def set_sprite(self, sprite):

        self._current_sprite = sprite
        self._view.canvas().set_sprite(self._current_sprite)
        self._view.animation_manager().set_sprite(self._current_sprite)
        self._view.layer_manager().set_sprite(self._current_sprite)

        self._view.show_workspace()

    def load_sprite(self):

        sprite_file = utils.show_openfile_dialog('Open Sprite:', 'Sprite (*.spr)')
        if sprite_file:
            sprite = Sprite.load_from_file(sprite_file)

            self.set_sprite(sprite)

            self._update_top_menu()

    def import_sprite(self):

        image_files = utils.show_open_files_dialog('Select one or more images:', 'PNG Image (*.png)')

        if len(image_files) > 0:

            sprite = Sprite.import_from_image_files(image_files)
            if sprite:
                self.set_sprite(sprite)

                self._update_top_menu()

    def save_sprite(self):

        if self._current_sprite is None:
            return

        if self._current_sprite.file_path():

            save_path = self._current_sprite.file_path()

        else:

            save_path = utils.show_savefile_dialog('Save Sprite...', 'Sprite (*.spr)')

        if save_path is not None and len(save_path) > 0:
            Sprite.save(self._current_sprite, save_path)

    def save_sprite_as(self):

        if self._current_sprite is None:
            return

        new_save_path = utils.show_savefile_dialog('Save Sprite As...', 'Sprite (*.spr)')

        if new_save_path:
            Sprite.save(self._current_sprite, new_save_path)

            self.close_sprite()

            new_sprite = Sprite.load_from_file(new_save_path)

            self.set_sprite(new_sprite)

    def export_sprite(self):

        if self._current_sprite is None:
            return

        target_folder = utils.show_save_to_folder_dialog('Choose a folder to save Sprite animations:')

        if target_folder:

            try:

                #Sprite.export(self._current_sprite, target_folder)
                Sprite.export_to_spritesheet(self._current_sprite, target_folder)

            except Exception as e:

                self._raise_error('exportSprite', e)
                return

            utils.show_info_message(self._view, 'Info', 'Sprite Exported Successfuly.')

    def close_sprite(self):

        # TODO Save Sprite Before Close Test
        self._view.canvas().unload_sprite()
        self._view.animation_display().unload_animation()
        self._view.layer_manager().clear()
        self._view.animation_manager().clear()
        self._current_sprite = None

        self._view.hide_workspace()

        self._update_top_menu()

    def terminate(self):

        self.removeEventFilter(self._view)
        self.close_sprite()
        self._view.close()

    def toggle_luminosity(self):

        self._view.canvas().toggle_back_luminosity()
        self._view.animation_display().toggle_back_luminosity()

    # ------------------------------------------------------------------------------------------------------------------

    def _connect_with_view(self):

        self._view.actionNew.triggered.connect(self.new_sprite)
        self._view.actionOpen.triggered.connect(self.load_sprite)
        self._view.actionImport.triggered.connect(self.import_sprite)
        self._view.actionSave.triggered.connect(self.save_sprite)
        self._view.actionSaveAs.triggered.connect(self.save_sprite_as)
        self._view.actionExport.triggered.connect(self.export_sprite)
        self._view.actionClose.triggered.connect(self.close_sprite)
        self._view.actionQuit.triggered.connect(self.terminate)

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _load_assets():

        # Fonts #

        QFontDatabase.addApplicationFont(":/fonts/font_nokia")
        QFontDatabase.addApplicationFont(":/fonts/font_flx")

        default_font = QFont("Nokia Cellphone FC")
        default_font.setPointSize(12)

        small_font = QFont("flxpixl")
        small_font.setPointSize(12)

        ResourcesCache.register_resource("BigFont", default_font)
        ResourcesCache.register_resource("SmallFont", small_font)

        # Pixmaps #

        checker_tile_light = utils.generate_checker_tile(8, QColor(238, 238, 238), QColor(255, 255, 255))
        checker_tile_dark = utils.generate_checker_tile(8, QColor(59, 59, 59), QColor(63, 63, 63))

        ResourcesCache.register_resource("CheckerTileLight", checker_tile_light)
        ResourcesCache.register_resource("CheckerTileDark", checker_tile_dark)

        tool_cursor_1 = QPixmap(':/images/tool_cursor_1')

        ResourcesCache.register_resource('ToolCursor1', tool_cursor_1)

    def _initialize_shortcuts(self):

        shortcut_data = appdata.shortcuts

        for holder, shortCutGroup in shortcut_data.items():

            self._shortCuts[holder] = {}

            for shortCutName, shortCutText in shortCutGroup.items():
                self._shortCuts[holder][shortCutName] = QShortcut(QKeySequence(shortCutText), self._view)
                self._shortCuts[holder][shortCutName].activated.connect(
                    lambda h=holder, n=shortCutName: self._on_shortcut_activated(h, n))

    def _on_shortcut_activated(self, holder, shortcut_name):

        # APPLICATION

        if holder == 'APPLICATION':

            target = self

            if shortcut_name == 'TOGGLE_LUMINOSITY':

                target.toggle_luminosity()

        # CANVAS

        elif holder == 'CANVAS':

            target = self._view.canvas()

            if shortcut_name == 'RESET':

                target.reset_view()

            elif shortcut_name == 'CLEAR':

                target.clear()

            elif shortcut_name == 'ZOOM1':

                target.zoom_to(1.0)

            elif shortcut_name == 'ZOOM2':

                target.zoom_to(2.0)

            elif shortcut_name == 'ZOOM3':

                target.zoom_to(3.0)

            elif shortcut_name == 'ZOOM4':

                target.zoom_to(4.0)

        # ANIMATION MANAGER

        elif holder == 'ANIMATION_MANAGER':

            target = self._view.animation_manager()

            if shortcut_name == 'GO_PREV_FRAME':

                target.go_to_previous_frame()

            elif shortcut_name == 'GO_NEXT_FRAME':

                target.go_to_next_frame()

        # COLOR PICKER

        elif holder == 'COLORPICKER':

            target = self._view.color_picker()

            if shortcut_name == 'SWITCH_COLOR':
                target.switch_active_color()

        # TOOLBOX

        elif holder == 'TOOLBOX':

            target = self._view.canvas().tool_box()

            if shortcut_name == 'TOOL_SLOT_0':
                target.switch_tool_slot(0)
            elif shortcut_name == 'TOOL_SLOT_1':
                target.switch_tool_slot(1)
            elif shortcut_name == 'TOOL_SLOT_2':
                target.switch_tool_slot(2)

    def _raise_error(self, source, exception):

        message = str(exception)
        logging.error('[{0}] {1}'.format(source, message))

        QMessageBox.warning(self._view, 'Warning', '[{0}] An error has ocurred: {1}'.format(source, message))

    def _update_top_menu(self):

        if self._current_sprite is not None:

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
