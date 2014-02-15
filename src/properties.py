class Property(object):
    def __init__(self, name):
        self._name = name
        self._value = None

    def name(self):
        return self._name

    def value(self):
        return self._value

    def set_value(self, v):
        self._value = v


class BooleanValue(Property):
    def __init__(self, name, on=None):

        super(BooleanValue, self).__init__(name)

        if on is not None:

            self._value = on

        else:

            self._value = False

    def set_on(self, on):

        self._value = on

    def is_on(self):

        return self._value is True


class RangedValue(Property):
    def __init__(self, name, min_value, max_value, initial_value=None):

        super(RangedValue, self).__init__(name)

        self._minValue = min_value
        self._maxValue = max_value

        if initial_value is not None:
            self._value = initial_value
        else:
            self._value = 0

    def min(self):

        return self._minValue

    def max(self):

        return self._maxValue

    def set_min(self, v):

        self._minValue = v

    def set_max(self, v):

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

    def add_property(self, prop):
        self._properties[prop.name()] = prop