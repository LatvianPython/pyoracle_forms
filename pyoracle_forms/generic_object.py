import enum

from .context import context


class ValueTypes(enum.IntEnum):
    UNKNOWN = 0
    BOOLEAN = 1
    NUMBER = 2
    TEXT = 3
    OBJECT = 4


property_getters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: context.get_boolean,
    ValueTypes.NUMBER: context.get_number,
    ValueTypes.TEXT: context.get_text,
    ValueTypes.OBJECT: context.get_object,
}

property_setters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: context.set_boolean,
    ValueTypes.NUMBER: context.set_number,
    ValueTypes.TEXT: context.set_text,
    ValueTypes.OBJECT: context.set_object,
}


class GenericObject:
    _object_number = None

    def __init__(self, generic_object):
        self._as_parameter_ = generic_object

    def has_property(self, property_number):
        return context.has_property(self, property_number)

    def property_value(self, property_number):
        value_type = context.property_type(property_number=property_number)
        try:
            func = property_getters[value_type]
        except KeyError:
            return f"UNKNOWN PROPERTY TYPE({value_type})"  # todo: decide what to do with these!
        else:
            return func(self, property_number=property_number)

    def set_property(self, property_number, property_value):
        value_type = context.property_type(property_number=property_number)
        func = property_setters[value_type]
        func(self, property_number, property_value)

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