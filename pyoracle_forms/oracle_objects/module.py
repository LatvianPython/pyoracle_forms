import logging
from ctypes import *

from pyoracle_forms.oracle_objects.alert import Alert
from pyoracle_forms.oracle_objects.attached_library import AttachedLibrary
from pyoracle_forms.oracle_objects.canvas import Canvas
from pyoracle_forms.constants import Properties
from pyoracle_forms.oracle_objects.data_block import DataBlock
from pyoracle_forms.error_handling import handle_error_code
from pyoracle_forms.oracle_objects.form_parameter import FormParameter
from pyoracle_forms.oracle_objects.generic import GenericObject
from pyoracle_forms.oracle_objects.program_unit import ProgramUnit
from pyoracle_forms.oracle_objects.property_class import PropertyClass
from pyoracle_forms.oracle_objects.trigger import Trigger
from pyoracle_forms.oracle_objects.visual_attribute import VisualAttribute
from pyoracle_forms.oracle_objects.window import Window
from pyoracle_forms.utils import api_function, Subobjects


@handle_error_code
def load_module(form_path):
    func = api_function('d2ffmdld_Load', (c_void_p, c_char_p, c_bool))
    form = c_void_p()

    error_code = func(pointer(form), form_path.encode('utf-8'), False)
    logging.debug(f'form = {form}')

    return error_code, form


@handle_error_code
def create_module(name):
    func = api_function('d2ffmdcr_Create', (c_void_p, c_char_p))
    form = c_void_p()

    error_code = func(pointer(form), name.encode('utf-8'))
    logging.debug(f'form = {form}')

    return error_code, form


@handle_error_code
def destroy_module(module):
    func = api_function('d2ffmdde_Destroy', (c_void_p,))

    logging.debug(f'destroying module = {module})')
    error_code = func(module)

    return error_code,


@handle_error_code
def save_module(module, path):
    func = api_function('d2ffmdsv_Save', (c_void_p, c_char_p, c_bool))

    logging.debug(f'saving module = {module})')
    error_code = func(module, path.encode('utf-8'), False)

    return error_code,


class Module(GenericObject):

    def __init__(self, module, path=None):
        super().__init__(module)
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @classmethod
    def create(cls, module):
        return cls(create_module(module))

    @classmethod
    def load(cls, path):
        return cls(load_module(path), path=path)

    def save(self, path=None):
        save_module(self, path or self.path)

    def destroy(self):
        destroy_module(self)

    canvases = Subobjects(Properties.CANVAS, Canvas)
    data_blocks = Subobjects(Properties.BLOCK, DataBlock)
    alerts = Subobjects(Properties.ALERT, Alert)
    attached_libraries = Subobjects(Properties.ATTACHED_LIBRARY, AttachedLibrary)
    program_units = Subobjects(Properties.PROGRAM_UNIT, ProgramUnit)
    form_parameters = Subobjects(Properties.FORM_PARAMETER, FormParameter)
    property_classes = Subobjects(Properties.PROPERTY_CLASS, PropertyClass)
    triggers = Subobjects(Properties.TRIGGER, Trigger)
    visual_attributes = Subobjects(Properties.VISUAL_ATTRIBUTE, VisualAttribute)
    windows = Subobjects(Properties.WINDOW, Window)
