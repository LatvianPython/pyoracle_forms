from __future__ import annotations

from ctypes import c_void_p
from typing import Optional, Any, Type
from types import TracebackType

from .context import create_module
from .context import load_module
from .context import save_module
from .generic_object import GenericObject, BaseObject, FormsObjects
from .misc import forms_object


@forms_object
class Module(BaseObject):
    object_type = FormsObjects.module

    def __init__(self, module: c_void_p, path: str):
        super().__init__(module)
        self.path = path

    def __enter__(self) -> Module:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.destroy()

    @classmethod
    def create(cls, module_name: str) -> Module:
        return cls(create_module(module_name), module_name)

    @classmethod
    def load(cls, path: str) -> Module:
        return cls(load_module(path), path=path)

    def save(self, path: Optional[str] = None) -> None:
        save_module(module=self, path=path or self.path)


@forms_object
class AttachedLibrary(GenericObject):
    object_type = FormsObjects.attached_library


@forms_object
class Alert(GenericObject):
    object_type = FormsObjects.alert


@forms_object
class Canvas(GenericObject):
    object_type = FormsObjects.canvas


@forms_object
class DataBlock(GenericObject):
    object_type = FormsObjects.data_block


@forms_object
class FormParameter(GenericObject):
    object_type = FormsObjects.form_parameter


@forms_object
class Graphic(GenericObject):
    object_type = FormsObjects.graphic


@forms_object
class Item(GenericObject):
    object_type = FormsObjects.item


@forms_object
class Point(GenericObject):
    object_type = FormsObjects.point


@forms_object
class ProgramUnit(GenericObject):
    object_type = FormsObjects.program_unit


@forms_object
class PropertyClass(GenericObject):
    object_type = FormsObjects.property_class


@forms_object
class RadioButton(GenericObject):
    object_type = FormsObjects.radio_button


@forms_object
class Relation(GenericObject):
    object_type = FormsObjects.relation


@forms_object
class TabPage(GenericObject):
    object_type = FormsObjects.tab_page


@forms_object
class Trigger(GenericObject):
    object_type = FormsObjects.trigger


@forms_object
class VisualAttribute(GenericObject):
    object_type = FormsObjects.visual_attribute


@forms_object
class Window(GenericObject):
    object_type = FormsObjects.window


@forms_object
class DataSourceArgument(GenericObject):
    object_type = FormsObjects.data_source_argument


@forms_object
class DataSourceColumn(GenericObject):
    object_type = FormsObjects.data_source_column


@forms_object
class Editor(GenericObject):
    object_type = FormsObjects.editor


@forms_object
class LOV(GenericObject):
    object_type = FormsObjects.lov


@forms_object
class LOVColumnMap(GenericObject):
    object_type = FormsObjects.lov_column_map


@forms_object
class Menu(GenericObject):
    object_type = FormsObjects.menu


@forms_object
class MenuItem(GenericObject):
    object_type = FormsObjects.menu_item


@forms_object
class ObjectGroup(GenericObject):
    object_type = FormsObjects.object_group


@forms_object
class ObjectChild(GenericObject):
    object_type = FormsObjects.object_child


@forms_object
class RecordGroup(GenericObject):
    object_type = FormsObjects.record_group


@forms_object
class RecordGroupColspec(GenericObject):
    object_type = FormsObjects.record_group_colspec


@forms_object
class Report(GenericObject):
    object_type = FormsObjects.report


@forms_object
class Event(GenericObject):
    object_type = FormsObjects.event


@forms_object
class ColumnValue(GenericObject):
    object_type = FormsObjects.column_value
