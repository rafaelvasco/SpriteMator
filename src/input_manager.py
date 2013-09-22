'''
Created on 08/09/2013

@author: Rafael Vasco
'''

from PyQt4.QtCore import Qt, pyqtSignal, QObject, QEvent



class InputManager(QObject):
    
    _instance = None
    
    keyPressed = pyqtSignal(Qt.Key)
    keyReleased = pyqtSignal(Qt.Key)
    mousePressed = pyqtSignal(Qt.MouseButton)
    mouseReleased = pyqtSignal(Qt.MouseButton)
    mouseWheel = pyqtSignal(int)
    
    
    
    def __init__(self):
        
        QObject.__init__(self)
        self._keyStateMap = {}
        self._mouseStateMap = {}
        
        
    @staticmethod
    def instance():
        
        if InputManager._instance == None:
            InputManager._instance = InputManager()
        
        return InputManager._instance
    
    def _processKeyPress(self, key):
        
        self.keyPressed.emit(key)
        self._keyStateMap[key] = True
        
        
    def _processKeyRelease(self, key):
        
        self.keyReleased.emit(key)
        self._keyStateMap[key] = False
    
    def _processMousePress(self, button):
        
        self.mousePressed.emit(button)
        self._mouseStateMap[button] = True
    
    def _processMouseRelease(self, button):
        
        self.mouseReleased.emit(button)
        self._mouseStateMap[button] = False
    
    def _processWheel(self, delta):
        
        self.mouseWheel.emit(delta)
    
    def _receiveApplicationEvent(self, event):
        
        if event.type() == QEvent.KeyPress:
            
            self._processKeyPress(event.key())
        
        elif event.type() == QEvent.KeyRelease:
            
            self._processKeyRelease(event.key())
            
        elif event.type() == QEvent.MouseButtonPress:
            
            self._processMousePress(event.button())
            
        elif event.type() == QEvent.MouseButtonRelease:
            
            self._processMouseRelease(event.button())
            
        elif event.type() == QEvent.Wheel:
            
            self._processWheel(event.delta())
    
    def isKeyPressed(self, key):
        
        
        return key in self._keyStateMap and self._keyStateMap[key]
    
    def isMousePressed(self, button):
        
        return button in self._mouseStateMap and self._mouseStateMap[button] or False
            
