from pyoracle_forms.constants import Properties
from pyoracle_forms.utils import Property
from .getters import get_property
from .misc import has_property
from .setters import set_property


class GenericObject:
    name = Property(Properties.NAME)

    def __init__(self, generic_object):
        self._as_parameter_ = generic_object

    def has_property(self, property_number):
        return has_property(self, property_number)

    def property_value(self, property_number):
        return get_property(self, property_number)

    def set_property(self, property_number, property_value):
        set_property(self, property_number, property_value)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._as_parameter_)})'

    def __bool__(self):
        return bool(self._as_parameter_)
