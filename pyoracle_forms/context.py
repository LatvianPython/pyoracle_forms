from __future__ import annotations

import atexit
from ctypes import pointer, c_int, c_void_p, c_char_p, c_bool, c_uint, CDLL
from functools import partial
from typing import (
    Callable,
    Any,
    Optional,
    Tuple,
    TYPE_CHECKING,
    cast,
    Union,
    Type,
    TypeVar,
)

from .error_handling import raise_for_code
from .forms_api import dlls

if TYPE_CHECKING:  # pragma: no cover
    from ctypes import _FuncPointer
    from .generic_object import BaseObject
    from .forms_objects import Module

T = TypeVar("T")

Setter = Callable[["BaseObject", int, T], None]
Getter = Callable[["BaseObject", int], T]
CTypes = Union[Type[c_void_p], Type[c_bool], Type[c_int], Type["String"]]


class Context:
    version: str
    encoding: str
    api: Optional[CDLL]
    free: Optional[_FuncPointer]

    def __init__(self) -> None:
        self.version, self.encoding = "12c", "utf-8"
        self.api, self.free = None, None
        self._as_parameter_ = c_void_p(0)

    def __bool__(self) -> bool:
        return bool(self._as_parameter_)

    def init(self, version: str, encoding: str) -> None:
        if not self:
            self.version, self.encoding = version, encoding
            self.api, msvcrt = dlls(self.version)
            self.free = msvcrt.free
            self.create_context()
            atexit.register(self.destroy_context)

    def create_context(self) -> None:
        # todo: maybe better way than just an assert?
        assert self.api is not None

        ctx = c_void_p()

        func = self.api.d2fctxcr_Create
        func.argtypes = (c_void_p, c_void_p)
        error_code = func(pointer(ctx), pointer(c_int()))
        if error_code:  # pragma: no cover
            raise_for_code(error_code)

        self._as_parameter_ = ctx

    def destroy_context(self) -> None:
        if self._as_parameter_:
            handled_api_function("d2fctxde_Destroy", tuple())(self)
            self._as_parameter_ = c_void_p(0)


context: Context = Context()


class String(c_char_p):
    def __init__(self) -> None:
        # todo: maybe better way than just an assert?
        assert context.free is not None
        super().__init__()
        self.free = context.free

    def __del__(self) -> None:
        self.free(self)


def api_function(  # type: ignore
    api_function_name: str, arguments: Tuple[Any, ...]
) -> Callable[..., int]:
    api_func = getattr(context.api, api_function_name)
    api_func.argtypes = (c_void_p,) + arguments
    return partial(api_func, context)


def inject_return_value(  # type: ignore
    args: Tuple[Any, ...], return_value_index: Optional[int]
) -> Tuple[Any, ...]:
    if return_value_index is not None:
        func_args = list(args)
        return_value = func_args[return_value_index]
        func_args[return_value_index] = pointer(return_value)
        injected_args = tuple(func_args)
    else:
        injected_args, return_value = args, None
    return injected_args, return_value


def handled_api_function(  # type: ignore
    api_function_name: str,
    arguments: Tuple[Any, ...],
    return_value_index: Optional[int] = None,
) -> Callable[..., Any]:
    def _handled_api_function(*args: Any) -> Any:  # type: ignore
        injected_args, return_value = inject_return_value(args, return_value_index)

        error_code = api_function(api_function_name, arguments)(*injected_args)

        if error_code:
            raise_for_code(error_code)
        return return_value

    return _handled_api_function


def handle_return_value(result: int) -> bool:
    if result in (2, 3):  # YES, NO
        return bool(result == 2)
    raise_for_code(result)


def is_subclassed(generic_object: BaseObject) -> bool:
    func = api_function("d2fobis_IsSubclassed", (c_void_p,))
    result = func(generic_object)
    return handle_return_value(result)


def has_property(generic_object: BaseObject, property_number: int) -> bool:
    func = api_function("d2fobhp_HasProp", (c_void_p, c_int))
    result = func(generic_object, property_number)
    return handle_return_value(result)


def setter(function_name: str, setter_type: CTypes) -> Setter[T]:
    return handled_api_function(function_name, (c_void_p, c_int, setter_type))


