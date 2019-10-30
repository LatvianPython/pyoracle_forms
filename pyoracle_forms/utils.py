from ctypes import c_char_p, c_void_p
from functools import partial

from pyoracle_forms.context import context
from pyoracle_forms.forms_api import api, free


class Property:
    def __init__(self, property_number):
        self.property_number = property_number

    def __get__(self, instance, owner):
        return instance.property_value(self.property_number)

    def __set__(self, instance, value):
        instance.set_property(self.property_number, value)


class Subobjects:
    def __init__(self, property_number, klass=None):
        self.property_number, self.klass = property_number, klass

    def __get__(self, instance, owner):
        from pyoracle_forms.oracle_objects.generic.misc import query_type
        from pyoracle_forms.misc import registered_objects

        def gen_subobjects():
            child = instance.property_value(self.property_number)

            if child:
                klass = self.klass or registered_objects[query_type(child)]
                child = klass(child)
                while child:
                    yield child
                    child = klass(child.next_object)

        return list(gen_subobjects())


def api_function(func, arguments):
    api_func = getattr(api, func)
    api_func.argtypes = (c_void_p,) + arguments

    api_func = partial(api_func, context)

    return api_func


class String(c_char_p):
    def __del__(self):
        free(self)
