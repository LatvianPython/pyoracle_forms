from __future__ import annotations

from ctypes import c_void_p
from typing import Optional, Any, Type, List
from types import TracebackType

from .context import create_module
from .context import load_module
from .context import save_module
from .generic_object import GenericObject, BaseObject, FormsObjects
from .misc import forms_object, Text, Number, Object, Bool, Subobjects


@forms_object
class Module(BaseObject):
    object_type = FormsObjects.module

    name: str = Text("NAME")
    comments: str = Text("COMMENT")
    console_window: str = Text("CONSOLE_WIN")
    cursor_mode: int = Number("CRSR_MODE")
    direction: int = Number("LANG_DIR")
    first_navigation_data_block: str = Text("FRST_NAVIGATION_BLK_NAM")
    menu_module: str = Text("MNU_MOD")
    menu_role: str = Text("MNU_ROLE")
    initial_menu: str = Text("INIT_MNU")
    form_horizontal_toolbar_canvas: str = Text("HORZ_TLBR_CNV")
    form_vertical_toolbar_canvas: str = Text("VERT_TLBR_CNV")
    mouse_navigation_limit: int = Number("MOUSE_NAVIGATION_LMT")
    current_record_visual_attribute_group: str = Text("REC_VAT_GRP_NAM")
    savepoint_mode: bool = Bool("SVPNT_MODE")
    title: str = Text("TITLE")
    use_3d_controls: bool = Bool("USE_3D_CNTRLS")
    validation_unit: int = Number("VALIDATION_UNIT")
    title_string_id: int = Number("TITLE_STRID")
    interaction_mode: int = Number("INTERACTION_MODE")
    maximum_query_time: int = Number("MAX_QRY_TIME")
    maximum_records_fetched: int = Number("MAX_RECS_FETCHED")
    isolation_mode: int = Number("ISOLATION_MODE")
    parent_objects_module: str = Text("PAR_MODULE")
    parent_objects_module_type: int = Number("PAR_MODTYP")
    parent_object_name: str = Text("PAR_NAM")
    parent_objects_file_name: str = Text("PAR_FLNAM")
    parent_objects_file_path: str = Text("PAR_FLPATH")
    runtime_compatibility_mode: int = Number("RUNTIME_COMP")
    parent_objects_type: int = Number("PAR_TYP")
    help_book_title: str = Text("HELP_BOOK_TITLE")
    defer_required_enforcement: int = Number("NEWDEFER_REQ_ENF")

    alerts: List[Alert] = Subobjects("ALERT")
    attached_libraries: List[AttachedLibrary] = Subobjects("ATT_LIB")
    data_blocks: List[DataBlock] = Subobjects("BLOCK")
    canvases: List[Canvas] = Subobjects("CANVAS")
    editors: List[Editor] = Subobjects("EDITOR")
    form_parameters: List[FormParameter] = Subobjects("FORM_PARAM")
    lovs: List[LOV] = Subobjects("LOV")
    menus: List[Menu] = Subobjects("MENU")
    triggers: List[Trigger] = Subobjects("TRIGGER")
    visual_attributes: List[VisualAttribute] = Subobjects("VIS_ATTR")
    windows: List[Window] = Subobjects("WINDOW")
    reports: List[Report] = Subobjects("REPORT")
    object_groups: List[ObjectGroup] = Subobjects("OBJ_GRP")
    program_units: List[ProgramUnit] = Subobjects("PROG_UNIT")
    property_classes: List[PropertyClass] = Subobjects("PROP_CLASS")
    record_groups: List[RecordGroup] = Subobjects("REC_GRP")
    events: List[Event] = Subobjects("EVENT")

    first_data_block_object: BaseObject = Object("FRST_NAVIGATION_BLK_OBJ")

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


# todo: this is special, has own create functions in C
@forms_object
class DataSourceArgument(GenericObject):
    object_type = FormsObjects.data_source_argument


# todo: this is special, has own create functions in C
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
