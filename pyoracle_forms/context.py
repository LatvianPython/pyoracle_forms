import atexit
from ctypes import pointer, c_int, c_void_p, c_char_p, c_bool, c_uint
from functools import partial

from .error_handling import handle_error_code
from .error_handling import raise_for_code
from .forms_api import dlls


class Context:
    def __init__(self):
        self.version, self.encoding = None, None
        self.api, self.free = None, None
        self._as_parameter_ = c_void_p(0)

    def __bool__(self):
        return bool(self._as_parameter_)

    def init(self, version, encoding):
        if not self:
            self.version, self.encoding = version, encoding
            self.api, self.free = dlls(self.version)
            self.create_context()
            atexit.register(self.destroy_context)

    def create_context(self):
        ctx = c_void_p()

        func = self.api.d2fctxcr_Create
        func.argtypes = (c_void_p, c_void_p)
        error_code = func(pointer(ctx), pointer(c_int()))
        if error_code:
            raise_for_code(error_code)

        self._as_parameter_ = ctx

    def destroy_context(self):
        handled_api_function("d2fctxde_Destroy", tuple())(self)
        self._as_parameter_ = None


context = Context()


def api_function(func, arguments):
    api_func = getattr(context.api, func)
    api_func.argtypes = (c_void_p,) + arguments
    return partial(api_func, context)


def handled_api_function(func, arguments, return_value=None):
    @handle_error_code
    def wrapped(*args):
        error_code = api_function(func, arguments)(*args)
        if return_value is not None:
            return (
                error_code,
                args[return_value].contents,
            )
        return error_code, None

    return wrapped


def has_property(generic_object, property_number):
    func = api_function("d2fobhp_HasProp", (c_void_p, c_int))
    result = func(generic_object, property_number)

    if result in (2, 3):  # YES, NO
        return result == 2
    raise_for_code(result)


def property_type(property_number):
    return api_function("d2fprgt_GetType", (c_uint,))(property_number)


def set_text(generic_object, property_number, text):
    handled_api_function("d2fobst_SetTextProp", (c_void_p, c_int, c_void_p))(
        generic_object, property_number, text.encode(context.encoding)
    )


def set_boolean(generic_object, property_number, boolean):
    handled_api_function("d2fobsb_SetBoolProp", (c_void_p, c_int, c_bool))(
        generic_object, property_number, boolean
    )


def set_number(generic_object, property_number, number):
    handled_api_function("d2fobsn_SetNumProp", (c_void_p, c_int, c_int))(
        generic_object, property_number, number
    )


def set_object(generic_object, property_number, obj):
    handled_api_function("d2fobso_SetObjProp", (c_void_p, c_int, c_void_p))(
        generic_object, property_number, obj
    )


def simple_get(function_name):
    return handled_api_function(
        function_name, (c_void_p, c_int, c_void_p), return_value=2
    )


def get_boolean(generic_object, property_number):
    return simple_get("d2fobgb_GetBoolProp")(
        generic_object, property_number, pointer(c_bool(False))
    ).value


def get_number(generic_object, property_number):
    return simple_get("d2fobgn_GetNumProp")(
        generic_object, property_number, pointer(c_int())
    ).value


def get_object(generic_object, property_number):
    return simple_get("d2fobgo_GetObjProp")(
        generic_object, property_number, pointer(c_void_p())
    ).value


def get_text(generic_object, property_number):
    allocated_text = simple_get("d2fobgt_GetTextProp")(
        generic_object, property_number, pointer(c_char_p())
    )

    try:
        text = allocated_text.value.decode(context.encoding)
    except AttributeError:
        text = ""
    else:
        context.free(allocated_text)
    return text


def load_module(form_path):
    return handled_api_function(
        "d2ffmdld_Load", (c_void_p, c_char_p, c_bool), return_value=0
    )(pointer(c_void_p()), form_path.encode("utf-8"), False)


def create_module(name):
    return handled_api_function(
        "d2ffmdcr_Create", (c_void_p, c_char_p), return_value=0
    )(pointer(c_void_p()), name.encode("utf-8"))


def save_module(module, path):
    handled_api_function("d2ffmdsv_Save", (c_void_p, c_char_p, c_bool))(
        module, path.encode("utf-8"), False
    )


def create(owner, name, obj_number):
    return handled_api_function(
        "d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int), return_value=1
    )(owner, pointer(c_void_p()), name.encode("utf-8"), obj_number)


def destroy(generic_object):
    handled_api_function("d2fobde_Destroy", (c_void_p,))(generic_object)


def move(generic_object, next_object):
    handled_api_function("d2fobmv_Move", (c_void_p, c_void_p))(
        generic_object, next_object
    )


def query_type(generic_object):
    return handled_api_function("d2fobqt_QueryType", (c_void_p,), return_value=1)(
        generic_object, pointer(c_int())
    ).value


def object_number(obj_name):
    return handled_api_function(
        "d2fobgcv_GetConstValue", (c_char_p, c_void_p), return_value=1
    )(obj_name.encode("utf-8"), pointer(c_int())).value


def get_constant(function_name):
    def _get_constant(*args):
        return handled_api_function(function_name, (c_int, c_void_p), return_value=1)(
            *args
        ).value.decode("utf-8")

    return _get_constant


def object_name(obj_number):
    return get_constant("d2fobgcn_GetConstName")(obj_number, pointer(c_char_p()))


def property_constant_name(property_number):
    return get_constant("d2fprgcn_GetConstName")(property_number, pointer(c_char_p()))


def property_name(property_number):
    try:
        return get_constant("d2fprgn_GetName")(property_number, pointer(c_char_p()))
    except AttributeError:
        return ""
