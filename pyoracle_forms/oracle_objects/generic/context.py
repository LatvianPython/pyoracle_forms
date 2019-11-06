import atexit
import builtins
from ctypes import *
from functools import partial

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.forms_api import dlls

if hasattr(builtins, "pyoracle_forms_ENCODING"):
    ENCODING = builtins.pyoracle_forms_ENCODING
else:
    ENCODING = "utf-8"

if hasattr(builtins, "pyoracle_forms_VERSION"):
    VERSION = builtins.pyoracle_forms_VERSION
else:
    VERSION = "12c"


class Context:
    def __init__(self):
        self.version, self.encoding = None, None
        self.api, self.free = None, None
        self._as_parameter_ = None

    def init(self, version, encoding):
        self.version, self.encoding = version, encoding
        self.api, self.free = dlls(self.version)
        self._as_parameter_ = self.create_context()
        atexit.register(self.destroy_context)

    def api_function(self, func, arguments):
        api_func = getattr(self.api, func)
        api_func.argtypes = (c_void_p,) + arguments

        api_func = partial(api_func, self)

        return api_func

    def handled_api_function(self, func, arguments):
        @handle_error_code
        def wrapped(*args):
            return self.api_function(func, arguments)(*args), None

        return wrapped

    @handle_error_code
    def create_context(self):
        ctx = c_void_p()
        attributes = c_int()

        func = self.api.d2fctxcr_Create
        func.argtypes = (c_void_p, c_void_p)

        error_code = func(pointer(ctx), pointer(attributes))

        return error_code, ctx

    @handle_error_code
    def destroy_context(self):
        func = api.d2fctxde_Destroy
        func.argtypes = (c_void_p,)
        error_code = func(self)
        self._as_parameter_.value = 0

        return error_code, None

    def set_text(self, generic_object, property_number, text):
        self.handled_api_function("d2fobst_SetTextProp", (c_void_p, c_int, c_void_p))(
            generic_object, property_number, text.encode(self.encoding)
        )

    def set_boolean(self, generic_object, property_number, boolean):
        self.handled_api_function("d2fobsb_SetBoolProp", (c_void_p, c_int, c_bool))(
            generic_object, property_number, boolean
        )

    def set_number(self, generic_object, property_number, number):
        self.handled_api_function("d2fobsn_SetNumProp", (c_void_p, c_int, c_int))(
            generic_object, property_number, number
        )

    def set_object(self, generic_object, property_number, obj):
        self.handled_api_function("d2fobso_SetObjProp", (c_void_p, c_int, c_void_p))(
            generic_object, property_number, obj
        )

    def get_boolean(self, generic_object, property_number):
        func = self.handled_api_function(
            "d2fobgb_GetBoolProp", (c_void_p, c_int, c_void_p)
        )
        arg = c_bool(False)
        func(generic_object, property_number, pointer(arg))

        return arg.value

    def get_number(self, generic_object, property_number):
        func = self.handled_api_function(
            "d2fobgn_GetNumProp", (c_void_p, c_int, c_void_p)
        )
        arg = c_int()
        func(generic_object, property_number, pointer(arg))

        return arg.value

    def get_text(self, generic_object, property_number):
        func = self.handled_api_function(
            "d2fobgt_GetTextProp", (c_void_p, c_int, c_void_p)
        )
        arg = c_char_p()
        func(generic_object, property_number, pointer(arg))

        try:
            text = arg.value.decode(self.encoding)
        except AttributeError:
            text = ""
        else:
            free(arg)
        return text

    def get_object(self, generic_object, property_number):
        func = self.handled_api_function(
            "d2fobgo_GetObjProp", (c_void_p, c_int, c_void_p)
        )
        arg = c_void_p()
        func(generic_object, property_number, pointer(arg))

        return arg.value

    def load_module(self, form_path):
        func = self.handled_api_function("d2ffmdld_Load", (c_void_p, c_char_p, c_bool))

        form = c_void_p()
        func(pointer(form), form_path.encode("utf-8"), False)

        return form

    def create_module(self, name):
        func = self.handled_api_function("d2ffmdcr_Create", (c_void_p, c_char_p))

        form = c_void_p()
        func(pointer(form), name.encode("utf-8"))

        return form

    def save_module(self, module, path):
        self.handled_api_function("d2ffmdsv_Save", (c_void_p, c_char_p, c_bool))(
            module, path.encode("utf-8"), False
        )

    @handle_error_code
    def has_property(self, generic_object, property_number):
        func = api_function("d2fobhp_HasProp", (c_void_p, c_int))

        error_code = func(generic_object, property_number)

        if error_code in (2, 3):
            return 0, error_code == 2
        return error_code, None

    def create(self, owner, name, object_number):
        func = self.handled_api_function(
            "d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int)
        )
        new_obj = c_void_p()
        func(owner, pointer(new_obj), name.encode("utf-8"), object_number)
        return new_obj

    def destroy(self, generic_object):
        self.handled_api_function("d2fobde_Destroy", (c_void_p,))(generic_object)

    def move(self, generic_object, next_object):
        self.handled_api_function("d2fobmv_Move", (c_void_p, c_void_p))(
            generic_object, next_object
        )

    @handle_error_code
    def query_type(self, generic_object):
        # d2fobqt_QueryType(ctx, p_obj, &v_obj_typ)
        func = api_function("d2fobqt_QueryType", (c_void_p,))

        object_type = c_int()
        error_code = func(generic_object, pointer(object_type))

        return error_code, object_type.value

    @handle_error_code
    def property_constant_name(self, property_number):
        func = api_function("d2fprgcn_GetConstName", (c_int, c_void_p))

        property_const_name = c_char_p()
        error_code = func(property_number, pointer(property_const_name))

        return error_code, property_const_name.value.decode("utf-8")

    @handle_error_code
    def property_name(self, property_number):
        # d2fprgn_GetName(d2fctx, D2FP_ALT_STY, &pname)
        func = api_function("d2fprgn_GetName", (c_int, c_void_p))

        object_type = c_char_p()
        error_code = func(property_number, pointer(object_type))

        try:
            return error_code, object_type.value.decode("utf-8")
        except AttributeError:
            return 0, ""


context = Context()
context.init(version=VERSION, encoding=ENCODING)

api, free = context.api, context.free
api_function = context.api_function


def property_type(property_number):
    return api_function("d2fprgt_GetType", (c_uint,))(property_number)
