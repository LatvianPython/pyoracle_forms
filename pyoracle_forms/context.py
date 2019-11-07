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

    def api_function(self, func, arguments):
        api_func = getattr(self.api, func)
        api_func.argtypes = (c_void_p,) + arguments
        return partial(api_func, self)

    def handled_api_function(self, func, arguments, return_value=None):
        @handle_error_code
        def wrapped(*args):
            error_code = self.api_function(func, arguments)(*args)
            if return_value is not None:
                return (
                    error_code,
                    args[return_value].contents,
                )
            return error_code, None

        return wrapped

    def create_context(self):
        ctx = c_void_p()

        func = self.api.d2fctxcr_Create
        func.argtypes = (c_void_p, c_void_p)
        error_code = func(pointer(ctx), pointer(c_int()))
        if error_code:
            raise_for_code(error_code)

        self._as_parameter_ = ctx

    def has_property(self, generic_object, property_number):
        func = self.api_function("d2fobhp_HasProp", (c_void_p, c_int))
        result = func(generic_object, property_number)

        if result in (2, 3):  # YES, NO
            return result == 2
        raise_for_code(result)

    def property_type(self, property_number):
        return self.api_function("d2fprgt_GetType", (c_uint,))(property_number)

    def destroy_context(self):
        self.handled_api_function("d2fctxde_Destroy", tuple())(self)
        self._as_parameter_ = None

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
        return self.handled_api_function(
            "d2fobgb_GetBoolProp", (c_void_p, c_int, c_void_p), return_value=2
        )(generic_object, property_number, pointer(c_bool(False))).value

    def get_number(self, generic_object, property_number):
        return self.handled_api_function(
            "d2fobgn_GetNumProp", (c_void_p, c_int, c_void_p), return_value=2
        )(generic_object, property_number, pointer(c_int())).value

    def get_text(self, generic_object, property_number):
        allocated_text = self.handled_api_function(
            "d2fobgt_GetTextProp", (c_void_p, c_int, c_void_p), return_value=2
        )(generic_object, property_number, pointer(c_char_p()))

        try:
            text = allocated_text.value.decode(self.encoding)
        except AttributeError:
            text = ""
        else:
            self.free(allocated_text)
        return text

    def get_object(self, generic_object, property_number):
        return self.handled_api_function(
            "d2fobgo_GetObjProp", (c_void_p, c_int, c_void_p), return_value=2
        )(generic_object, property_number, pointer(c_void_p())).value

    def load_module(self, form_path):
        return self.handled_api_function(
            "d2ffmdld_Load", (c_void_p, c_char_p, c_bool), return_value=0
        )(pointer(c_void_p()), form_path.encode("utf-8"), False)

    def create_module(self, name):
        return self.handled_api_function(
            "d2ffmdcr_Create", (c_void_p, c_char_p), return_value=0
        )(pointer(c_void_p()), name.encode("utf-8"))

    def save_module(self, module, path):
        self.handled_api_function("d2ffmdsv_Save", (c_void_p, c_char_p, c_bool))(
            module, path.encode("utf-8"), False
        )

    def create(self, owner, name, object_number):
        return self.handled_api_function(
            "d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int), return_value=1
        )(owner, pointer(c_void_p()), name.encode("utf-8"), object_number)

    def destroy(self, generic_object):
        self.handled_api_function("d2fobde_Destroy", (c_void_p,))(generic_object)

    def move(self, generic_object, next_object):
        self.handled_api_function("d2fobmv_Move", (c_void_p, c_void_p))(
            generic_object, next_object
        )

    def query_type(self, generic_object):
        return self.handled_api_function(
            "d2fobqt_QueryType", (c_void_p,), return_value=1
        )(generic_object, pointer(c_int())).value

    def object_name(self, object_number):
        return self.handled_api_function(
            "d2fobgcn_GetConstName", (c_int, c_void_p), return_value=1
        )(object_number, pointer(c_char_p())).value.decode("utf-8")

    def object_number(self, object_name):
        return self.handled_api_function(
            "d2fobgcv_GetConstValue", (c_char_p, c_void_p), return_value=1
        )(object_name.encode("utf-8"), pointer(c_int())).value

    def property_constant_name(self, property_number):
        return self.handled_api_function(
            "d2fprgcn_GetConstName", (c_int, c_void_p), return_value=1
        )(property_number, pointer(c_char_p())).value.decode("utf-8")

    def property_name(self, property_number):
        try:
            return self.handled_api_function(
                "d2fprgn_GetName", (c_int, c_void_p), return_value=1
            )(property_number, pointer(c_char_p())).value.decode("utf-8")
        except AttributeError:
            return ""


context = Context()
