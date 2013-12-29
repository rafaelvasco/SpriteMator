'''
Created on 28/12/2013

@author: Rafael
'''

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QDialog, QMessageBox

from ui.newSpriteDialog_ui import Ui_newSpriteDialog


class NewSpriteDialogResult(object):
    
    def __init__(self):
        
        self.choosenWidth = 0
        self.choosenHeight = 0

class NewSpriteDialog(QDialog, Ui_newSpriteDialog):
    
    def __init__(self, parent=None):
        
        QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.buttonCancel.clicked.connect(self._onButtonCancelClicked)
        self.buttonCreate.clicked.connect(self._onButtonCreateClicked)
        
        
        self._result = NewSpriteDialogResult()
        
        self._result.choosenWidth = self.spinWidth.value()
        self._result.choosenHeight = self.spinHeight.value()
        
        
    def result(self):
        
        return self._result 
    
    
    def _onButtonCreateClicked(self):
        
        
        
        
        if self.radioCustom.isChecked():
            
            self._result.choosenWidth = self.spinWidth.value()
            self._result.choosenHeight = self.spinHeight.value()
            
            if self._result.choosenWidth == 0 or self._result.choosenHeight == 0:
            
                QMessageBox.information(self, 'Invalid Size', 'Invalid Sprite Width or Height !')
                return
            
        else:
            
            if self.radio16.isChecked():
                
                self._result.choosenWidth = 16
                self._result.choosenHeight = 16
                
            elif self.radio24.isChecked():
                
                self._result.choosenWidth = 24
                self._result.choosenHeight = 24
                
            elif self.radio32.isChecked():
                
                self._result.choosenWidth = 32
                self._result.choosenHeight = 32
                
            elif self.radio48.isChecked():
                
                self._result.choosenWidth = 48
                self._result.choosenHeight = 48
                
            elif self.radio64.isChecked():
                
                self._result.choosenWidth = 64
                self._result.choosenHeight = 64
                
            elif self.radio96.isChecked():
                
                self._result.choosenWidth = 96
                self._result.choosenHeight = 96
                
            elif self.radio128.isChecked():
                
                self._result.choosenWidth = 128
                self._result.choosenHeight = 128
                
            elif self.radio256.isChecked():
                
                self._result.choosenWidth = 256
                self._result.choosenHeight = 256
            
            else:
                
                raise Exception('No radio selected!')
        
        
        
        
        
        self.accept()
    
    def _onButtonCancelClicked(self):
        
        self.reject()
        
   
    