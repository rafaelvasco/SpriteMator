#-----------------------------------------------------------------------------------------------------------------------
# Name:        NewSpriteDialog
# Purpose:     New Sprite dialog definition
#
# Author:      Rafael Vasco
#
# Created:     31/03/13
# Copyright:   (c) Rafael 2013
# Licence:     <your licence>
#-----------------------------------------------------------------------------------------------------------------------

from PyQt5.QtWidgets import QDialog, QMessageBox

from ui.newSpriteDialog_ui import Ui_newSpriteDialog


class NewSpriteDialogResult(object):
    
    def __init__(self):
        
        self.choosen_width = 0
        self.choosen_height = 0


class NewSpriteDialog(QDialog, Ui_newSpriteDialog):
    
    def __init__(self):

        QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.buttonCancel.clicked.connect(self._on_button_cancel_clicked)
        self.buttonCreate.clicked.connect(self._on_button_create_clicked)

        self._result = NewSpriteDialogResult()
        
        self._result.choosen_width = self.spinWidth.value()
        self._result.choosen_height = self.spinHeight.value()
        
    def result(self):
        
        return self._result 
    
    def _on_button_create_clicked(self):
        
        if self.radioCustom.isChecked():
            
            self._result.choosen_width = self.spinWidth.value()
            self._result.choosen_height = self.spinHeight.value()
            
            if self._result.choosen_width == 0 or self._result.choosen_height == 0:
            
                QMessageBox.information(self, 'Invalid Size', 'Invalid Sprite Width or Height !')
                return
            
        else:
            
            if self.radio16.isChecked():
                
                self._result.choosen_width = 16
                self._result.choosen_height = 16
                
            elif self.radio24.isChecked():
                
                self._result.choosen_width = 24
                self._result.choosen_height = 24
                
            elif self.radio32.isChecked():
                
                self._result.choosen_width = 32
                self._result.choosen_height = 32
                
            elif self.radio48.isChecked():
                
                self._result.choosen_width = 48
                self._result.choosen_height = 48
                
            elif self.radio64.isChecked():
                
                self._result.choosen_width = 64
                self._result.choosen_height = 64
                
            elif self.radio96.isChecked():
                
                self._result.choosen_width = 96
                self._result.choosen_height = 96
                
            elif self.radio128.isChecked():
                
                self._result.choosen_width = 128
                self._result.choosen_height = 128
                
            elif self.radio256.isChecked():
                
                self._result.choosen_width = 256
                self._result.choosen_height = 256
            
            else:
                
                raise Exception('No radio selected!')

        self.accept()

    def _on_button_cancel_clicked(self):
        
        self.reject()
