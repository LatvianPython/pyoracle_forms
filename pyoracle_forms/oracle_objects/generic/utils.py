import enum

from pyoracle_forms.properties import property_type
from .wrapped_functions import get_boolean
from .wrapped_functions import get_number
from .wrapped_functions import get_object
from .wrapped_functions import get_text
from .wrapped_functions import set_boolean
from .wrapped_functions import set_number
from .wrapped_functions import set_object
from .wrapped_functions import set_text


class ValueTypes(enum.IntEnum):
    UNKNOWN = 0
    BOOLEAN = 1
    NUMBER = 2
    TEXT = 3
    OBJECT = 4


property_getters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: get_boolean,
    ValueTypes.NUMBER: get_number,
    ValueTypes.TEXT: get_text,
    ValueTypes.OBJECT: get_object,
}

property_setters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: set_boolean,
    ValueTypes.NUMBER: set_number,
    ValueTypes.TEXT: set_text,
    ValueTypes.OBJECT: set_object,
}


def get_property(generic_object, property_number):
    value_type = property_type(property_number=property_number)
    try:
        func = property_getters[value_type]
    except KeyError:
        return f"UNKNOWN PROPERTY TYPE({value_type})"  # todo: decide what to do with these?
    else:
        return func(generic_object, property_number=property_number)


def set_property(generic_object, property_number, property_value):
    value_type = property_type(property_number=property_number)

    func = property_setters[value_type]

    func(generic_object, property_number, property_value)
