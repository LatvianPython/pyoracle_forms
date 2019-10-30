from ctypes import *

from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.utils import api_function


@handle_error_code
def load_module(form_path):
    func = api_function('d2ffmdld_Load', (c_void_p, c_char_p, c_bool))
    form = c_void_p()

    error_code = func(pointer(form), form_path.encode('utf-8'), False)

    return error_code, form


@handle_error_code
def create_module(name):
    func = api_function('d2ffmdcr_Create', (c_void_p, c_char_p))
    form = c_void_p()

    error_code = func(pointer(form), name.encode('utf-8'))

    return error_code, form


@handle_error_code
def destroy_module(module):
    func = api_function('d2ffmdde_Destroy', (c_void_p,))

    error_code = func(module)

    return error_code,


@handle_error_code
def save_module(module, path):
    func = api_function('d2ffmdsv_Save', (c_void_p, c_char_p, c_bool))

    error_code = func(module, path.encode('utf-8'), False)

    return error_code,
