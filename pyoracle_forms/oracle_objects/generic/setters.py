from ctypes import *

from pyoracle_forms.constants import ValueTypes
from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.properties import property_type
from pyoracle_forms.utils import api_function


@handle_error_code
def set_text(generic_object, property_number, text):
    # d2fobst_SetTextProp(ctx, obj, pnum, text);
    func = api_function('d2fobst_SetTextProp', (c_void_p, c_int, c_void_p))

    # todo: encoding should not be hardcoded
    text = text.encode('utf-8')
    error_code = func(generic_object, property_number, text)

    return error_code,


@handle_error_code
def set_boolean(generic_object, property_number, boolean):
    # d2fobsb_SetBoolProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, boolean prp );
    func = api_function('d2fobsb_SetBoolProp', (c_void_p, c_int, c_bool))

    error_code = func(generic_object, property_number, boolean)

    return error_code,


@handle_error_code
def set_numeric(generic_object, property_number, numeric):
    # d2fobsn_SetNumProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, number prp );
    func = api_function('d2fobsn_SetNumProp', (c_void_p, c_int, c_int))

    error_code = func(generic_object, property_number, numeric)

    return error_code,


@handle_error_code
def set_object(generic_object, property_number, obj):
    # d2fobso_SetObjProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, dvoid *prp );
    func = api_function('d2fobso_SetObjProp', (c_void_p, c_int, c_void_p))

    error_code = func(generic_object, property_number, obj)

    return error_code,


# ORA_RETTYPE(d2fstatus) d2fobsp_SetBlobProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, dvoid *prp );

property_setters = {
    # ValueTypes.UNKNOWN: None,
    ValueTypes.BOOLEAN: set_boolean,
    ValueTypes.NUMBER: set_numeric,
    ValueTypes.TEXT: set_text,
    ValueTypes.OBJECT: set_object
}


def set_property(generic_object, property_number, property_value):
    value_type = property_type(property_number=property_number)

    func = property_setters[value_type]

    func(generic_object, property_number, property_value)
