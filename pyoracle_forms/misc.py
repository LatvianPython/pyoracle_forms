import enum
from collections.abc import MutableSequence

from pyoracle_forms.forms_api import api_objects
from pyoracle_forms.oracle_objects import query_type, GenericObject
from pyoracle_forms.properties import property_name, property_constant_name

registered_objects = {}


class ObjectProperties(enum.Enum):
    canvases = 'D2FP_CANVAS'
    alerts = 'D2FP_ALERT'
    attached_libraries = 'D2FP_ATT_LIB'
    data_blocks = 'D2FP_BLOCK'
    form_parameters = 'D2FP_FORM_PARAM'
    graphics = 'D2FP_GRAPHIC'
    items = 'D2FP_ITEM'
    program_units = 'D2FP_PROG_UNIT'
    property_classes = 'D2FP_PROP_CLASS'
    radio_buttons = 'D2FP_RADIO_BUTTON'
    relations = 'D2FP_RELATION'
    tab_pages = 'D2FP_TAB_PAGE'
    triggers = 'D2FP_TRIGGER'
    visual_attributes = 'D2FP_VIS_ATTR'
    windows = 'D2FP_WINDOW'


class Property:
    def __init__(self, property_number):
        self.property_number = property_number

    def __get__(self, instance, owner):
        return instance.property_value(self.property_number)

    def __set__(self, instance, value):
        instance.set_property(self.property_number, value)


# todo: better name
class ManagedObjects(MutableSequence):
    def __init__(self, iterable):
        self.data = list(iterable)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __delitem__(self, key):
        item = self.data[key]
        item.destroy()
        del self.data[key]

    def __setitem__(self, key, value):
        if isinstance(value, GenericObject):
            raise NotImplementedError
        else:
            raise TypeError(f'Should be instance of {GenericObject.__name__}')

    def insert(self, index, obj):
        raise NotImplementedError


class Subobjects:
    def __init__(self, property_number, prop_name):
        self.property_number, self.property_name = property_number, prop_name

    def __get__(self, instance, owner):
        def gen_subobjects():
            child = instance.property_value(self.property_number)
            if child:
                klass = registered_objects[query_type(child)]
                child = klass(child)
                while child:
                    yield child
                    child = klass(child.next_object)

        # subobjects = ManagedObjects(gen_subobjects())
        # setattr(instance, self.property_name, subobjects)

        subobjects = list(gen_subobjects())
        return subobjects


def forms_object(cls):
    object_type = cls.object_type
    obj_type = api_objects[object_type.value]
    setattr(cls, '_object_number', obj_type['object_number'])

    registered_objects[cls._object_number] = cls

    for prop in obj_type['properties']:

        property_number = prop['property_number']

        const_name = f'D2FP_{property_constant_name(property_number)}'
        try:
            obj_property = ObjectProperties(const_name)
        except ValueError:
            prop_name = '_'.join(property_name(property_number).lower().split()).replace('\'', '')
            if prop_name and '(obsolete)' not in prop_name:
                setattr(cls, prop_name, Property(property_number))
        else:
            prop_name = obj_property.name
            setattr(cls, prop_name, Subobjects(property_number, prop_name))

    return cls
