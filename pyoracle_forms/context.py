import atexit
from ctypes import *

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.forms_api import api


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

    return error_code,


class Context:
    def __init__(self):
        self._as_parameter_ = create_context()


context = Context()

atexit.register(destroy_context, context)
