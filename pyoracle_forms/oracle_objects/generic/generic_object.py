from .utils import get_property
from .utils import set_property
from .wrapped_functions import has_property


class GenericObject:

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
