from ctypes import c_char_p, c_void_p
from functools import partial

from pyoracle_forms.context import context
from pyoracle_forms.forms_api import api, free


def api_function(func, arguments):
    api_func = getattr(api, func)
    api_func.argtypes = (c_void_p,) + arguments

    api_func = partial(api_func, context)

    return api_func


class String(c_char_p):
    def __del__(self):
        free(self)
