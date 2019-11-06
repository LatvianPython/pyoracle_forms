import enum

from pyoracle_forms.context import context


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


def get_property(generic_object, property_number):
    value_type = context.property_type(property_number=property_number)
    try:
        func = property_getters[value_type]
    except KeyError:
        return f"UNKNOWN PROPERTY TYPE({value_type})"  # todo: decide what to do with these!
    else:
        return func(generic_object, property_number=property_number)


def set_property(generic_object, property_number, property_value):
    value_type = context.property_type(property_number=property_number)

    func = property_setters[value_type]

    func(generic_object, property_number, property_value)
