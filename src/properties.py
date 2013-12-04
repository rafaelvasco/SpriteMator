'''
Created on 25/11/2013

@author: Rafael
'''

class Property(object):

    def __init__(self, name):

        self._name = name
        self._value = None



    def name(self):

        return self._name

    def value(self):
        return self._value

    def setValue(self, v):
        self._value = v
        

class BooleanValue(Property):

    def __init__(self, name, on=None):

        super(BooleanValue, self).__init__(name)

        if on is not None:

            self._value = on

        else:

            self._value = False


    def setOn(self, on):

        self._value = on

    def isOn(self):

        return self._value == True

class RangedValue(Property):

    def __init__(self, name, minValue, maxValue, initialValue=None):

        super(RangedValue, self).__init__(name)

        self._minValue = minValue
        self._maxValue = maxValue
        
        if initialValue is not None:
            self._value = initialValue
        else:
            self._value = 0

    def min(self):
    
        return self._minValue

    def max(self):
    
        return self._maxValue

    def setMin(self, v):

        self._minValue = v

    def setMax(self, v):

        self._maxValue = v

class PropertyHolder(object):

    def __init__(self):
        
        self._properties = {}


    def name(self):
        return None

    def properties(self):
        return self._properties

    def property(self, name):

        return self._properties[name].value()

    def addProperty(self, prop):

        self._properties[prop.name()] = prop