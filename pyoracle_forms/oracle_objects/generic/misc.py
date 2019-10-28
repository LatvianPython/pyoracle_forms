from ctypes import *

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.utils import api_function


@handle_error_code
def query_type(generic_object):
    # d2fobqt_QueryType(ctx, p_obj, &v_obj_typ)
    func = api_function('d2fobqt_QueryType', (c_void_p,))

    object_type = c_int()
    error_code = func(generic_object, pointer(object_type))

    return error_code, object_type.value


@handle_error_code
def type_name(object_type):
    # d2fobgcn_GetConstName(ctx, v_obj_typ, &v_typ_name)
    func = api_function('d2fobgcn_GetConstName', (c_uint, c_void_p))

    return_val = c_char_p()
    error_code = func(object_type, pointer(return_val))

    return error_code, return_val.value.decode('utf-8')


@handle_error_code
def has_property(generic_object, property_number):
    # d2fobhp_HasProp(ctx, p_obj, D2FP_NAME)
    func = api_function('d2fobhp_HasProp', (c_void_p, c_int))

    error_code = func(generic_object, property_number)

    if error_code in (2, 3):
        return 0, error_code == 2
    return error_code, None
