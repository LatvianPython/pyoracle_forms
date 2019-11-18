import enum
from typing import Dict, Callable, Type, Tuple, Union

from .context import object_name
from .context import property_constant_name
from .context import property_name
from .context import query_type
from .generic_object import BaseObject, GenericObject

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


class Property:
    def __init__(self, property_number):
        self.property_number = property_number

    def __get__(self, instance, owner):
        return instance.get_property(self.property_number)

    def __set__(self, instance, value):
        instance.set_property(self.property_number, value)


class Subobjects:
    def __init__(self, property_number, prop_name):
        self.property_number, self.property_name = property_number, prop_name

    def __get__(self, instance, owner):
        def gen_subobjects():
            child = instance.get_property(self.property_number)
            if child:
                klass = registered_objects[object_name(query_type(child))]
                child = klass(child)
                while child:
                    yield child
                    child = klass(child.next_object)

        subobjects = list(gen_subobjects())
        return subobjects

    def __set__(self, instance, value):
        raise AttributeError


def property_attribute(property_number: int) -> Tuple[str, Union[Property, Subobjects]]:
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
        return prop_name, Subobjects(property_number, prop_name)


def add_properties(cls: Type[BaseObject], api_objects: Dict) -> Type[BaseObject]:
    object_type = cls.object_type
    obj_type = api_objects[object_type.value]
    cls._object_number = obj_type["object_number"]

    for forms_object_property in obj_type["properties"]:

        property_number = forms_object_property["property_number"]

        prop_name, attribute = property_attribute(property_number)

        if prop_name and "(obsolete)" not in prop_name:
            setattr(cls, prop_name, attribute)

    return cls


def forms_object(cls: Type[BaseObject]) -> Type[BaseObject]:
    registered_objects[cls.object_type.value[6:]] = cls
    return cls