set_text: Setter[bytes] = setter("d2fobst_SetTextProp", c_void_p)
set_boolean: Setter[bool] = setter("d2fobsb_SetBoolProp", c_bool)
set_number: Setter[int] = setter("d2fobsn_SetNumProp", c_int)
set_object: Setter[BaseObject] = setter("d2fobso_SetObjProp", c_void_p)


def getter(function_name: str, return_type: CTypes) -> Getter[T]:
    func = handled_api_function(function_name, (c_void_p, c_int, c_void_p), 2)

    def _getter(generic_object: BaseObject, property_number: int) -> Getter[T]:
        return func(generic_object, property_number, return_type()).value

    return cast(Getter[T], _getter)


get_boolean: Getter[bool] = getter("d2fobgb_GetBoolProp", c_bool)
get_number: Getter[int] = getter("d2fobgn_GetNumProp", c_int)
get_object: Getter[BaseObject] = getter("d2fobgo_GetObjProp", c_void_p)
get_text: Getter[bytes] = getter("d2fobgt_GetTextProp", String)


def load_module(form_path: str) -> c_void_p:
    return handled_api_function(
        "d2ffmdld_Load", (c_void_p, c_char_p, c_bool), return_value_index=0
    )(c_void_p(), form_path.encode(context.encoding), False)


def create_module(name: str) -> c_void_p:
    return handled_api_function(
        "d2ffmdcr_Create", (c_void_p, c_char_p), return_value_index=0
    )(c_void_p(), name.encode(context.encoding))


def save_module(module: Module, path: str) -> None:
    handled_api_function("d2ffmdsv_Save", (c_void_p, c_char_p, c_bool))(
        module, path.encode(context.encoding), False
    )


def create(owner: BaseObject, name: str, obj_number: int) -> c_void_p:
    return handled_api_function(
        "d2fobcr_Create", (c_void_p, c_void_p, c_char_p, c_int), return_value_index=1
    )(owner, c_void_p(), name.encode(context.encoding), obj_number)


def destroy(generic_object: BaseObject) -> None:
    handled_api_function("d2fobde_Destroy", (c_void_p,))(generic_object)


def move(generic_object: BaseObject, next_object: Optional[BaseObject]) -> None:
    handled_api_function("d2fobmv_Move", (c_void_p, c_void_p))(
        generic_object, next_object
    )


def query_type(generic_object: Union[BaseObject, c_void_p]) -> int:
    return int(
        handled_api_function("d2fobqt_QueryType", (c_void_p,), return_value_index=1)(
            generic_object, c_int()
        ).value
    )


GetConstant = Callable[[int], str]


def get_constant(function_name: str) -> GetConstant:
    def _get_constant(constant_property: int) -> str:
        constant_value = handled_api_function(
            function_name, (c_int, c_void_p), return_value_index=1
        )(constant_property, c_char_p())
        return (constant_value.value or b"").decode(context.encoding)

    return _get_constant


object_name: GetConstant = get_constant("d2fobgcn_GetConstName")
property_constant_name: GetConstant = get_constant("d2fprgcn_GetConstName")
property_name: GetConstant = get_constant("d2fprgn_GetName")


def property_type(property_number: int) -> int:
    return int(api_function("d2fprgt_GetType", (c_uint,))(property_number))


def property_constant_number(property_const_name: str) -> int:
    return handled_api_function(
        "d2fprgcv_GetConstValue", (c_char_p, c_void_p), return_value_index=1
    )(property_const_name.encode(context.encoding), c_int()).value


def object_number(obj_name: str) -> int:
    return int(
        handled_api_function(
            "d2fobgcv_GetConstValue", (c_char_p, c_void_p), return_value_index=1
        )(obj_name.encode(context.encoding), c_int()).value
    )


def set_subclass(
    to_subclass: BaseObject, parent: BaseObject, keep_path: bool = False
) -> None:
    handled_api_function("d2fobsc_SubClass", (c_void_p, c_void_p, c_bool))(
        to_subclass, parent, keep_path
    )


def remove_subclass(to_un_subclass: BaseObject) -> None:
    handled_api_function("d2fobus_UnSubClass", (c_void_p,))(to_un_subclass)
