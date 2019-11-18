from __future__ import annotations

import atexit
from ctypes import pointer, c_int, c_void_p, c_char_p, c_bool, c_uint, CDLL
from functools import partial
from typing import Callable, Any, Optional, Generic

from .error_handling import handle_error_code
from .error_handling import raise_for_code
from .forms_api import dlls

if False:
    from .forms_objects import BaseObject


class Context:
    version: str
    encoding: str
    api: Optional[CDLL]
    free: Optional[Any]

    def __init__(self):
        self.version, self.encoding = "12c", "utf-8"
        self.api, self.free = None, None
        self._as_parameter_ = c_void_p(0)

    def __bool__(self):
        return bool(self._as_parameter_)

    def init(self, version: str, encoding: str) -> None:
        if not self:
            self.version, self.encoding = version, encoding
            self.api, msvcrt = dlls(self.version)
            self.free = msvcrt.free
            self.create_context()
            atexit.register(self.destroy_context)

    def create_context(self):
        assert self.api is not None

        ctx = c_void_p()

        func = self.api.d2fctxcr_Create
        func.argtypes = (c_void_p, c_void_p)
        error_code = func(pointer(ctx), pointer(c_int()))
        if error_code:
            raise_for_code(error_code)

        self._as_parameter_ = ctx

    def destroy_context(self):
        handled_api_function("d2fctxde_Destroy", tuple())(self)
        self._as_parameter_ = c_void_p(0)


context: Context = Context()


class String(c_char_p):
    def __init__(self, *args, **kwargs):
        assert context.free is not None
        super().__init__(*args, **kwargs)
        self.free = context.free

    def __del__(self):
        self.free(self)

    @property
    def value(self):
        value = super().value or b""
        return value.decode(context.encoding)


def api_function(api_function_name, arguments):
    api_func = getattr(context.api, api_function_name)
    api_func.argtypes = (c_void_p,) + arguments
    return partial(api_func, context)


def inject_return_value(args, return_value_index):
    if return_value_index is not None:
        func_args = list(args)
        return_value = func_args[return_value_index]
        func_args[return_value_index] = pointer(return_value)
        injected_args = tuple(func_args)
    else:
        injected_args, return_value = args, None
    return injected_args, return_value


def handled_api_function(api_function_name, arguments, return_value_index=None):
    @handle_error_code
    def _handled_api_function(*args):
        injected_args, return_value = inject_return_value(args, return_value_index)

        error_code = api_function(api_function_name, arguments)(*injected_args)
        return (
            error_code,
            return_value,
        )

    return _handled_api_function


def has_property(generic_object: BaseObject, property_number: int) -> bool:
    func = api_function("d2fobhp_HasProp", (c_void_p, c_int))
    result = func(generic_object, property_number)

    if result in (2, 3):  # YES, NO
        return result == 2
    raise_for_code(result)


def property_type(property_number: int) -> int:
    return api_function("d2fprgt_GetType", (c_uint,))(property_number)


def setter(function_name, setter_type):
    return handled_api_function(function_name, (c_void_p, c_int, setter_type))


set_text: Callable = setter("d2fobst_SetTextProp", c_void_p)
set_boolean: Callable = setter("d2fobsb_SetBoolProp", c_bool)
set_number: Callable = setter("d2fobsn_SetNumProp", c_int)
set_object: Callable = setter("d2fobso_SetObjProp", c_void_p)


def getter(function_name: str, return_type: Any) -> Callable:
    func = handled_api_function(function_name, (c_void_p, c_int, c_void_p), 2)

    def _getter(generic_object: BaseObject, property_number: int) -> Any:
        return func(generic_object, property_number, return_type()).value

    return _getter


get_boolean: Callable = getter("d2fobgb_GetBoolProp", c_bool)
get_number: Callable = getter("d2fobgn_GetNumProp", c_int)
get_object: Callable = getter("d2fobgo_GetObjProp", c_void_p)
get_text: Callable = getter("d2fobgt_GetTextProp", String)


def load_module(form_path):
    return handled_api_function(
        "d2ffmdld_Load", (c_void_p, c_char_p, c_bool), return_value_index=0
    )(c_void_p(), form_path.encode("utf-8"), False)


def create_module(name):
    return handled_api_function(
        "d2ffmdcr_Create", (c_void_p, c_char_p), return_value_index=0
    )(c_void_p(), name.encode("utf-8"))


def save_module(module, path):
    handled_api_function("d2ffmdsv_Save", (c_void_p, c_char_p, c_bool))(
        module, path.encode("utf-8"), False
    )


def create(owner, name, obj_number):
    return handled_api_function(
        "d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int), return_value_index=1
    )(owner, c_void_p(), name.encode("utf-8"), obj_number)


def destroy(generic_object):
    handled_api_function("d2fobde_Destroy", (c_void_p,))(generic_object)


def move(generic_object, next_object):
    handled_api_function("d2fobmv_Move", (c_void_p, c_void_p))(
        generic_object, next_object
    )


def query_type(generic_object):
    return handled_api_function("d2fobqt_QueryType", (c_void_p,), return_value_index=1)(
        generic_object, c_int()
    ).value


def object_number(obj_name):
    return handled_api_function(
        "d2fobgcv_GetConstValue", (c_char_p, c_void_p), return_value_index=1
    )(obj_name.encode("utf-8"), c_int()).value


def get_constant(function_name):
    def _get_constant(constant_property):
        constant_value = handled_api_function(
            function_name, (c_int, c_void_p), return_value_index=1
        )(constant_property, c_char_p())
        try:
            return constant_value.value.decode("utf-8")
        except AttributeError:
            return ""

    return _get_constant


object_name = get_constant("d2fobgcn_GetConstName")
property_constant_name = get_constant("d2fprgcn_GetConstName")
property_name = get_constant("d2fprgn_GetName")
