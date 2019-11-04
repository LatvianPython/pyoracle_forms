import atexit
from functools import partial
from ctypes import *

from .forms_api import api, free
from pyoracle_forms.error_handling import handle_error_code


def api_function(func, arguments):
    api_func = getattr(api, func)
    api_func.argtypes = (c_void_p,) + arguments

    api_func = partial(api_func, context)

    return api_func


class String(c_char_p):
    def __del__(self):
        free(self)


@handle_error_code
def create_context():
    ctx = c_void_p()
    attributes = c_int()

    func = api.d2fctxcr_Create
    func.argtypes = (c_void_p, c_void_p)

    error_code = func(pointer(ctx), pointer(attributes))

    return error_code, ctx


@handle_error_code
def destroy_context(ctx):
    func = api.d2fctxde_Destroy
    func.argtypes = (c_void_p,)
    error_code = func(ctx)
    ctx.value = 0

    return error_code, None


class Context:
    def __init__(self):
        self._as_parameter_ = create_context()


context = Context()

atexit.register(destroy_context, context)
