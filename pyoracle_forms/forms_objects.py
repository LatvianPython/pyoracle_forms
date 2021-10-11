from __future__ import annotations

from ctypes import c_void_p
from types import TracebackType
from typing import Optional, Type, Union

from .context import create_module
from .context import load_module
from .context import save_module
from .generic_object import GenericObject, BaseObject, FormsObjects
from .misc import forms_object, Text, Number, Object, Bool, Subobjects


@forms_object
class Module(BaseObject):
    object_type = FormsObjects.module

    name = Text("NAME")
    comments = Text("COMMENT")
    console_window = Text("CONSOLE_WIN")
    cursor_mode = Number("CRSR_MODE")
    direction = Number("LANG_DIR")
    first_navigation_data_block = Text("FRST_NAVIGATION_BLK_NAM")
    menu_module = Text("MNU_MOD")
    menu_role = Text("MNU_ROLE")
    initial_menu = Text("INIT_MNU")
    form_horizontal_toolbar_canvas = Text("HORZ_TLBR_CNV")
    form_vertical_toolbar_canvas = Text("VERT_TLBR_CNV")
    mouse_navigation_limit = Number("MOUSE_NAVIGATION_LMT")
    current_record_visual_attribute_group = Text("REC_VAT_GRP_NAM")
    savepoint_mode = Bool("SVPNT_MODE")
    title = Text("TITLE")
    use_3d_controls = Bool("USE_3D_CNTRLS")
    validation_unit = Number("VALIDATION_UNIT")
    title_string_id = Number("TITLE_STRID")
    interaction_mode = Number("INTERACTION_MODE")
    maximum_query_time = Number("MAX_QRY_TIME")
    maximum_records_fetched = Number("MAX_RECS_FETCHED")
    isolation_mode = Number("ISOLATION_MODE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    runtime_compatibility_mode = Number("RUNTIME_COMP")
    parent_objects_type = Number("PAR_TYP")
    help_book_title = Text("HELP_BOOK_TITLE")
    defer_required_enforcement = Number("NEWDEFER_REQ_ENF")

    alerts: Subobjects[Alert] = Subobjects("ALERT")
    attached_libraries: Subobjects[AttachedLibrary] = Subobjects("ATT_LIB")
    data_blocks: Subobjects[DataBlock] = Subobjects("BLOCK")
    canvases: Subobjects[Canvas] = Subobjects("CANVAS")
    editors: Subobjects[Editor] = Subobjects("EDITOR")
    form_parameters: Subobjects[FormParameter] = Subobjects("FORM_PARAM")
    lovs: Subobjects[LOV] = Subobjects("LOV")
    menus: Subobjects[Menu] = Subobjects("MENU")
    triggers: Subobjects[Trigger] = Subobjects("TRIGGER")
    visual_attributes: Subobjects[VisualAttribute] = Subobjects("VIS_ATTR")
    windows: Subobjects[Window] = Subobjects("WINDOW")
    reports: Subobjects[Report] = Subobjects("REPORT")
    object_groups: Subobjects[ObjectGroup] = Subobjects("OBJ_GRP")
    program_units: Subobjects[ProgramUnit] = Subobjects("PROG_UNIT")
    property_classes: Subobjects[PropertyClass] = Subobjects("PROP_CLASS")
    record_groups: Subobjects[RecordGroup] = Subobjects("REC_GRP")
    events: Subobjects[Event] = Subobjects("EVENT")

    first_data_block_object = Object("FRST_NAVIGATION_BLK_OBJ")

    next_object = Object("NEXT")
    previous_object = Object("PREVIOUS")
    source_object = Object("SOURCE")

    current_record_va_pointer = Object("REC_VAT_GRP_OBJ")

    def __init__(self, module: Union[c_void_p, BaseObject], path: Optional[str] = None):
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
        path = path or self.path
        if path is None:
            raise ValueError("No path provided or available")
        save_module(module=self, path=path)


@forms_object
class AttachedLibrary(GenericObject):
    object_type = FormsObjects.attached_library


@forms_object
class Alert(GenericObject):
    object_type = FormsObjects.alert


@forms_object
class Canvas(GenericObject):
    object_type = FormsObjects.canvas


# todo: todo: undocumented, no .h file
@forms_object
class CompoundText(GenericObject):
    object_type = FormsObjects.compound_text


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


# todo: todo: undocumented, no .h file
@forms_object
class VisualState(GenericObject):
    object_type = FormsObjects.visual_state


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
