from __future__ import annotations

from typing import Callable, Dict, Optional, Any, Tuple, Union, TYPE_CHECKING
from ctypes import c_void_p
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

if TYPE_CHECKING:
    from .context import Setter
    from .context import Getter


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
    data_source_argument = "D2FFO_DAT_SRC_ARG"
    data_source_column = "D2FFO_DAT_SRC_COL"
    editor = "D2FFO_EDITOR"
    event = "D2FFO_EVENT"
    lov = "D2FFO_LOV"
    lov_column_map = "D2FFO_LV_COLMAP"
    menu = "D2FFO_MENU"
    menu_item = "D2FFO_MENU_ITEM"
    object_group = "D2FFO_OBJ_GROUP"
    object_child = "D2FFO_OBG_CHILD"
    record_group = "D2FFO_REC_GROUP"
    record_group_colspec = "D2FFO_RG_COLSPEC"
    report = "D2FFO_REPORT"
    column_value = "D2FFO_COLUMN_VALUE"


class ValueTypes(enum.IntEnum):
    UNKNOWN = 0
    BOOLEAN = 1
    NUMBER = 2
    TEXT = 3
    OBJECT = 4


PropertyTypes = Union[bool, int, str, "BaseObject", c_void_p]


property_getters: Dict[ValueTypes, Tuple[Getter, Callable]] = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: (get_boolean, lambda x: x),
    ValueTypes.NUMBER: (get_number, lambda x: x),
    ValueTypes.TEXT: (get_text, lambda x: (x or b"").decode(context.encoding)),
    ValueTypes.OBJECT: (get_object, lambda x: x),
}

property_setters: Dict[ValueTypes, Tuple[Setter, Callable]] = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: (set_boolean, lambda x: x),
    ValueTypes.NUMBER: (set_number, lambda x: x),
    ValueTypes.TEXT: (set_text, lambda x: x.encode(context.encoding)),
    ValueTypes.OBJECT: (set_object, lambda x: x),
}


class BaseObject:
    object_type: FormsObjects
    _object_number: Optional[int]
    _as_parameter_: c_void_p

    def __init__(self, generic_object: c_void_p) -> None:
        self._as_parameter_ = generic_object

    def has_property(self, property_number: int) -> bool:
        return has_property(self, property_number)

    def get_property(self, property_number: int) -> PropertyTypes:
        value_type = ValueTypes(property_type(property_number=property_number))
        try:
            func, postprocess = property_getters[value_type]
        except KeyError:
            return f"UNKNOWN PROPERTY TYPE({value_type})"  # todo: decide what to do with these!
        else:
            return postprocess(func(self, property_number))

    def set_property(self, property_number: int, property_value: PropertyTypes) -> None:
        value_type = ValueTypes(property_type(property_number=property_number))
        func, preprocess = property_setters[value_type]
        func(self, property_number, preprocess(property_value))

    def destroy(self) -> None:
        destroy(self)
        self._as_parameter_ = c_void_p(0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._as_parameter_)})"

    def __bool__(self) -> bool:
        return bool(self._as_parameter_)


class GenericObject(BaseObject):
    @classmethod
    def create(cls, owner: BaseObject, name: str) -> GenericObject:
        # todo: maybe better way than just an assert?
        assert cls._object_number is not None
        return cls(create(owner, name, cls._object_number))
