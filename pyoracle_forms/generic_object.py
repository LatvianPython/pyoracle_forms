from __future__ import annotations

import enum
from ctypes import c_void_p
from typing import Optional, Union, NoReturn

from .context import create
from .context import destroy
from .context import has_property
from .context import remove_subclass
from .context import set_subclass
from .context import move
from .context import query_type
from .context import is_subclassed

from .property_types import Properties


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
    visual_state = "D2FFO_VIS_STATE"  # todo: undocumented, no .h file
    compound_text = "D2FFO_CMPTXT"  # todo: undocumented, no .h file
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


PropertyTypes = Union[bool, int, str, bytes, "BaseObject", c_void_p]


class BaseObject:
    object_type: FormsObjects
    _object_number: Optional[int]
    _as_parameter_: c_void_p

    def __init__(
        self, generic_object: Union[c_void_p, BaseObject, GenericObject]
    ) -> None:
        if isinstance(generic_object, BaseObject):
            self._as_parameter_ = generic_object._as_parameter_
        else:
            self._as_parameter_ = generic_object

    def has_property(self, property_number: int) -> bool:
        return has_property(self, property_number)

    def destroy(self) -> None:
        destroy(self)
        self._as_parameter_ = c_void_p(0)

    def remove_subclass(self) -> None:
        remove_subclass(self)

    def set_subclass(self, property_class: BaseObject, keep_path: bool = False) -> None:
        set_subclass(self, property_class, keep_path)

    def move(self, next_object: GenericObject) -> None:
        move(self, next_object)

    def query_type(self) -> int:
        return query_type(self)

    def duplicate(self, new_owner: GenericObject, new_name: str) -> NoReturn:
        raise NotImplementedError()

    def replicate(self, new_owner: GenericObject, new_name: str) -> NoReturn:
        raise NotImplementedError()

    def find_object(self, name: str, object_type: FormsObjects) -> NoReturn:
        raise NotImplementedError()

    def inherit_property(self, property_type: Properties) -> NoReturn:
        raise NotImplementedError()

    def is_property_inherited(self, property_type: Properties) -> NoReturn:
        raise NotImplementedError()

    def is_property_default(self, property_type: Properties) -> NoReturn:
        raise NotImplementedError()

    def is_subclassed(self) -> bool:
        return is_subclassed(self)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._as_parameter_)})"

    def __bool__(self) -> bool:
        return bool(self._as_parameter_)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseObject):
            return NotImplemented
        return self._as_parameter_ == other._as_parameter_


class GenericObject(BaseObject):
    @classmethod
    def create(cls, owner: BaseObject, name: str) -> GenericObject:
        # todo: maybe better way than just an assert?
        assert cls._object_number is not None
        return cls(create(owner, name, cls._object_number))
