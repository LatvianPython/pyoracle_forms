from __future__ import annotations

import enum
from typing import (
    Dict,
    Type,
    Tuple,
    Union,
    NoReturn,
    Iterable,
    List,
    TypeVar,
    Generic,
    Any,
    TYPE_CHECKING,
)

from .context import context, property_type
from .context import get_boolean
from .context import get_number
from .context import get_object
from .context import get_text
from .context import object_name
from .context import property_constant_name
from .context import property_constant_number
from .context import property_name
from .context import query_type
from .context import set_boolean
from .context import set_number
from .context import set_object
from .context import set_text
from .generic_object import BaseObject, ValueTypes, GenericObject

if TYPE_CHECKING:
    from . import Module

registered_objects: Dict[str, Union[Type[GenericObject], Type["Module"]]] = {}


class ObjectProperties(enum.Enum):
    canvases = "D2FP_CANVAS"
    alerts = "D2FP_ALERT"
    attached_libraries = "D2FP_ATT_LIB"
    data_blocks = "D2FP_BLOCK"
    form_parameters = "D2FP_FORM_PARAM"
    graphics = "D2FP_GRAPHIC"
    items = "D2FP_ITEM"
    points = "D2FP_POINT"
    program_units = "D2FP_PROG_UNIT"
    property_classes = "D2FP_PROP_CLASS"
    radio_buttons = "D2FP_RADIO_BUTTON"
    relations = "D2FP_RELATION"
    tab_pages = "D2FP_TAB_PAGE"
    triggers = "D2FP_TRIGGER"
    visual_attributes = "D2FP_VIS_ATTR"
    windows = "D2FP_WINDOW"
    data_source_arguments = "D2FP_DAT_SRC_ARG"
    data_source_columns = "D2FP_DAT_SRC_COL"
    editors = "D2FP_EDITOR"
    event = "D2FP_EVENT"
    lovs = "D2FP_LOV"
    lov_column_maps = "D2FP_LV_COLMAP"
    menus = "D2FP_MENU"
    menu_items = "D2FP_MENU_ITEM"
    object_groups = "D2FP_OBJ_GRP"
    object_children = "D2FP_OBG_CHILD"
    record_groups = "D2FP_REC_GRP"
    record_group_colspecs = "D2FP_COL_SPEC"
    reports = "D2FP_REPORT"
    column_value = "D2FP_COLUMN_VALUE"


class Common:
    def __init__(self, constant: str):
        self.constant = constant


class Unknown(Common):
    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> NoReturn:
        raise NotImplementedError()

    def __set__(self, instance: BaseObject, value: Any) -> NoReturn:
        raise NotImplementedError()


class Text(Common):
    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> str:
        return (
            get_text(instance, property_constant_number(self.constant)) or b""
        ).decode(context.encoding)

    def __set__(self, instance: BaseObject, value: str) -> None:
        set_text(
            instance,
            property_constant_number(self.constant),
            value.encode(context.encoding),
        )


class Bool(Common):
    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> bool:
        return get_boolean(instance, property_constant_number(self.constant))

    def __set__(self, instance: BaseObject, value: bool) -> None:
        set_boolean(instance, property_constant_number(self.constant), value)


class Number(Common):
    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> int:
        return get_number(instance, property_constant_number(self.constant))

    def __set__(self, instance: BaseObject, value: int) -> None:
        set_number(instance, property_constant_number(self.constant), value)


class Object(Common):
    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> BaseObject:
        return BaseObject(get_object(instance, property_constant_number(self.constant)))

    def __set__(self, instance: BaseObject, value: BaseObject) -> None:
        set_object(instance, property_constant_number(self.constant), value)


T = TypeVar("T")

properties = {
    ValueTypes.UNKNOWN: Unknown,
    ValueTypes.BOOLEAN: Bool,
    ValueTypes.NUMBER: Number,
    ValueTypes.TEXT: Text,
    ValueTypes.OBJECT: Object,
}


class Subobjects(Generic[T]):
    def __init__(self, constant: str) -> None:
        self.constant = constant

    def __get__(
        self, instance: GenericObject, owner: Type[GenericObject]
    ) -> List[GenericObject]:
        def gen_subobjects() -> Iterable[GenericObject]:
            first_child = get_object(instance, property_constant_number(self.constant))
            if first_child:
                obj_name = object_name(query_type(first_child))
                klass: Type[GenericObject] = registered_objects[obj_name]  # type: ignore

                child = klass(first_child)
                while child:
                    yield child
                    child = klass(child.next_object)  # type: ignore

        subobjects = list(gen_subobjects())
        return subobjects

    def __set__(self, instance: BaseObject, value: List[BaseObject]) -> NoReturn:
        raise AttributeError("can't set attribute")


def property_attribute(
    property_number: int,
) -> Tuple[str, Union[Common, Subobjects[BaseObject]]]:
    constant_name = property_constant_name(property_number)
    const_name = f"D2FP_{constant_name}"
    try:
        obj_property = ObjectProperties(const_name)
    except ValueError:
        prop_name = (
            "_".join(property_name(property_number).lower().split())
            .replace("'", "")
            .replace("-", "_")
            .replace("/", "_")
        )
        value_type = ValueTypes(property_type(property_number=property_number))
        klass = properties[value_type]
        return prop_name, klass(constant_name)
    else:
        prop_name = obj_property.name
        return prop_name, Subobjects(property_constant_name(property_number))


def object_type(cls: Type[BaseObject], api_objects: Dict) -> Tuple[Dict, int]:
    try:
        obj_type = api_objects[cls.object_type.value]
    except KeyError:
        # todo: clean up dirty hack
        #  mostly for column_value, which seems to be not documented by orcl anyway
        obj_type = api_objects["D2FFO_ANY"]
        object_number = 6
    else:
        object_number = obj_type["object_number"]

    return obj_type, object_number


def add_properties(cls: Type[BaseObject], api_objects: Dict) -> Type[BaseObject]:
    obj_type, cls._object_number = object_type(cls, api_objects)

    for forms_object_property in obj_type["properties"]:

        property_number = forms_object_property["property_number"]

        attribute: Union[str, Union[Common, Subobjects[BaseObject]]]
        prop_name, attribute = property_attribute(property_number)

        if prop_name and "(obsolete)" not in prop_name:
            setattr(cls, prop_name, attribute)

    return cls


def forms_object(
    cls: Union[Type[GenericObject], Type[Module]]
) -> Union[Type[GenericObject], Type[Module]]:
    registered_objects[cls.object_type.value[6:]] = cls
    return cls
