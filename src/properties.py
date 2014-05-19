from PyQt5.QtWidgets import QSpinBox

from src.widgets import OnOffButton, Slider


class Property(object):
    def __init__(self, name, description, value):
        self._name = name
        self._description = description
        self._value = value

    def name(self):
        return self._name

    def description(self):
        return self._description

    def value(self):
        return self._value

    def set_value(self, v):
        self._value = v

    def build_property_widget(self):
        pass


class NumberProperty(Property):
    def __init__(self, name, description=None, value=None, ):
        super(NumberProperty, self).__init__(name, value, description)

    def build_property_widget(self):
        number_input = QSpinBox()
        number_input.setValue(self.value())
        number_input.valueChanged.connect(lambda v: self.set_value(v))

        return number_input


class BooleanProperty(Property):
    def __init__(self, name, description=None, on=None):

        super(BooleanProperty, self).__init__(name, description, on)

        if on is not None:

            self._value = on

        else:

            self._value = False

    def set_on(self, on):

        self._value = on

    def toggle(self):

        self._value = not self._value

    def is_on(self):

        return self._value is True

    def build_property_widget(self):

        bool_input = OnOffButton()
        bool_input.setChecked(self.is_on())
        bool_input.toggled.connect(lambda: self.toggle())

        return bool_input


class RangedProperty(Property):
    def __init__(self, name, min_value, max_value, description, initial_value=None):

        super(RangedProperty, self).__init__(name, description, initial_value)

        self._minValue = min_value
        self._maxValue = max_value

        if initial_value is not None:
            self._value = initial_value
        else:
            self._value = self._minValue

    def set_value(self, v):

        self._value = v

        if self._value < self._minValue:
            self._value = self._minValue
        elif self._value > self._maxValue:
            self._value = self._maxValue

    def min(self):

        return self._minValue

    def max(self):

        return self._maxValue

    def set_min(self, v):

        self._minValue = v

    def set_max(self, v):

        self._maxValue = v

    def build_property_widget(self):

        ranged_input = Slider(self.min(), self.max())
        ranged_input.set_value(self.value())
        ranged_input.valueChanged.connect(lambda v: self.set_value(v))

        return ranged_input


class PropertyHolder(object):
    def __init__(self):
        self._properties = {}

    def properties(self):
        return self._properties

    def property(self, name):
        return self._properties[name]

    def has_property(self, name):
        return name in self._properties.keys()

    def property_value(self, name):
        return self._properties[name].value()

    def add_property(self, prop_name, prop_value, prop_description=None):

        if type(prop_value) is int:
            self._properties[prop_name] = NumberProperty(prop_name, prop_description, prop_value)
        elif type(prop_value) is bool:
            self._properties[prop_name] = BooleanProperty(prop_name, prop_description, prop_value)

    def add_ranged_property(self, prop_name, prop_min, prop_max, prop_value=None, prop_description=None):
        self._properties[prop_name] = RangedProperty(prop_name, prop_min, prop_max, prop_description, prop_value,)

