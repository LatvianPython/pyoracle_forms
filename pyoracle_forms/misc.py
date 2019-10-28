from pyoracle_forms.forms_api import api_objects
from pyoracle_forms.properties import property_name
from pyoracle_forms.utils import Property


def forms_object(object_type):
    object_type = api_objects[object_type.value]

    def class_decorator(cls):
        for prop in object_type['properties']:
            property_number = prop['property_number']
            prop_name = '_'.join(property_name(property_number).lower().split()).replace('\'', '')
            if prop_name and '(obsolete)' not in prop_name:
                setattr(cls, prop_name, Property(property_number))

        return cls

    return class_decorator
