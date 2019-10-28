from ctypes import *

from pyoracle_forms.constants import ValueTypes
from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.properties import property_type
from pyoracle_forms.utils import api_function, String


@handle_error_code
def bool_property(generic_object, property_number):
    # d2fobgb_GetBoolProp(ctx, p_obj, prop_num, &v_value)
    func = api_function('d2fobgb_GetBoolProp', (c_void_p, c_int, c_void_p))

    arg = c_bool(False)
    error_code = func(generic_object, property_number, pointer(arg))

    return error_code, arg.value


@handle_error_code
def number_property(generic_object, property_number):
    # d2fobgn_GetNumProp(ctx, p_obj, prop_num, &v_value)
    func = api_function('d2fobgn_GetNumProp', (c_void_p, c_int, c_void_p))

    arg = c_int()
    error_code = func(generic_object, property_number, pointer(arg))

    return error_code, arg.value


@handle_error_code
def text_property(generic_object, property_number):
    # d2fobgt_GetTextProp(ctx, p_obj, prop_num, &v_value)
    func = api_function('d2fobgt_GetTextProp', (c_void_p, c_int, c_void_p))

    arg = String()
    error_code = func(generic_object, property_number, pointer(arg))

    try:
        # todo: decoding is broken, forms can be created with any NLS_LANG setting,
        #  should have user decide which encoding to use with what form upon creation of module or context?
        try:
            return error_code, arg.value.decode('utf-8')
        except UnicodeDecodeError:
            return error_code, arg.value.decode('cp1257')
    except AttributeError:
        return error_code, None


@handle_error_code
def object_property(generic_object, property_number):
    # d2fobgo_GetObjProp(ctx, p_obj, prop_num, &v_subobj)
    func = api_function('d2fobgo_GetObjProp', (c_void_p, c_int, c_void_p))

    arg = c_void_p()
    error_code = func(generic_object, property_number, pointer(arg))

    if arg.value:
        return error_code, arg
    return error_code, None


# d2fobgp_GetBlobProp(ctx, obj, D2FP_PERSIST_CLIENT_INFO, val)


property_getters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: bool_property,
    ValueTypes.NUMBER: number_property,
    ValueTypes.TEXT: text_property,
    ValueTypes.OBJECT: object_property
}


def get_property(generic_object, property_number):
    value_type = property_type(property_number=property_number)
    try:
        func = property_getters[value_type]
    except KeyError:
        return f'UNKNOWN PROPERTY TYPE({value_type})'  # todo: decide what to do with these?
    else:
        return func(generic_object, property_number=property_number)
