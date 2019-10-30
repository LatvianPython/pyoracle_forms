from pyoracle_forms.constants import ObjectProperties
from pyoracle_forms.forms_api import api_objects
from pyoracle_forms.properties import property_name, property_constant_name
from pyoracle_forms.utils import Property, Subobjects

registered_objects = {}


def forms_object(object_type):
    object_type = api_objects[object_type.value]

    def class_decorator(cls):
        setattr(cls, '_object_number', object_type['object_number'])

        registered_objects[cls._object_number] = cls

        for prop in object_type['properties']:

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
                setattr(cls, prop_name, Subobjects(property_number))

        return cls

    return class_decorator
