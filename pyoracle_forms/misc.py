import enum
from ctypes import c_void_p
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
)

from .context import context
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
from .generic_object import BaseObject, PropertyTypes

registered_objects: Dict[str, Type[BaseObject]] = {}


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


class Property:
    def __init__(self, property_number: int):
        self.property_number = property_number

    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> PropertyTypes:
        return instance.get_property(self.property_number)

    def __set__(self, instance: BaseObject, value: PropertyTypes) -> None:
        instance.set_property(self.property_number, value)


class Text:
    def __init__(self, constant: str):
        self.constant = constant

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


class Bool:
    def __init__(self, constant: str):
        self.constant = constant

    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> bool:
        return get_boolean(instance, property_constant_number(self.constant))

    def __set__(self, instance: BaseObject, value: bool) -> None:
        set_boolean(instance, property_constant_number(self.constant), value)


class Number:
    def __init__(self, constant: str):
        self.constant = constant

    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> int:
        return get_number(instance, property_constant_number(self.constant))

    def __set__(self, instance: BaseObject, value: int) -> None:
        set_number(instance, property_constant_number(self.constant), value)


class Object:
    def __init__(self, constant: str):
        self.constant = constant

    def __get__(self, instance: BaseObject, owner: Type[BaseObject]) -> BaseObject:
        return BaseObject(get_object(instance, property_constant_number(self.constant)))

    def __set__(self, instance: BaseObject, value: BaseObject) -> None:
        set_object(instance, property_constant_number(self.constant), value)


T = TypeVar("T")


class Subobjects(Generic[T]):
    def __init__(self, constant: str) -> None:
        self.constant = constant

    def __get__(
        self, instance: BaseObject, owner: Type[BaseObject]
    ) -> List[BaseObject]:
        def gen_subobjects() -> Iterable[BaseObject]:
            first_child: c_void_p = instance.get_property(
                property_constant_number(self.constant)
            )
            if first_child:
                obj_name = object_name(query_type(first_child))
                klass = registered_objects[obj_name]
                child = klass(first_child)
                while child:
                    yield child
                    child = klass(child.next_object)

        subobjects = list(gen_subobjects())
        return subobjects

    def __set__(self, instance: BaseObject, value: List[BaseObject]) -> NoReturn:
        raise AttributeError("can't set attribute")


def property_attribute(
    property_number: int,
) -> Tuple[str, Union[Property, Subobjects[BaseObject]]]:
    const_name = f"D2FP_{property_constant_name(property_number)}"
    try:
        obj_property = ObjectProperties(const_name)
    except ValueError:
        prop_name = (
            "_".join(property_name(property_number).lower().split())
            .replace("'", "")
            .replace("-", "_")
            .replace("/", "_")
        )
        return prop_name, Property(property_number)
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

        attribute: Union[str, Union[Property, Subobjects[BaseObject]]]
        prop_name, attribute = property_attribute(property_number)

        if prop_name and "(obsolete)" not in prop_name:
            setattr(cls, prop_name, attribute)

    return cls


def forms_object(cls: Type[BaseObject]) -> Type[BaseObject]:
    registered_objects[cls.object_type.value[6:]] = cls
    return cls
