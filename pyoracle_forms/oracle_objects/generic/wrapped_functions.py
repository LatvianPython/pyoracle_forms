from ctypes import *
import builtins

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.context import api_function, String


if hasattr(builtins, "pyoracle_forms_ENCODING"):
    encoding = builtins.pyoracle_forms_ENCODING
else:
    encoding = "utf-8"


@handle_error_code
def set_text(generic_object, property_number, text):
    # d2fobst_SetTextProp(ctx, obj, pnum, text);
    func = api_function("d2fobst_SetTextProp", (c_void_p, c_int, c_void_p))

    text = text.encode(encoding)
    error_code = func(generic_object, property_number, text)

    return error_code, None


@handle_error_code
def set_boolean(generic_object, property_number, boolean):
    # d2fobsb_SetBoolProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, boolean prp );
    func = api_function("d2fobsb_SetBoolProp", (c_void_p, c_int, c_bool))

    error_code = func(generic_object, property_number, boolean)

    return error_code, None


@handle_error_code
def set_number(generic_object, property_number, numeric):
    # d2fobsn_SetNumProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, number prp );
    func = api_function("d2fobsn_SetNumProp", (c_void_p, c_int, c_int))

    error_code = func(generic_object, property_number, numeric)

    return error_code, None


@handle_error_code
def set_object(generic_object, property_number, obj):
    # d2fobso_SetObjProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, dvoid *prp );
    func = api_function("d2fobso_SetObjProp", (c_void_p, c_int, c_void_p))

    error_code = func(generic_object, property_number, obj)

    return error_code, None


# ORA_RETTYPE(d2fstatus) d2fobsp_SetBlobProp( d2fctx *pd2fctx, d2fob *pd2fob, ub2 pnum, dvoid *prp );


@handle_error_code
def query_type(generic_object):
    # d2fobqt_QueryType(ctx, p_obj, &v_obj_typ)
    func = api_function("d2fobqt_QueryType", (c_void_p,))

    object_type = c_int()
    error_code = func(generic_object, pointer(object_type))

    return error_code, object_type.value


@handle_error_code
def type_name(object_type):
    # d2fobgcn_GetConstName(ctx, v_obj_typ, &v_typ_name)
    func = api_function("d2fobgcn_GetConstName", (c_uint, c_void_p))

    return_val = c_char_p()
    error_code = func(object_type, pointer(return_val))

    return error_code, return_val.value.decode("utf-8")


@handle_error_code
def has_property(generic_object, property_number):
    # d2fobhp_HasProp(ctx, p_obj, D2FP_NAME)
    func = api_function("d2fobhp_HasProp", (c_void_p, c_int))

    error_code = func(generic_object, property_number)

    if error_code in (2, 3):
        return 0, error_code == 2
    return error_code, None


@handle_error_code
def get_boolean(generic_object, property_number):
    # d2fobgb_GetBoolProp(ctx, p_obj, prop_num, &v_value)
    func = api_function("d2fobgb_GetBoolProp", (c_void_p, c_int, c_void_p))

    arg = c_bool(False)
    error_code = func(generic_object, property_number, pointer(arg))

    return error_code, arg.value


@handle_error_code
def get_number(generic_object, property_number):
    # d2fobgn_GetNumProp(ctx, p_obj, prop_num, &v_value)
    func = api_function("d2fobgn_GetNumProp", (c_void_p, c_int, c_void_p))

    arg = c_int()
    error_code = func(generic_object, property_number, pointer(arg))

    return error_code, arg.value


@handle_error_code
def get_text(generic_object, property_number):
    # d2fobgt_GetTextProp(ctx, p_obj, prop_num, &v_value)
    func = api_function("d2fobgt_GetTextProp", (c_void_p, c_int, c_void_p))

    arg = String()
    error_code = func(generic_object, property_number, pointer(arg))

    try:
        return error_code, arg.value.decode(encoding)
    except AttributeError:
        return error_code, None


@handle_error_code
def get_object(generic_object, property_number):
    # d2fobgo_GetObjProp(ctx, p_obj, prop_num, &v_subobj)
    func = api_function("d2fobgo_GetObjProp", (c_void_p, c_int, c_void_p))

    arg = c_void_p()
    error_code = func(generic_object, property_number, pointer(arg))

    if arg.value:
        return error_code, arg
    return error_code, None


# d2fobgp_GetBlobProp(ctx, obj, D2FP_PERSIST_CLIENT_INFO, val)


# d2fobdu_Duplicate( d2fctx *pd2fctx, d2fob *new_owner, d2fob *pd2fob_src, d2fob **ppd2fob_dst, text *new_name );
# d2fobfo_FindObj(d2fctx *pd2fctx, d2fob *owner, text *name, d2fotyp objtyp, d2fob **ppd2fob );


@handle_error_code
def create(owner, name, object_number):
    # d2fobcr_Create(ctx, d2fob *owner, d2fob **ppd2fob, text *name, d2fotyp objtyp );
    func = api_function("d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int))

    new_obj = c_void_p()
    error_code = func(owner, pointer(new_obj), name.encode("utf-8"), object_number)

    return error_code, new_obj


@handle_error_code
def destroy(generic_object):
    # d2fobde_Destroy( d2fctx *pd2fctx, d2fob *pd2fob );
    func = api_function("d2fobde_Destroy", (c_void_p,))

    error_code = func(generic_object)

    return error_code, None


@handle_error_code
def move(generic_object, next_object):
    # d2fobmv_Move( d2fctx *pd2fctx, d2fob *pd2fob, d2fob *pd2fob_nxt );
    func = api_function("d2fobmv_Move", (c_void_p, c_void_p))

    error_code = func(generic_object, next_object)

    return error_code, None
