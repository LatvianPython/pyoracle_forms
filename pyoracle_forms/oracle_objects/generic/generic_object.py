from .utils import get_property
from .utils import set_property
from pyoracle_forms.context import context


class GenericObject:
    _object_number = None

    def __init__(self, generic_object):
        self._as_parameter_ = generic_object

    def has_property(self, property_number):
        return context.has_property(self, property_number)

    def property_value(self, property_number):
        return get_property(self, property_number)

    def set_property(self, property_number, property_value):
        set_property(self, property_number, property_value)

    def destroy(self):
        context.destroy(self)
        self._as_parameter_ = 0

    @classmethod
    def create(cls, owner, name):
        new_object = cls(context.create(owner, name, cls._object_number))
        return new_object

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._as_parameter_)})"

    def __bool__(self):
        return bool(self._as_parameter_)
