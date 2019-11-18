from __future__ import annotations

from typing import Callable, Dict
import enum

from .context import create
from .context import destroy
from .context import get_boolean
from .context import get_number
from .context import get_object
from .context import get_text
from .context import has_property
from .context import property_type
from .context import set_boolean
from .context import set_number
from .context import set_object
from .context import set_text
from .context import context


class FormsObjects(enum.Enum):
    canvas = "D2FFO_CANVAS"
    alert = "D2FFO_ALERT"
    attached_library = "D2FFO_ATT_LIB"
    data_block = "D2FFO_BLOCK"
    form_parameter = "D2FFO_FORM_PARAM"
    graphic = "D2FFO_GRAPHIC"
    item = "D2FFO_ITEM"
    point = "D2FFO_POINT"
    program_unit = "D2FFO_PROG_UNIT"
    property_class = "D2FFO_PROP_CLASS"
    radio_button = "D2FFO_RADIO_BUTTON"
    relation = "D2FFO_RELATION"
    tab_page = "D2FFO_TAB_PAGE"
    trigger = "D2FFO_TRIGGER"
    visual_attribute = "D2FFO_VIS_ATTR"
    window = "D2FFO_WINDOW"
    module = "D2FFO_FORM_MODULE"


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
    ValueTypes.BOOLEAN: (set_boolean, lambda x: x),
    ValueTypes.NUMBER: (set_number, lambda x: x),
    ValueTypes.TEXT: (set_text, lambda x: x.encode(context.encoding)),
    ValueTypes.OBJECT: (set_object, lambda x: x),
}


class BaseObject:
    object_type: FormsObjects
    _object_number = None

    def __init__(self, generic_object):
        self._as_parameter_ = generic_object

    def has_property(self, property_number: int) -> bool:
        return has_property(self, property_number)

    def get_property(self, property_number):
        value_type = ValueTypes(property_type(property_number=property_number))
        try:
            func = property_getters[value_type]
        except KeyError:
            return f"UNKNOWN PROPERTY TYPE({value_type})"  # todo: decide what to do with these!
        else:
            return func(self, property_number=property_number)

    def set_property(self, property_number, property_value):
        value_type = ValueTypes(property_type(property_number=property_number))
        func, preprocess = property_setters[value_type]
        func(self, property_number, preprocess(property_value))

    def destroy(self):
        destroy(self)
        self._as_parameter_ = 0

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._as_parameter_)})"

    def __bool__(self):
        return bool(self._as_parameter_)


class GenericObject(BaseObject):
    @classmethod
    def create(cls, owner: BaseObject, name: str) -> GenericObject:
        return cls(create(owner, name, cls._object_number))
