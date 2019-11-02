from ctypes import *

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.utils import api_function


# **    d2fprgvn_GetValueName(d2fctx, D2FP_ALT_STY, D2FC_ALST_CAUTION, &vname)
# **    returns "Caution" in the vname [OUT] parameter.


# **    d2fprgvv_GetValueValue(d2fctx, D2FP_ALT_STY, "Caution", &val)
# **    returns 1 in the val [OUT] parameter.


# **    d2fprgcv_GetConstValue(d2fctx, "ALT_STY", &pnum)
# **    returns D2FP_ALT_STY in the pnum [OUT] parameter.


# **    d2fprgcn_GetConstName(d2fctx, D2FP_ALT_STY, &pcname)
# **    returns "ALT_STY" in the pcname [OUT] parameter.

@handle_error_code
def property_constant_name(property_number):
    func = api_function('d2fprgcn_GetConstName', (c_int, c_void_p))

    property_const_name = c_char_p()
    error_code = func(property_number, pointer(property_const_name))

    return error_code, property_const_name.value.decode('utf-8')


# **    d2fprgt_GetType(d2fctx, D2FP_ALT_STY)
# **    returns D2FP_TYP_NUMBER.
def property_type(property_number):
    # d2fprgt_GetType(ctx, prop_num)
    func = api_function('d2fprgt_GetType', (c_uint,))

    return func(property_number)


# **    d2fprgn_GetName(d2fctx, D2FP_ALT_STY, &pname)
# **    returns "Alert Style" in the pname [OUT] parameter.
@handle_error_code
def property_name(property_number):
    # d2fprgn_GetName(d2fctx, D2FP_ALT_STY, &pname)
    func = api_function('d2fprgn_GetName', (c_int, c_void_p))

    object_type = c_char_p()
    error_code = func(property_number, pointer(object_type))

    try:
        return error_code, object_type.value.decode('utf-8')
    except AttributeError:
        return 0, ''
