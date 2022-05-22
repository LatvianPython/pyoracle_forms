from __future__ import annotations

from ctypes import c_void_p
from types import TracebackType
from typing import Optional, Type, Union, List, TypeVar

from .context import create_module
from .context import load_module
from .context import save_module
from .context import load_library
from .generic_object import GenericObject, BaseObject, FormsObjects
from .misc import (
    forms_object,
    Text,
    Number,
    Object,
    Bool,
    Subobjects,
    Unknown,
    Constant,
)
from .constants import *


# satisfy both MyPy and PyCharm IDE autocomplete
U = TypeVar("U")
ObjectList = Union[List[U], Subobjects[U]]
Obj = Union[U, Object[U]]


@forms_object
class Module(BaseObject):
    object_type = FormsObjects.module

    name = Text("NAME")
    comments = Text("COMMENT")
    console_window = Text("CONSOLE_WIN")
    cursor_mode: Constant[CursorMode] = Constant("CRSR_MODE", CursorMode)
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    first_navigation_data_block = Text("FRST_NAVIGATION_BLK_NAM")
    menu_module = Text("MNU_MOD")
    menu_role = Text("MNU_ROLE")
    initial_menu = Text("INIT_MNU")
    form_horizontal_toolbar_canvas = Text("HORZ_TLBR_CNV")
    form_vertical_toolbar_canvas = Text("VERT_TLBR_CNV")
    mouse_navigation_limit: Constant[MouseNavigationLimit] = Constant(
        "MOUSE_NAVIGATION_LMT", MouseNavigationLimit
    )
    current_record_visual_attribute_group = Text("REC_VAT_GRP_NAM")
    savepoint_mode = Bool("SVPNT_MODE")
    title = Text("TITLE")
    use_3d_controls = Bool("USE_3D_CNTRLS")
    validation_unit: Constant[ValidationUnit] = Constant(
        "VALIDATION_UNIT", ValidationUnit
    )
    title_string_id = Number("TITLE_STRID")
    interaction_mode: Constant[InteractionMode] = Constant(
        "INTERACTION_MODE", InteractionMode
    )
    maximum_query_time = Number("MAX_QRY_TIME")
    maximum_records_fetched = Number("MAX_RECS_FETCHED")
    isolation_mode: Constant[IsolationMode] = Constant("ISOLATION_MODE", IsolationMode)
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    runtime_compatibility_mode: Constant[RuntimeCompatibilityMode] = Constant(
        "RUNTIME_COMP", RuntimeCompatibilityMode
    )
    parent_objects_type = Number("PAR_TYP")
    help_book_title = Text("HELP_BOOK_TITLE")
    defer_required_enforcement = Number("NEWDEFER_REQ_ENF")

    alerts: ObjectList[Alert] = Subobjects("ALERT")
    attached_libraries: ObjectList[AttachedLibrary] = Subobjects("ATT_LIB")
    data_blocks: ObjectList[DataBlock] = Subobjects("BLOCK")
    canvases: ObjectList[Canvas] = Subobjects("CANVAS")
    editors: ObjectList[Editor] = Subobjects("EDITOR")
    form_parameters: ObjectList[FormParameter] = Subobjects("FORM_PARAM")
    lovs: ObjectList[LOV] = Subobjects("LOV")
    menus: ObjectList[Menu] = Subobjects("MENU")
    triggers: ObjectList[Trigger] = Subobjects("TRIGGER")
    visual_attributes: ObjectList[VisualAttribute] = Subobjects("VIS_ATTR")
    windows: ObjectList[Window] = Subobjects("WINDOW")
    reports: ObjectList[Report] = Subobjects("REPORT")
    object_groups: ObjectList[ObjectGroup] = Subobjects("OBJ_GRP")
    program_units: ObjectList[ProgramUnit] = Subobjects("PROG_UNIT")
    property_classes: ObjectList[PropertyClass] = Subobjects("PROP_CLASS")
    record_groups: ObjectList[RecordGroup] = Subobjects("REC_GRP")
    events: ObjectList[Event] = Subobjects("EVENT")

    next_object: Obj[Module] = Object("NEXT")
    previous_object: Obj[Module] = Object("PREVIOUS")

    first_data_block_object: Obj[DataBlock] = Object("FRST_NAVIGATION_BLK_OBJ")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    current_record_va_pointer: Obj[VisualAttribute] = Object("REC_VAT_GRP_OBJ")

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
class Library(BaseObject):
    object_type = FormsObjects.library

    attached_libraries: ObjectList[AttachedLibrary] = Subobjects("ATT_LIB")
    pl_sql_library_location = Text("LIB_LOC")
    pl_sql_library_source: Constant[PLSQLLibrarySource] = Constant(
        "LIB_SRC", PLSQLLibrarySource
    )
    next_object: Obj[Library] = Object("NEXT")
    previous_object: Obj[Library] = Object("PREVIOUS")
    program_units: ObjectList[LibraryProgramUnit] = Subobjects("LIB_PROG_UNIT")

    def __init__(self, module: Union[c_void_p, BaseObject], path: Optional[str] = None):
        super().__init__(module)
        self.path = path

    def __enter__(self) -> Library:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.destroy()

    @classmethod
    def load(cls, path: str) -> Library:
        return cls(load_library(path), path=path)


@forms_object
class LibraryProgramUnit(GenericObject):
    # auto-generated
    object_type = FormsObjects.library_program_unit

    name = Text("NAME")
    next_object: Obj[LibraryProgramUnit] = Object("NEXT")
    program_unit_text = Text("PGU_TXT")
    program_unit_type: Constant[ProgramUnitType] = Constant("PGU_TYP", ProgramUnitType)


@forms_object
class AttachedLibrary(GenericObject):
    # auto-generated
    object_type = FormsObjects.attached_library

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    pl_sql_library_location = Text("LIB_LOC")
    pl_sql_library_source = Number("LIB_SRC")
    name = Text("NAME")
    next_object: Obj[AttachedLibrary] = Object("NEXT")
    previous_object: Obj[AttachedLibrary] = Object("PREVIOUS")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Alert(GenericObject):
    # auto-generated
    object_type = FormsObjects.alert

    button_1_label = Text("BTN_1_LBL")
    button_2_label = Text("BTN_2_LBL")
    button_3_label = Text("BTN_3_LBL")
    default_alert_button: Constant[DefaultAlertButton] = Constant(
        "DFLT_ALT_BTN", DefaultAlertButton
    )
    message = Text("ALT_MSG")
    alert_style: Constant[AlertStyle] = Constant("ALT_STY", AlertStyle)
    background_color = Text("BACK_COLOR")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    name = Text("NAME")
    next_object: Obj[Alert] = Object("NEXT")
    title = Text("TITLE")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    previous_object: Obj[Alert] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


class Any(GenericObject):
    keyboard_accelerator = Text("KBRD_ACC")
    alerts: Subobjects[Alert] = Subobjects("ALERT")
    justification = Number("JUSTIFICATION")
    button_1_label = Text("BTN_1_LBL")
    button_2_label = Text("BTN_2_LBL")
    button_3_label = Text("BTN_3_LBL")
    default_alert_button = Number("DFLT_ALT_BTN")
    message = Text("ALT_MSG")
    alert_style = Number("ALT_STY")
    attached_libraries: Subobjects[AttachedLibrary] = Subobjects("ATT_LIB")
    automatic_select = Bool("AUTO_SLCT")
    automatic_display = Bool("AUTO_DISP")
    automatic_query = Bool("AUTO_QRY")
    automatic_refresh = Bool("AUTO_RFRSH")
    automatic_skip = Bool("AUTO_SKP")
    background_color = Text("BACK_COLOR")
    database_item = Bool("DB_ITM")
    bevel = Number("BEVEL")
    mirror_item_object: Object[BaseObject] = Object("SYNC_ITM_OBJ")
    data_blocks: Subobjects[DataBlock] = Subobjects("BLOCK")
    bottom_title = Text("BTM_TTL")
    graphics: Subobjects[Graphic] = Subobjects("GRAPHIC")
    canvases: Subobjects[Canvas] = Subobjects("CANVAS")
    canvas = Text("CNV_NAM")
    canvas_object_pointer: Object[Canvas] = Object("CNV_OBJ")
    case_info = Unknown("CLIENT_INFO")
    case_insensitive_query = Bool("CASE_INSENSITIVE_QRY")
    case_restriction = Number("CASE_RSTRCTION")
    check_box_mapping_of_other_values = Number("CHK_BX_OTHER_VALS")
    value_when_checked = Text("CHKED_VAL")
    close_allowed = Bool("CLS_ALLOWED")
    canvas_type = Number("CNV_TYP")
    synchronize_with_item = Text("SYNC_ITM_NAM")
    column_data_type = Number("COL_DAT_TYP")
    column_mapping_object: Object[LOVColumnMap] = Object("COL_MAP")
    enforce_column_security = Bool("ENFRC_COL_SECURITY")
    record_group_colspecs: Subobjects[RecordGroupColspec] = Subobjects("COL_SPEC")
    command_text = Text("COM_TXT")
    command_type = Number("COM_TYP")
    comments = Text("COMMENT")
    image_format = Number("IMG_FMT")
    console_window = Text("CONSOLE_WIN")
    image_depth = Number("IMG_DPTH")
    cursor_mode = Number("CRSR_MODE")
    deferred = Bool("DEFERRED")
    delete_allowed = Bool("DEL_ALLOWED")
    delete_record_behavior = Number("DEL_REC")
    prompt_foreground_color = Text("PRMPT_FORE_COLOR")
    detail_data_block = Text("DETAIL_BLK")
    default_button = Bool("DFLT_BTN")
    initial_keyboard_state = Number("INIT_KBRD_DIR")
    direction = Number("LANG_DIR")
    visible = Bool("VISIBLE")
    display_without_privilege = Bool("DISP_NO_PRIV")
    display_width = Number("DISP_WID")
    viewport_x_position = Number("VPRT_X_POS")
    viewport_y_position = Number("VPRT_Y_POS")
    editors: Subobjects[Editor] = Subobjects("EDITOR")
    editor = Text("EDT_NAM")
    editor_object_pointer: Object[Editor] = Object("EDT_OBJ")
    editor_x_position = Number("EDT_X_POS")
    editor_y_position = Number("EDT_Y_POS")
    enabled = Bool("ENABLED")
    execution_hierarchy = Number("EXEC_HIERARCHY")
    fill_pattern = Text("FILL_PAT")
    fire_in_enter_query_mode = Bool("FIRE_IN_QRY")
    first_navigation_data_block = Text("FRST_NAVIGATION_BLK_NAM")
    first_data_block_object: Object[BaseObject] = Object("FRST_NAVIGATION_BLK_OBJ")
    resize_allowed = Bool("RESIZE_ALLOWED")
    menu_module = Text("MNU_MOD")
    menu_role = Text("MNU_ROLE")
    initial_menu = Text("INIT_MNU")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style = Number("FONT_STY")
    font_weight = Number("FONT_WGHT")
    font_spacing = Number("FONT_SPCING")
    foreground_color = Text("FORE_COLOR")
    format_mask = Text("FMT_MSK")
    form_parameters: Subobjects[FormParameter] = Subobjects("FORM_PARAM")
    parameter_data_type = Number("PARAM_DAT_TYP")
    parameter_initial_value = Text("PARAM_INIT_VAL")
    filename = Text("FLNAM")
    execution_mode = Number("EXEC_MODE")
    height = Number("HEIGHT")
    highest_allowed_value = Text("HIGHEST_ALLOWED_VAL")
    hint = Text("HINT")
    show_horizontal_scroll_bar = Bool("SHOW_HORZ_SCRLBR")
    horizontal_toolbar_canvas = Text("HTB_CNV_NAME")
    iconic = Bool("ICONIC")
    minimize_allowed = Bool("MINIMIZE_ALLOWED")
    icon_filename = Text("ICON_FLNAM")
    minimized_title = Text("MINIMIZE_TTL")
    inherit_menu = Bool("INHRT_MNU")
    insert_allowed = Bool("INSRT_ALLOWED")
    items: Subobjects[Item] = Subobjects("ITEM")
    item_type = Number("ITM_TYP")
    copy_value_from_item = Text("COPY_VAL_FROM_ITM")
    data_type = Number("DAT_TYP")
    initial_value = Text("INIT_VAL")
    join_condition = Text("JOIN_COND")
    keep_cursor_position = Bool("KEEP_CRSR_POS")
    key_mode = Number("KEY_MODE")
    label = Text("LABEL")
    prompt_background_color = Text("PRMPT_BACK_COLOR")
    pl_sql_library_location = Text("LIB_LOC")
    pl_sql_library_source = Number("LIB_SRC")
    locking_mode = Number("LOCK_MODE")
    lock_record = Bool("LOCK_REC")
    filter_before_display = Bool("FLTR_BEFORE_DISP")
    lovs: Subobjects[LOV] = Subobjects("LOV")
    list_of_values = Text("LOV_NAM")
    lov_object_pointer: Object[LOV] = Object("LOV_OBJ")
    list_type = Number("LST_TYP")
    validate_from_list = Bool("VALIDATE_FROM_LST")
    list_x_position = Number("LOV_X_POS")
    list_y_position = Number("LOV_Y_POS")
    lowest_allowed_value = Text("LOWEST_ALLOWED_VAL")
    list_style = Number("LST_STY")
    magic_item = Number("MAGIC_ITM")
    main_menu = Text("MAIN_MNU")
    maximum_length = Number("MAX_LEN")
    menus: Subobjects[Menu] = Subobjects("MENU")
    form_horizontal_toolbar_canvas = Text("HORZ_TLBR_CNV")
    form_vertical_toolbar_canvas = Text("VERT_TLBR_CNV")
    menu_directory = Text("MNU_DRCTRY")
    menu_filename = Text("MNU_FLNAM")
    menu_item_object: Object[MenuItem] = Object("MNU_ITM")
    menu_item_type = Number("MNU_ITM_TYP")
    compression_quality = Number("CMPRSSION_QLTY")
    associated_menus: Object[BaseObject] = Object("ASSOC_MNUS")
    menu_item_radio_group = Text("MNU_ITM_RAD_GRP")
    access_key = Text("ACCESS_KEY")
    modal = Bool("MODAL")
    mouse_navigation_limit = Number("MOUSE_NAVIGATION_LMT")
    mouse_navigate = Bool("MOUSE_NAVIGATE")
    move_allowed = Bool("MV_ALLOWED")
    multi_line = Bool("MLT_LIN")
    name = Text("NAME")
    prompt_fill_pattern = Text("PRMPT_FILL_PAT")
    keyboard_navigable = Bool("KBRD_NAVIGABLE")
    navigation_style = Number("NAVIGATION_STY")
    next_object: Object[ColumnValue] = Object("NEXT")
    next_navigation_data_block = Text("NXT_NAVIGATION_BLK_NAM")
    next_data_block_object: Object[DataBlock] = Object("NXT_NAVIGATION_BLK_OBJ")
    next_navigation_item = Text("NXT_NAVIGATION_ITM_NAM")
    next_item_object: Object[BaseObject] = Object("NXT_NAVIGATION_ITM_OBJ")
    object_groups: Subobjects[ObjectGroup] = Subobjects("OBJ_GRP")
    object_group_child_object: Object[ObjectGroup] = Object("OG_CHILD")
    old_lov_text = Text("OLD_LOV_TXT")
    optimizer_hint = Text("OPT_HINT")
    order_by_clause = Text("ORDR_BY_CLAUSE")
    mapping_of_other_values = Text("OTHER_VALS")
    primary_key = Bool("PRMRY_KEY")
    program_units: Subobjects[ProgramUnit] = Subobjects("PROG_UNIT")
    property_classes: Subobjects[PropertyClass] = Subobjects("PROP_CLASS")
    prevent_masterless_operations = Bool("PRVNT_MSTRLESS_OPS")
    previous_navigation_data_block = Text("PREV_NAVIGATION_BLK_NAM")
    previous_data_block_object: Object[DataBlock] = Object("PREV_NAVIGATION_BLK_OBJ")
    previous_navigation_item = Text("PREV_NAVIGATION_ITM_NAM")
    previous_item_object: Object[BaseObject] = Object("PREV_NAVIGATION_ITM_OBJ")
    query_allowed = Bool("QRY_ALLOWED")
    query_length = Number("QRY_LEN")
    query_only = Bool("QRY_ONLY")
    display_quality = Number("DISP_QLTY")
    radio_button_object: Object[RadioButton] = Object("RAD_BUT")
    raise_on_entry = Bool("RAISE_ON_ENT")
    radio_button_value = Text("RDB_VAL")
    reading_order = Number("READING_ORDR")
    number_of_records_buffered = Number("RECS_BUFFERED_COUNT")
    number_of_records_displayed = Number("RECS_DISP_COUNT")
    query_array_size = Number("RECS_FETCHED_COUNT")
    distance_between_records = Number("DIST_BTWN_RECS")
    record_groups: Subobjects[RecordGroup] = Subobjects("REC_GRP")
    record_group = Text("REC_GRP_NAM")
    record_group_object_pointer: Object[RecordGroup] = Object("REC_GRP_OBJ")
    record_group_query = Text("REC_GRP_QRY")
    record_group_type = Number("REC_GRP_TYP")
    record_orientation = Number("REC_ORNT")
    current_record_visual_attribute_group = Text("REC_VAT_GRP_NAM")
    relation_object: Object[Relation] = Object("REL")
    hide_on_exit = Bool("HIDE_ON_EXIT")
    rendered = Bool("RENDERED")
    required = Bool("REQUIRED")
    return_item = Text("RTRN_ITM")
    reverse_direction = Bool("REV_DIR")
    hide_object = Bool("HIDE")
    prompt_font_name = Text("PRMPT_FONT_NAM")
    savepoint_mode = Bool("SVPNT_MODE")
    scroll_bar_canvas = Text("SCRLBR_CNV_NAM")
    scroll_bar_orientation = Number("SCRLBR_ORNT")
    scroll_bar_width = Number("SCRLBR_WID")
    scroll_bar_x_position = Number("SCRLBR_X_POS")
    scroll_bar_y_position = Number("SCRLBR_Y_POS")
    show_scroll_bar = Bool("SHOW_SCRLBR")
    conceal_data = Bool("CONCEAL_DATA")
    display_in_keyboard_help = Bool("DISP_IN_KBRD_HLP")
    sizing_style = Number("SIZING_STY")
    startup_code = Text("STRTUP_CODE")
    sub_title = Text("SUB_TTL")
    tear_off_menu = Bool("TEAR_OFF_MNU")
    title = Text("TITLE")
    prompt_font_size = Number("PRMPT_FONT_SIZ")
    triggers: Subobjects[Trigger] = Subobjects("TRIGGER")
    keyboard_help_text = Text("KBRD_HLP_TXT")
    trigger_style = Number("TRG_STY")
    trigger_text = Text("TRG_TXT")
    value_when_unchecked = Text("UNCHKED_VAL")
    update_allowed = Bool("UPDT_ALLOWED")
    update_changed_columns_only = Bool("UPDT_CHANGED_COLS")
    update_only_if_null = Bool("UPDT_IF_NULL")
    use_3d_controls = Bool("USE_3D_CNTRLS")
    use_security = Bool("USE_SECURITY")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Object[VisualAttribute] = Object("VAT_OBJ")
    prompt_font_style = Number("PRMPT_FONT_STY")
    calculation_mode = Number("CALC_MODE")
    prompt_font_weight = Number("PRMPT_FONT_WGHT")
    prompt_font_spacing = Number("PRMPT_FONT_SPCING")
    column_name = Text("COL_NAM")
    prompt_display_style = Number("PRMPT_DISP_STY")
    show_vertical_scroll_bar = Bool("SHOW_VERT_SCRLBR")
    viewport_height = Number("VPRT_HGT")
    viewport_width = Number("VPRT_WID")
    viewport_x_position_on_canvas = Number("VPRT_X_POS_ON_CNV")
    viewport_y_position_on_canvas = Number("VPRT_Y_POS_ON_CNV")
    visual_attributes: Subobjects[VisualAttribute] = Subobjects("VIS_ATTR")
    validation_unit = Number("VALIDATION_UNIT")
    vertical_toolbar_canvas = Text("VTB_CNV_NAME")
    where_clause = Text("WHERE_CLAUSE")
    width = Number("WIDTH")
    windows: Subobjects[Window] = Subobjects("WINDOW")
    enforce_primary_key = Bool("ENFRC_PRMRY_KEY")
    window = Text("WND_NAM")
    window_object_pointer: Object[Window] = Object("WND_OBJ")
    window_style = Number("WIN_STY")
    primary_canvas = Text("PRMRY_CNV")
    wrap_style = Number("WRAP_STY")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    maximize_allowed = Bool("MAXIMIZE_ALLOWED")
    display_hint_automatically = Bool("AUTO_HINT")
    tooltip = Text("TOOLTIP")
    current_record_va_pointer: Object[VisualAttribute] = Object("REC_VAT_GRP_OBJ")
    graphics_type = Number("GRAPHICS_TYP")
    closed = Bool("CLOSED")
    arrow_style = Number("ARROW_STY")
    x_corner_radius = Number("CORNER_RADIUS_X")
    y_corner_radius = Number("CORNER_RADIUS_Y")
    start_angle = Number("INTERNAL_STRT_ANGLE")
    end_angle = Number("INTERNAL_END_ANGLE")
    prompt = Text("PRMPT")
    prompt_reading_order = Number("PRMPT_READING_ORDR")
    prompt_justification = Number("PRMPT_JST")
    previous_object: Object[ColumnValue] = Object("PREVIOUS")
    prompt_attachment_edge = Number("PRMPT_ATT_EDGE")
    prompt_attachment_offset = Number("PRMPT_ATT_OFST")
    prompt_alignment = Number("PRMPT_ALIGN")
    prompt_alignment_offset = Number("PRMPT_ALIGN_OFST")
    owning_object: Object[BaseObject] = Object("OWNER")
    dither = Bool("DITHER")
    clip_x_position = Number("CLIP_X_POS")
    clip_y_position = Number("CLIP_Y_POS")
    clip_width = Number("CLIP_WID")
    clip_height = Number("CLIP_HGT")
    frame_title_reading_order = Number("TTL_READING_ORDR")
    frame_title_alignment = Number("FRAME_TTL_ALIGN")
    frame_title_offset = Number("FRAME_TTL_OFST")
    frame_title_spacing = Number("FRAME_TTL_SPCING")
    frame_title = Text("FRAME_TTL")
    layout_style = Number("LAYOUT_STY")
    frame_alignment = Number("FRAME_ALIGN")
    single_object_alignment = Number("SNGL_OBJ_ALIGN")
    vertical_fill = Bool("VERT_FILL")
    maximum_objects_per_line = Number("MAX_OBJS")
    allow_expansion = Bool("ALLOW_EXPANSION")
    horizontal_margin = Number("HORZ_MARGN")
    vertical_margin = Number("VERT_MARGN")
    vertical_object_offset = Number("VERT_OBJ_OFST")
    horizontal_object_offset = Number("HORZ_OBJ_OFST")
    start_prompt_offset = Number("STRT_PRMPT_OFST")
    top_prompt_offset = Number("TOP_PRMPT_OFST")
    start_prompt_alignment = Number("STRT_PRMPT_ALIGN")
    top_prompt_alignment = Number("TOP_PRMPT_ALIGN")
    allow_multi_line_prompts = Bool("ALLOW_MLT_LIN_PRMPTS")
    allow_top_attached_prompts = Bool("ALLOW_TOP_ATT_PRMPTS")
    allow_start_attached_prompts = Bool("ALLOW_STRT_ATT_PRMPTS")
    update_layout = Number("UPDT_LAYOUT")
    line_width = Number("INTERNAL_LIN_WID")
    rotation_angle = Number("INTERNAL_ROTATION_ANGLE")
    edge_foreground_color = Text("EDGE_FORE_COLOR")
    edge_background_color = Text("EDGE_BACK_COLOR")
    dash_style = Number("DASH_STY")
    cap_style = Number("CAP_STY")
    join_style = Number("JOIN_STY")
    line_spacing = Number("LIN_SPCING")
    custom_spacing = Number("CSTM_SPCING")
    fixed_bounding_box = Bool("FIXED_BOUNDING_BX")
    wrap_text = Bool("WRAP_TXT")
    bounding_box_scaleable = Bool("BOUNDING_BX_SCALABLE")
    font_scaleable = Bool("FONT_SCALEABLE")
    horizontal_origin = Number("HORZ_ORGN")
    vertical_origin = Number("VERT_ORGN")
    horizontal_justification = Number("HORZ_JST")
    vertical_justification = Number("VERT_JST")
    formula = Text("FORMULA")
    summary_function = Number("SUMM_FUNC")
    summarized_item = Text("SUMM_ITM_NAM")
    number_of_items_displayed = Number("ITMS_DISP")
    scrollbar_canvas_object_pointer: Object[Canvas] = Object("SCRLBR_CNV_OBJ")
    argument_mode = Number("DSA_MODE")
    tab_pages: Subobjects[TabPage] = Subobjects("TAB_PAGE")
    tab_page = Text("TBP_NAM")
    tab_page_name: Object[BaseObject] = Object("TBP_OBJ")
    communication_mode = Number("COMM_MODE")
    data_source_data_block = Text("DAT_SRC_BLK")
    data_source_x_axis = Text("DAT_SRC_X_AXS")
    data_source_y_axis = Text("DAT_SRC_Y_AXS")
    update_on_commit = Bool("UPDT_COMMIT")
    update_on_query = Bool("UPDT_QRY")
    popup_menu = Text("POPUP_MNU_NAM")
    popup_menu_object: Object[BaseObject] = Object("POPUP_MNU_OBJ")
    dml_data_target_name = Text("DML_DAT_NAM")
    query_data_source_name = Text("QRY_DAT_SRC_NAM")
    data_source_column_name = Text("DSC_NAM")
    data_source_column_type = Number("DSC_TYP")
    argument_name = Text("DSA_NAM")
    argument_type = Number("DSA_TYP")
    argument_value = Text("DSA_VAL")
    database_data_block = Bool("DB_BLK")
    query_data_source_type = Number("QRY_DAT_SRC_TYP")
    query_all_records = Bool("QRY_ALL_RECS")
    dml_data_target_type = Number("DML_DAT_TYP")
    dml_array_size = Number("DML_ARY_SIZ")
    tooltip_visual_attribute_group = Text("TOOLTIP_VAT_GRP")
    tooltip_va_object: Object[VisualAttribute] = Object("POPUP_VA_OBJ")
    insert_procedure_name = Text("INSRT_PROC_NAM")
    update_procedure_name = Text("UPDT_PROC_NAM")
    delete_procedure_name = Text("DEL_PROC_NAM")
    lock_procedure_name = Text("LOCK_PROC_NAM")
    single_record = Bool("SNGL_REC")
    trigger_internal_type = Number("TRG_INTERNAL_TYP")
    length = Number("DSC_LEN")
    mandatory = Bool("DSC_MANDATORY")
    precision = Number("DSC_PRECISION")
    scale = Number("DSC_SCALE")
    prompt_va_object: Object[VisualAttribute] = Object("PRMPT_VAT_OBJ")
    prompt_visual_attribute_group = Text("PRMPT_VAT_NAM")
    layout_data_block = Text("LAYOUT_DATA_BLK_NAM")
    owning_module: Object[Module] = Object("MODULE")
    source_object: Object[PropertyClass] = Object("SOURCE")
    scroll_bar_tab_page = Text("SCRLBR_TBP_NAM")
    scrollbar_tab_object: Object[TabPage] = Object("SCRLBR_TBP_OBJ")
    visible_in_vertical_menu_toolbar = Bool("VSBL_IN_VERT_MNU_TLBR")
    visible_in_horizontal_menu_toolbar = Bool("VSBL_IN_HORZ_MNU_TLBR")
    tab_attachment_edge = Number("TAB_ATT_EDGE")
    argument_type_name = Text("DSA_TYP_NAM")
    visible_in_menu = Bool("VSBL_IN_MENU")
    visual_attribute_type = Number("VAT_TYP")
    program_unit_text = Text("PGU_TXT")
    icon_in_menu = Bool("ICON_IN_MNU")
    automatic_position = Bool("AUTO_POS")
    automatic_column_width = Bool("AUTO_COL_WID")
    record_group_fetch_size = Number("REC_GRP_FETCH_SIZ")
    title_va_object: Object[VisualAttribute] = Object("FRAME_TTL_VAT_OBJ")
    frame_title_visual_attribute_group = Text("FRAME_TTL_VAT_NAM")
    frame_title_foreground_color = Text("FRAME_TTL_FORE_COLOR")
    frame_title_background_color = Text("FRAME_TTL_BACK_COLOR")
    frame_title_fill_pattern = Text("FRAME_TTL_FILL_PAT")
    frame_title_font_name = Text("FRAME_TTL_FONT_NAM")
    frame_title_font_size = Number("FRAME_TTL_FONT_SIZ")
    frame_title_font_style = Number("FRAME_TTL_FONT_STY")
    frame_title_font_weight = Number("FRAME_TTL_FONT_WGHT")
    frame_title_font_spacing = Number("FRAME_TTL_FONT_SPCING")
    corner_style = Number("TAB_STY")
    interaction_mode = Number("INTERACTION_MODE")
    maximum_query_time = Number("MAX_QRY_TIME")
    maximum_records_fetched = Number("MAX_RECS_FETCHED")
    isolation_mode = Number("ISOLATION_MODE")
    count_of_data_items_in_the_column = Number("COL_VALS_COUNT")
    real_object_pointed_to_by_the_object_group_child: Object[BaseObject] = Object(
        "OBJ_GRP_CHILD_REAL_OBJ"
    )
    reports: Subobjects[Report] = Subobjects("REPORT")
    count_of_list_element_items = Number("LST_ELEMENT_COUNT")
    precompute_summaries = Bool("PRECOMP_SUMM")
    report_destination_type = Number("RPT_DESTINATION_TYP")
    report_destination_name = Text("RPT_DESTINATION_NAM")
    report_destination_format = Text("RPT_DESTINATION_FMT")
    report_server = Text("RPT_SRVR")
    other_reports_parameters = Text("RPT_PARAMS")
    share_library_with_form = Bool("SHARE_LIB")
    keyboard_state = Number("KBRD_STATE")
    summarized_block = Text("SUMM_BLK_NAM")
    scroll_bar_alignment = Number("SCRLBR_ALIGN")
    shrinkwrap = Bool("SHRINKWRAP")
    graphic_object_font_name = Text("GRA_FONT_NAM")
    graphic_object_font_size = Number("GRA_FONT_SIZ")
    graphic_object_font_style = Number("GRA_FONT_STY")
    graphic_object_text = Text("GRA_TEXT")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    submenu_name = Text("SUB_MNU_NAM")
    submenu_object: Object[BaseObject] = Object("SUB_MNU_OBJ")
    menu_item_code = Text("MNU_ITM_CODE")
    runtime_compatibility_mode = Number("RUNTIME_COMP")
    graphic_font_weight = Number("GRA_FONT_WGHT")
    graphic_font_spacing = Number("GRA_FONT_SPCING")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    scroll_bar_length = Number("SCRLBR_LEN")
    relation_type = Number("REL_TYPE")
    detail_reference_item = Text("DETAIL_ITEMREF")
    column_type_name = Text("DSC_TYPE_NAME")
    parent_column = Text("DSC_PARENT_NAME")
    alias = Text("ALIAS")
    help_book_title = Text("HELP_BOOK_TITLE")
    help_book_topic = Text("HELP_BOOK_TOPIC")
    allow_empty_branches = Bool("TRE_ALLW_EMP_BRANCH")
    multi_selection = Bool("TRE_MULTI_SELECT")
    show_lines = Bool("TRE_SHOW_LINES")
    show_symbols = Bool("TRE_SHOW_SYMBOL")
    tre_record_group = Text("TRE_REC_GRP")
    data_query = Text("TRE_DATA_QRY")
    implementation_class = Text("IMPL_CLASS")
    dml_returning_value = Bool("DML_RET_VAL")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    active_style = Number("TAB_ACT_STY")
    width_style = Number("TAB_WID_STY")
    column_value: Subobjects[ColumnValue] = Subobjects("COLUMN_VALUE")
    defer_required_enforcement = Number("NEWDEFER_REQ_ENF")
    data_length_semantics = Number("DATA_LEN_SEMANTICS")
    event: Subobjects[Event] = Subobjects("EVENT")
    event_type = Number("EVENT_TYPE")
    subscription_name = Text("EVENT_SUBS_NAME")
    scope = Number("EVENT_SCOPE")
    auto_subscribe = Bool("EVENT_ENABLED")
    event_implementation_class = Text("EVENT_IMPLCLASS")
    correlation_id = Text("EVENT_CORRID")
    priority_mode = Number("EVENT_PRIORITY_MODE")
    view_mode = Number("EVENT_VIEW_MODE")
    report_object_type = Number("RPT_OBJECT_TYPE")
    delivery_type = Number("RPT_DEL_TYPE")
    ssl_connection = Number("RPT_SSL_CONN")
    service_location = Text("RPT_SRVC_LOC")
    report_path = Text("RPT_ABS_PATH")
    report_locale = Text("RPT_LOCALE")
    report_format = Text("RPT_OPT_FMT")
    template_name = Text("RPT_TEMPLATE_NAME")
    report_parameters = Text("RPT_BIP_PARAMS")
    ftp_server_name = Text("RPT_FTP_SERVER")
    ftp_user = Text("RPT_FTP_USER")
    ftp_file_name = Text("RPT_FTP_FILENAME")
    secure_ftp = Bool("RPT_FTP_SECURED")
    number = Text("RPT_FAX_NUMBER")
    fax_server_name = Text("RPT_FAX_SERVER")
    to_email = Text("RPT_MAIL_TO")
    from_email = Text("RPT_MAIL_FROM")
    cc_email = Text("RPT_MAIL_CC")
    bcc_email = Text("RPT_MAIL_BCC")
    reply_to = Text("RPT_MAIL_REPLYTO")
    subject = Text("RPT_MAIL_SUBJECT")
    body = Text("RPT_MAIL_BODY")
    mail_server_name = Text("RPT_MAIL_SERVER")
    local_file_name = Text("RPT_LOCAL_FILENAME")
    number_of_copies = Number("RPT_PRINT_NUMBEROFCOPY")
    orientation = Number("RPT_PRINT_ORIENTATION")
    page_range = Text("RPT_PRINT_PAGERANGE")
    side = Number("RPT_PRINT_SIDE")
    tray = Number("RPT_PRINT_TRAY")
    print_server_name = Text("RPT_PRINT_NAME")
    webdav_auth_type = Number("RPT_WEBDAV_AUTHTYPE")
    webdav_user = Text("RPT_WEBDAV_USER")
    webdav_file_path = Text("RPT_WEBDAV_FILE")
    webdav_server_name = Text("RPT_WEBDAV_SERVER")


@forms_object
class Canvas(GenericObject):
    # auto-generated
    object_type = FormsObjects.canvas

    background_color = Text("BACK_COLOR")
    bevel: Constant[Bevel] = Constant("BEVEL", Bevel)
    graphics: ObjectList[Graphic] = Subobjects("GRAPHIC")
    case_info = Unknown("CLIENT_INFO")
    canvas_type: Constant[CanvasType] = Constant("CNV_TYP", CanvasType)
    comments = Text("COMMENT")
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    visible = Bool("VISIBLE")
    display_viewport = Bool("DISP_VIEWPORT")
    viewport_x_position = Number("VPRT_X_POS")
    viewport_y_position = Number("VPRT_Y_POS")
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    show_horizontal_scroll_bar = Bool("SHOW_HORZ_SCRLBR")
    name = Text("NAME")
    next_object: Obj[Canvas] = Object("NEXT")
    raise_on_entry = Bool("RAISE_ON_ENT")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    show_vertical_scroll_bar = Bool("SHOW_VERT_SCRLBR")
    viewport_height = Number("VPRT_HGT")
    viewport_width = Number("VPRT_WID")
    viewport_x_position_on_canvas = Number("VPRT_X_POS_ON_CNV")
    viewport_y_position_on_canvas = Number("VPRT_Y_POS_ON_CNV")
    visual_stat: Obj[VisualState] = Object("VIS_STATE")
    width = Number("WIDTH")
    window = Text("WND_NAM")
    window_object_pointer: Obj[Window] = Object("WND_OBJ")
    previous_object: Obj[Canvas] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    tab_pages: ObjectList[TabPage] = Subobjects("TAB_PAGE")
    popup_menu = Text("POPUP_MNU_NAM")
    popup_menu_object: Obj[BaseObject] = Object("POPUP_MNU_OBJ")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    tab_attachment_edge: Constant[TabAttachmentEdge] = Constant(
        "TAB_ATT_EDGE", TabAttachmentEdge
    )
    corner_style: Constant[CornerStyle] = Constant("TAB_STY", CornerStyle)
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    help_book_topic = Text("HELP_BOOK_TOPIC")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    active_style = Number("TAB_ACT_STY")
    width_style = Number("TAB_WID_STY")
    gradient_start_side = Number("GRADIENT_START")


# todo: todo: undocumented, no .h file
@forms_object
class CompoundText(Any):
    # auto-generated
    object_type = FormsObjects.compound_text


@forms_object
class DataBlock(GenericObject):
    # auto-generated
    object_type = FormsObjects.data_block

    background_color = Text("BACK_COLOR")
    case_info = Unknown("CLIENT_INFO")
    enforce_column_security = Bool("ENFRC_COL_SECURITY")
    comments = Text("COMMENT")
    delete_allowed = Bool("DEL_ALLOWED")
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    fill_pattern = Text("FILL_PAT")
    foreground_color = Text("FORE_COLOR")
    insert_allowed = Bool("INSRT_ALLOWED")
    items: ObjectList[Item] = Subobjects("ITEM")
    key_mode: Constant[KeyMode] = Constant("KEY_MODE", KeyMode)
    locking_mode: Constant[LockingMode] = Constant("LOCK_MODE", LockingMode)
    name = Text("NAME")
    navigation_style: Constant[NavigationStyle] = Constant(
        "NAVIGATION_STY", NavigationStyle
    )
    next_object: Obj[DataBlock] = Object("NEXT")
    next_navigation_data_block = Text("NXT_NAVIGATION_BLK_NAM")
    next_data_block_object: Obj[DataBlock] = Object("NXT_NAVIGATION_BLK_OBJ")
    optimizer_hint = Text("OPT_HINT")
    order_by_clause = Text("ORDR_BY_CLAUSE")
    previous_navigation_data_block = Text("PREV_NAVIGATION_BLK_NAM")
    previous_data_block_object: Obj[DataBlock] = Object("PREV_NAVIGATION_BLK_OBJ")
    query_allowed = Bool("QRY_ALLOWED")
    number_of_records_buffered = Number("RECS_BUFFERED_COUNT")
    number_of_records_displayed = Number("RECS_DISP_COUNT")
    query_array_size = Number("RECS_FETCHED_COUNT")
    record_orientation: Constant[RecordOrientation] = Constant(
        "REC_ORNT", RecordOrientation
    )
    current_record_visual_attribute_group = Text("REC_VAT_GRP_NAM")
    relation_object: Obj[Relation] = Object("REL")
    reverse_direction = Bool("REV_DIR")
    scroll_bar_canvas = Text("SCRLBR_CNV_NAM")
    scroll_bar_orientation: Constant[ScrollBarOrientation] = Constant(
        "SCRLBR_ORNT", ScrollBarOrientation
    )
    scroll_bar_width = Number("SCRLBR_WID")
    scroll_bar_x_position = Number("SCRLBR_X_POS")
    scroll_bar_y_position = Number("SCRLBR_Y_POS")
    show_scroll_bar = Bool("SHOW_SCRLBR")
    triggers: ObjectList[Trigger] = Subobjects("TRIGGER")
    update_allowed = Bool("UPDT_ALLOWED")
    update_changed_columns_only = Bool("UPDT_CHANGED_COLS")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    where_clause = Text("WHERE_CLAUSE")
    enforce_primary_key = Bool("ENFRC_PRMRY_KEY")
    current_record_va_pointer: Obj[VisualAttribute] = Object("REC_VAT_GRP_OBJ")
    previous_object: Obj[DataBlock] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    scrollbar_canvas_object_pointer: Obj[Canvas] = Object("SCRLBR_CNV_OBJ")
    dml_data_target_name = Text("DML_DAT_NAM")
    query_data_source_name = Text("QRY_DAT_SRC_NAM")
    database_data_block = Bool("DB_BLK")
    query_data_source_type: Constant[QueryDataSourceType] = Constant(
        "QRY_DAT_SRC_TYP", QueryDataSourceType
    )
    query_all_records = Bool("QRY_ALL_RECS")
    dml_data_target_type: Constant[DMLDataTargetType] = Constant(
        "DML_DAT_TYP", DMLDataTargetType
    )
    dml_array_size = Number("DML_ARY_SIZ")
    insert_procedure_name = Text("INSRT_PROC_NAM")
    update_procedure_name = Text("UPDT_PROC_NAM")
    delete_procedure_name = Text("DEL_PROC_NAM")
    lock_procedure_name = Text("LOCK_PROC_NAM")
    single_record = Bool("SNGL_REC")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    scroll_bar_tab_page = Text("SCRLBR_TBP_NAM")
    scrollbar_tab_object: Obj[TabPage] = Object("SCRLBR_TBP_OBJ")
    maximum_query_time = Number("MAX_QRY_TIME")
    maximum_records_fetched = Number("MAX_RECS_FETCHED")
    precompute_summaries = Bool("PRECOMP_SUMM")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    query_column_object: Obj[DataSourceColumn] = Object("QRY_DAT_SRC_COL")
    query_argument_object: Obj[DataSourceArgument] = Object("QRY_DAT_SRC_ARG")
    insert_column_object: Obj[DataSourceColumn] = Object("INS_DAT_SRC_COL")
    insert_argument_object: Obj[DataSourceArgument] = Object("INS_DAT_SRC_ARG")
    update_column_object: Obj[DataSourceColumn] = Object("UPD_DAT_SRC_COL")
    update_argument_object: Obj[DataSourceArgument] = Object("UPD_DAT_SRC_ARG")
    delete_column_object: Obj[DataSourceColumn] = Object("DEL_DAT_SRC_COL")
    delete_argument_object: Obj[DataSourceArgument] = Object("DEL_DAT_SRC_ARG")
    lock_column_object: Obj[DataSourceColumn] = Object("LOCK_DAT_SRC_COL")
    lock_argument_object: Obj[DataSourceArgument] = Object("LOCK_DAT_SRC_ARG")
    parent_objects_type = Number("PAR_TYP")
    scroll_bar_length = Number("SCRLBR_LEN")
    alias = Text("ALIAS")
    include_ref_item = Bool("INCLUDE_REFITEM")
    dml_returning_value = Bool("DML_RET_VAL")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    row_banding_frequency = Number("ROW_BANDING_FREQ")


@forms_object
class FormParameter(GenericObject):
    # auto-generated
    object_type = FormsObjects.form_parameter

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    parameter_data_type: Constant[ParameterDataType] = Constant(
        "PARAM_DAT_TYP", ParameterDataType
    )
    parameter_initial_value = Text("PARAM_INIT_VAL")
    name = Text("NAME")
    next_object: Obj[FormParameter] = Object("NEXT")
    previous_object: Obj[FormParameter] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Graphic(GenericObject):
    # auto-generated
    object_type = FormsObjects.graphic

    background_color = Text("BACK_COLOR")
    bevel: Constant[Bevel] = Constant("BEVEL", Bevel)
    graphics: ObjectList[Graphic] = Subobjects("GRAPHIC")
    case_info = Unknown("CLIENT_INFO")
    image_format: Constant[ImageFormat] = Constant("IMG_FMT", ImageFormat)
    image_depth: Constant[ImageDepth] = Constant("IMG_DPTH", ImageDepth)
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    fill_pattern = Text("FILL_PAT")
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    name = Text("NAME")
    next_object: Obj[Graphic] = Object("NEXT")
    display_quality: Constant[DisplayQuality] = Constant("DISP_QLTY", DisplayQuality)
    number_of_records_displayed = Number("RECS_DISP_COUNT")
    distance_between_records = Number("DIST_BTWN_RECS")
    scroll_bar_width = Number("SCRLBR_WID")
    show_scroll_bar = Bool("SHOW_SCRLBR")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    width = Number("WIDTH")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    graphics_type: Constant[GraphicsType] = Constant("GRAPHICS_TYP", GraphicsType)
    closed = Bool("CLOSED")
    arrow_style: Constant[ArrowStyle] = Constant("ARROW_STY", ArrowStyle)
    x_corner_radius = Number("CORNER_RADIUS_X")
    y_corner_radius = Number("CORNER_RADIUS_Y")
    start_angle = Number("INTERNAL_STRT_ANGLE")
    end_angle = Number("INTERNAL_END_ANGLE")
    previous_object: Obj[Graphic] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    dither = Bool("DITHER")
    clip_x_position = Number("CLIP_X_POS")
    clip_y_position = Number("CLIP_Y_POS")
    clip_width = Number("CLIP_WID")
    clip_height = Number("CLIP_HGT")
    points: ObjectList[Point] = Subobjects("POINT")
    frame_title_reading_order: Constant[ReadingOrder] = Constant(
        "TTL_READING_ORDR", ReadingOrder
    )
    frame_title_alignment: Constant[FrameTitleAlignment] = Constant(
        "FRAME_TTL_ALIGN", FrameTitleAlignment
    )
    frame_title_offset = Number("FRAME_TTL_OFST")
    frame_title_spacing = Number("FRAME_TTL_SPCING")
    frame_title = Text("FRAME_TTL")
    layout_style: Constant[LayoutStyle] = Constant("LAYOUT_STY", LayoutStyle)
    frame_alignment: Constant[FrameAlignment] = Constant("FRAME_ALIGN", FrameAlignment)
    single_object_alignment: Constant[SingleObjectAlignment] = Constant(
        "SNGL_OBJ_ALIGN", SingleObjectAlignment
    )
    vertical_fill = Bool("VERT_FILL")
    maximum_objects_per_line = Number("MAX_OBJS")
    allow_expansion = Bool("ALLOW_EXPANSION")
    horizontal_margin = Number("HORZ_MARGN")
    vertical_margin = Number("VERT_MARGN")
    vertical_object_offset = Number("VERT_OBJ_OFST")
    horizontal_object_offset = Number("HORZ_OBJ_OFST")
    start_prompt_offset = Number("STRT_PRMPT_OFST")
    top_prompt_offset = Number("TOP_PRMPT_OFST")
    start_prompt_alignment: Constant[PromptAlignment] = Constant(
        "STRT_PRMPT_ALIGN", PromptAlignment
    )
    top_prompt_alignment: Constant[PromptAlignment] = Constant(
        "TOP_PRMPT_ALIGN", PromptAlignment
    )
    allow_multi_line_prompts = Bool("ALLOW_MLT_LIN_PRMPTS")
    allow_top_attached_prompts = Bool("ALLOW_TOP_ATT_PRMPTS")
    allow_start_attached_prompts = Bool("ALLOW_STRT_ATT_PRMPTS")
    update_layout: Constant[UpdateLayout] = Constant("UPDT_LAYOUT", UpdateLayout)
    line_width = Number("INTERNAL_LIN_WID")
    rotation_angle = Number("INTERNAL_ROTATION_ANGLE")
    edge_foreground_color = Text("EDGE_FORE_COLOR")
    edge_background_color = Text("EDGE_BACK_COLOR")
    edge_pattern = Text("EDGE_PAT")
    dash_style: Constant[DashStyle] = Constant("DASH_STY", DashStyle)
    cap_style: Constant[CapStyle] = Constant("CAP_STY", CapStyle)
    join_style: Constant[JoinStyle] = Constant("JOIN_STY", JoinStyle)
    line_spacing: Constant[LineSpacing] = Constant("LIN_SPCING", LineSpacing)
    custom_spacing = Number("CSTM_SPCING")
    fixed_bounding_box = Bool("FIXED_BOUNDING_BX")
    wrap_text = Bool("WRAP_TXT")
    bounding_box_scaleable = Bool("BOUNDING_BX_SCALABLE")
    font_scaleable = Bool("FONT_SCALEABLE")
    horizontal_origin: Constant[HorizontalOrigin] = Constant(
        "HORZ_ORGN", HorizontalOrigin
    )
    vertical_origin: Constant[VerticalOrigin] = Constant("VERT_ORGN", VerticalOrigin)
    horizontal_justification: Constant[Justification] = Constant(
        "HORZ_JST", Justification
    )
    vertical_justification: Constant[Justification] = Constant(
        "VERT_JST", Justification
    )
    compound_text_object: Obj[CompoundText] = Object("CMPTXT")
    tab_page = Text("TBP_NAM")
    tab_page_name: Obj[BaseObject] = Object("TBP_OBJ")
    layout_data_block = Text("LAYOUT_DATA_BLK_NAM")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    title_va_object: Obj[VisualAttribute] = Object("FRAME_TTL_VAT_OBJ")
    frame_title_visual_attribute_group = Text("FRAME_TTL_VAT_NAM")
    frame_title_foreground_color = Text("FRAME_TTL_FORE_COLOR")
    frame_title_background_color = Text("FRAME_TTL_BACK_COLOR")
    frame_title_fill_pattern = Text("FRAME_TTL_FILL_PAT")
    frame_title_font_name = Text("FRAME_TTL_FONT_NAM")
    frame_title_font_size = Number("FRAME_TTL_FONT_SIZ")
    frame_title_font_style: Constant[FontStyle] = Constant(
        "FRAME_TTL_FONT_STY", FontStyle
    )
    frame_title_font_weight: Constant[FontWeight] = Constant(
        "FRAME_TTL_FONT_WGHT", FontWeight
    )
    frame_title_font_spacing: Constant[FontSpacing] = Constant(
        "FRAME_TTL_FONT_SPCING", FontSpacing
    )
    scroll_bar_alignment: Constant[ScrollBarAlignment] = Constant(
        "SCRLBR_ALIGN", ScrollBarAlignment
    )
    shrinkwrap = Bool("SHRINKWRAP")
    graphic_object_font_name = Text("GRA_FONT_NAM")
    graphic_object_font_size = Number("GRA_FONT_SIZ")
    graphic_object_font_style: Constant[FontStyle] = Constant("GRA_FONT_STY", FontStyle)
    graphic_object_text = Text("GRA_TEXT")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    graphic_font_weight: Constant[FontWeight] = Constant("GRA_FONT_WGHT", FontWeight)
    graphic_font_spacing: Constant[FontSpacing] = Constant(
        "GRA_FONT_SPCING", FontSpacing
    )
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Item(GenericObject):
    # auto-generated
    object_type = FormsObjects.item

    justification: Constant[Justification] = Constant("JUSTIFICATION", Justification)
    automatic_skip = Bool("AUTO_SKP")
    background_color = Text("BACK_COLOR")
    database_item = Bool("DB_ITM")
    bevel: Constant[Bevel] = Constant("BEVEL", Bevel)
    mirror_item_object: Obj[BaseObject] = Object("SYNC_ITM_OBJ")
    canvas = Text("CNV_NAM")
    canvas_object_pointer: Obj[Canvas] = Object("CNV_OBJ")
    case_info = Unknown("CLIENT_INFO")
    case_insensitive_query = Bool("CASE_INSENSITIVE_QRY")
    case_restriction: Constant[CaseRestriction] = Constant(
        "CASE_RSTRCTION", CaseRestriction
    )
    check_box_mapping_of_other_values: Constant[
        CheckBoxMappingofOtherValues
    ] = Constant("CHK_BX_OTHER_VALS", CheckBoxMappingofOtherValues)
    value_when_checked = Text("CHKED_VAL")
    synchronize_with_item = Text("SYNC_ITM_NAM")
    comments = Text("COMMENT")
    image_format: Constant[ImageFormat] = Constant("IMG_FMT", ImageFormat)
    image_depth: Constant[ImageDepth] = Constant("IMG_DPTH", ImageDepth)
    prompt_foreground_color = Text("PRMPT_FORE_COLOR")
    default_button = Bool("DFLT_BTN")
    initial_keyboard_state: Constant[InitialKeyboardState] = Constant(
        "INIT_KBRD_DIR", InitialKeyboardState
    )
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    visible = Bool("VISIBLE")
    editor = Text("EDT_NAM")
    editor_object_pointer: Obj[Editor] = Object("EDT_OBJ")
    editor_x_position = Number("EDT_X_POS")
    editor_y_position = Number("EDT_Y_POS")
    enabled = Bool("ENABLED")
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    format_mask = Text("FMT_MSK")
    filename = Text("FLNAM")
    execution_mode: Constant[ExecutionMode] = Constant("EXEC_MODE", ExecutionMode)
    height = Number("HEIGHT")
    highest_allowed_value = Text("HIGHEST_ALLOWED_VAL")
    hint = Text("HINT")
    show_horizontal_scroll_bar = Bool("SHOW_HORZ_SCRLBR")
    iconic = Bool("ICONIC")
    icon_filename = Text("ICON_FLNAM")
    insert_allowed = Bool("INSRT_ALLOWED")
    item_type: Constant[ItemType] = Constant("ITM_TYP", ItemType)
    copy_value_from_item = Text("COPY_VAL_FROM_ITM")
    data_type: Constant[DataType] = Constant("DAT_TYP", DataType)
    initial_value = Text("INIT_VAL")
    keep_cursor_position = Bool("KEEP_CRSR_POS")
    label = Text("LABEL")
    prompt_background_color = Text("PRMPT_BACK_COLOR")
    lock_record = Bool("LOCK_REC")
    list_of_values = Text("LOV_NAM")
    lov_object_pointer: Obj[LOV] = Object("LOV_OBJ")
    validate_from_list = Bool("VALIDATE_FROM_LST")
    list_x_position = Number("LOV_X_POS")
    list_y_position = Number("LOV_Y_POS")
    lowest_allowed_value = Text("LOWEST_ALLOWED_VAL")
    list_style: Constant[ListStyle] = Constant("LST_STY", ListStyle)
    maximum_length = Number("MAX_LEN")
    compression_quality: Constant[CompressionQuality] = Constant(
        "CMPRSSION_QLTY", CompressionQuality
    )
    access_key = Text("ACCESS_KEY")
    mouse_navigate = Bool("MOUSE_NAVIGATE")
    multi_line = Bool("MLT_LIN")
    name = Text("NAME")
    prompt_fill_pattern = Text("PRMPT_FILL_PAT")
    keyboard_navigable = Bool("KBRD_NAVIGABLE")
    next_object: Obj[Item] = Object("NEXT")
    next_navigation_item = Text("NXT_NAVIGATION_ITM_NAM")
    next_item_object: Obj[BaseObject] = Object("NXT_NAVIGATION_ITM_OBJ")
    mapping_of_other_values = Text("OTHER_VALS")
    primary_key = Bool("PRMRY_KEY")
    previous_navigation_item = Text("PREV_NAVIGATION_ITM_NAM")
    previous_item_object: Obj[BaseObject] = Object("PREV_NAVIGATION_ITM_OBJ")
    query_allowed = Bool("QRY_ALLOWED")
    query_length = Number("QRY_LEN")
    query_only = Bool("QRY_ONLY")
    display_quality: Constant[DisplayQuality] = Constant("DISP_QLTY", DisplayQuality)
    radio_button_object: Obj[RadioButton] = Object("RAD_BUT")
    reading_order: Constant[ReadingOrder] = Constant("READING_ORDR", ReadingOrder)
    distance_between_records = Number("DIST_BTWN_RECS")
    record_group = Text("REC_GRP_NAM")
    record_group_object_pointer: Obj[RecordGroup] = Object("REC_GRP_OBJ")
    current_record_visual_attribute_group = Text("REC_VAT_GRP_NAM")
    rendered = Bool("RENDERED")
    required = Bool("REQUIRED")
    prompt_font_name = Text("PRMPT_FONT_NAM")
    conceal_data = Bool("CONCEAL_DATA")
    sizing_style: Constant[SizingStyle] = Constant("SIZING_STY", SizingStyle)
    prompt_font_size = Number("PRMPT_FONT_SIZ")
    triggers: ObjectList[Trigger] = Subobjects("TRIGGER")
    value_when_unchecked = Text("UNCHKED_VAL")
    update_allowed = Bool("UPDT_ALLOWED")
    update_only_if_null = Bool("UPDT_IF_NULL")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    prompt_font_style: Constant[FontStyle] = Constant("PRMPT_FONT_STY", FontStyle)
    calculation_mode: Constant[CalculationMode] = Constant("CALC_MODE", CalculationMode)
    prompt_font_weight: Constant[FontWeight] = Constant("PRMPT_FONT_WGHT", FontWeight)
    prompt_font_spacing: Constant[FontSpacing] = Constant(
        "PRMPT_FONT_SPCING", FontSpacing
    )
    column_name = Text("COL_NAM")
    prompt_display_style: Constant[PromptDisplayStyle] = Constant(
        "PRMPT_DISP_STY", PromptDisplayStyle
    )
    show_vertical_scroll_bar = Bool("SHOW_VERT_SCRLBR")
    width = Number("WIDTH")
    wrap_style: Constant[WrapStyle] = Constant("WRAP_STY", WrapStyle)
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    display_hint_automatically = Bool("AUTO_HINT")
    tooltip = Text("TOOLTIP")
    current_record_va_pointer: Obj[VisualAttribute] = Object("REC_VAT_GRP_OBJ")
    prompt = Text("PRMPT")
    prompt_reading_order: Constant[ReadingOrder] = Constant(
        "PRMPT_READING_ORDR", ReadingOrder
    )
    prompt_justification: Constant[Justification] = Constant("PRMPT_JST", Justification)
    previous_object: Obj[Item] = Object("PREVIOUS")
    prompt_attachment_edge: Constant[PromptAttachmentEdge] = Constant(
        "PRMPT_ATT_EDGE", PromptAttachmentEdge
    )
    prompt_attachment_offset = Number("PRMPT_ATT_OFST")
    prompt_alignment: Constant[PromptAlignment] = Constant(
        "PRMPT_ALIGN", PromptAlignment
    )
    prompt_alignment_offset: Constant[PromptAlignment] = Constant(
        "PRMPT_ALIGN_OFST", PromptAlignment
    )
    owning_object: Obj[BaseObject] = Object("OWNER")
    formula = Text("FORMULA")
    summary_function: Constant[SummaryFunction] = Constant("SUMM_FUNC", SummaryFunction)
    summarized_item = Text("SUMM_ITM_NAM")
    number_of_items_displayed = Number("ITMS_DISP")
    tab_page = Text("TBP_NAM")
    tab_page_name: Obj[BaseObject] = Object("TBP_OBJ")
    communication_mode: Constant[CommunicationMode] = Constant(
        "COMM_MODE", CommunicationMode
    )
    data_source_data_block = Text("DAT_SRC_BLK")
    data_source_x_axis = Text("DAT_SRC_X_AXS")
    data_source_y_axis = Text("DAT_SRC_Y_AXS")
    update_on_commit = Bool("UPDT_COMMIT")
    update_on_query = Bool("UPDT_QRY")
    query_name = Text("QUERY_NAME")
    popup_menu = Text("POPUP_MNU_NAM")
    popup_menu_object: Obj[BaseObject] = Object("POPUP_MNU_OBJ")
    tooltip_visual_attribute_group = Text("TOOLTIP_VAT_GRP")
    tooltip_va_object: Obj[VisualAttribute] = Object("POPUP_VA_OBJ")
    prompt_va_object: Obj[VisualAttribute] = Object("PRMPT_VAT_OBJ")
    prompt_visual_attribute_group = Text("PRMPT_VAT_NAM")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    count_of_list_element_items = Number("LST_ELEMENT_COUNT")
    keyboard_state: Constant[KeyboardState] = Constant("KBRD_STATE", KeyboardState)
    summarized_block = Text("SUMM_BLK_NAM")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    help_book_topic = Text("HELP_BOOK_TOPIC")
    allow_empty_branches = Bool("TRE_ALLW_EMP_BRANCH")
    multi_selection = Bool("TRE_MULTI_SELECT")
    show_lines = Bool("TRE_SHOW_LINES")
    show_symbols = Bool("TRE_SHOW_SYMBOL")
    data_query = Text("TRE_DATA_QRY")
    implementation_class = Text("IMPL_CLASS")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    data_length_semantics: Constant[DataLengthSemantics] = Constant(
        "DATA_LEN_SEMANTICS", DataLengthSemantics
    )
    row_banding_frequency = Number("ROW_BANDING_FREQ")
    cursor_style = Number("CURSOR_STYLE")


@forms_object
class Point(GenericObject):
    # auto-generated
    object_type = FormsObjects.point

    name = Text("NAME")
    next_object: Obj[Point] = Object("NEXT")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    previous_object: Obj[Point] = Object("PREVIOUS")


@forms_object
class ProgramUnit(GenericObject):
    # auto-generated
    object_type = FormsObjects.program_unit

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    name = Text("NAME")
    next_object: Obj[ProgramUnit] = Object("NEXT")
    previous_object: Obj[ProgramUnit] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    program_unit_text = Text("PGU_TXT")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    program_unit_type: Constant[ProgramUnitType] = Constant("PGU_TYP", ProgramUnitType)
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class PropertyClass(GenericObject):
    # auto-generated
    object_type = FormsObjects.property_class

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    name = Text("NAME")
    next_object: Obj[PropertyClass] = Object("NEXT")
    triggers: ObjectList[Trigger] = Subobjects("TRIGGER")
    previous_object: Obj[PropertyClass] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class RadioButton(GenericObject):
    # auto-generated
    object_type = FormsObjects.radio_button

    background_color = Text("BACK_COLOR")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    prompt_foreground_color = Text("PRMPT_FORE_COLOR")
    visible = Bool("VISIBLE")
    enabled = Bool("ENABLED")
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    label = Text("LABEL")
    prompt_background_color = Text("PRMPT_BACK_COLOR")
    access_key = Text("ACCESS_KEY")
    name = Text("NAME")
    prompt_fill_pattern = Text("PRMPT_FILL_PAT")
    next_object: Obj[RadioButton] = Object("NEXT")
    radio_button_value = Text("RDB_VAL")
    distance_between_records = Number("DIST_BTWN_RECS")
    prompt_font_name = Text("PRMPT_FONT_NAM")
    prompt_font_size = Number("PRMPT_FONT_SIZ")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    prompt_font_style: Constant[FontStyle] = Constant("PRMPT_FONT_STY", FontStyle)
    prompt_font_weight: Constant[FontWeight] = Constant("PRMPT_FONT_WGHT", FontWeight)
    prompt_font_spacing: Constant[FontSpacing] = Constant(
        "PRMPT_FONT_SPCING", FontSpacing
    )
    prompt_display_style: Constant[PromptDisplayStyle] = Constant(
        "PRMPT_DISP_STY", PromptDisplayStyle
    )
    width = Number("WIDTH")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    prompt = Text("PRMPT")
    prompt_reading_order: Constant[ReadingOrder] = Constant(
        "PRMPT_READING_ORDR", ReadingOrder
    )
    prompt_justification: Constant[Justification] = Constant("PRMPT_JST", Justification)
    previous_object: Obj[RadioButton] = Object("PREVIOUS")
    prompt_attachment_edge: Constant[PromptAttachmentEdge] = Constant(
        "PRMPT_ATT_EDGE", PromptAttachmentEdge
    )
    prompt_attachment_offset = Number("PRMPT_ATT_OFST")
    prompt_alignment: Constant[PromptAlignment] = Constant(
        "PRMPT_ALIGN", PromptAlignment
    )
    prompt_alignment_offset: Constant[PromptAlignment] = Constant(
        "PRMPT_ALIGN_OFST", PromptAlignment
    )
    owning_object: Obj[BaseObject] = Object("OWNER")
    prompt_va_object: Obj[VisualAttribute] = Object("PRMPT_VAT_OBJ")
    prompt_visual_attribute_group = Text("PRMPT_VAT_NAM")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_second_level_owners_name = Text("PAR_SL2OBJ_NAM")
    parent_objects_second_level_owners_type = Number("PAR_SL2OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Relation(GenericObject):
    # auto-generated
    object_type = FormsObjects.relation

    automatic_query = Bool("AUTO_QRY")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    deferred = Bool("DEFERRED")
    delete_record_behavior: Constant[DeleteRecordBehavior] = Constant(
        "DEL_REC", DeleteRecordBehavior
    )
    detail_data_block = Text("DETAIL_BLK")
    join_condition = Text("JOIN_COND")
    name = Text("NAME")
    next_object: Obj[Relation] = Object("NEXT")
    prevent_masterless_operations = Bool("PRVNT_MSTRLESS_OPS")
    previous_object: Obj[Relation] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    relation_type: Constant[RelationType] = Constant("REL_TYPE", RelationType)
    detail_reference_item = Text("DETAIL_ITEMREF")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class TabPage(GenericObject):
    # auto-generated
    object_type = FormsObjects.tab_page

    background_color = Text("BACK_COLOR")
    graphics: ObjectList[Graphic] = Subobjects("GRAPHIC")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    visible = Bool("VISIBLE")
    enabled = Bool("ENABLED")
    fill_pattern = Text("FILL_PAT")
    foreground_color = Text("FORE_COLOR")
    icon_filename = Text("ICON_FLNAM")
    label = Text("LABEL")
    name = Text("NAME")
    next_object: Obj[TabPage] = Object("NEXT")
    visual_attribute_group = Text("VAT_NAM")
    previous_object: Obj[TabPage] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    gradient_start_side = Number("GRADIENT_START")


@forms_object
class Trigger(GenericObject):
    # auto-generated
    object_type = FormsObjects.trigger

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    execution_hierarchy: Constant[ExecutionHierarchy] = Constant(
        "EXEC_HIERARCHY", ExecutionHierarchy
    )
    fire_in_enter_query_mode = Bool("FIRE_IN_QRY")
    name = Text("NAME")
    next_object: Obj[Trigger] = Object("NEXT")
    hide_object = Bool("HIDE")
    display_in_keyboard_help = Bool("DISP_IN_KBRD_HLP")
    keyboard_help_text = Text("KBRD_HLP_TXT")
    trigger_step_object: Obj[BaseObject] = Object("TRIG_STEP")
    trigger_style: Constant[TriggerStyle] = Constant("TRG_STY", TriggerStyle)
    trigger_text = Text("TRG_TXT")
    previous_object: Obj[Trigger] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    trigger_internal_type = Number("TRG_INTERNAL_TYP")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_second_level_owners_name = Text("PAR_SL2OBJ_NAM")
    parent_objects_second_level_owners_type = Number("PAR_SL2OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


# todo: todo: undocumented, no .h file
@forms_object
class VisualAttribute(GenericObject):
    # auto-generated
    object_type = FormsObjects.visual_attribute

    background_color = Text("BACK_COLOR")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    prompt_foreground_color = Text("PRMPT_FORE_COLOR")
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    prompt_background_color = Text("PRMPT_BACK_COLOR")
    name = Text("NAME")
    prompt_fill_pattern = Text("PRMPT_FILL_PAT")
    next_object: Obj[VisualAttribute] = Object("NEXT")
    prompt_font_name = Text("PRMPT_FONT_NAM")
    prompt_font_size = Number("PRMPT_FONT_SIZ")
    prompt_font_style: Constant[FontStyle] = Constant("PRMPT_FONT_STY", FontStyle)
    prompt_font_weight: Constant[FontWeight] = Constant("PRMPT_FONT_WGHT", FontWeight)
    prompt_font_spacing: Constant[FontSpacing] = Constant(
        "PRMPT_FONT_SPCING", FontSpacing
    )
    previous_object: Obj[VisualAttribute] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    visual_attribute_type: Constant[VisualAttributeType] = Constant(
        "VAT_TYP", VisualAttributeType
    )
    frame_title_foreground_color = Text("FRAME_TTL_FORE_COLOR")
    frame_title_background_color = Text("FRAME_TTL_BACK_COLOR")
    frame_title_fill_pattern = Text("FRAME_TTL_FILL_PAT")
    frame_title_font_name = Text("FRAME_TTL_FONT_NAM")
    frame_title_font_size = Number("FRAME_TTL_FONT_SIZ")
    frame_title_font_style: Constant[FontStyle] = Constant(
        "FRAME_TTL_FONT_STY", FontStyle
    )
    frame_title_font_weight: Constant[FontWeight] = Constant(
        "FRAME_TTL_FONT_WGHT", FontWeight
    )
    frame_title_font_spacing: Constant[FontSpacing] = Constant(
        "FRAME_TTL_FONT_SPCING", FontSpacing
    )
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class VisualState(Any):
    # auto-generated
    object_type = FormsObjects.visual_state


@forms_object
class Window(GenericObject):
    # auto-generated
    object_type = FormsObjects.window

    background_color = Text("BACK_COLOR")
    bevel: Constant[Bevel] = Constant("BEVEL", Bevel)
    case_info = Unknown("CLIENT_INFO")
    close_allowed = Bool("CLS_ALLOWED")
    comments = Text("COMMENT")
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    fill_pattern = Text("FILL_PAT")
    resize_allowed = Bool("RESIZE_ALLOWED")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    show_horizontal_scroll_bar = Bool("SHOW_HORZ_SCRLBR")
    horizontal_toolbar_canvas = Text("HTB_CNV_NAME")
    minimize_allowed = Bool("MINIMIZE_ALLOWED")
    icon_filename = Text("ICON_FLNAM")
    minimized_title = Text("MINIMIZE_TTL")
    inherit_menu = Bool("INHRT_MNU")
    modal = Bool("MODAL")
    move_allowed = Bool("MV_ALLOWED")
    name = Text("NAME")
    next_object: Obj[Window] = Object("NEXT")
    hide_on_exit = Bool("HIDE_ON_EXIT")
    title = Text("TITLE")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    show_vertical_scroll_bar = Bool("SHOW_VERT_SCRLBR")
    vertical_toolbar_canvas = Text("VTB_CNV_NAME")
    width = Number("WIDTH")
    window_style: Constant[WindowStyle] = Constant("WIN_STY", WindowStyle)
    primary_canvas = Text("PRMRY_CNV")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    maximize_allowed = Bool("MAXIMIZE_ALLOWED")
    previous_object: Obj[Window] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    help_book_topic = Text("HELP_BOOK_TOPIC")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


# todo: this is special, has own create functions in C
@forms_object
class DataSourceArgument(GenericObject):
    # auto-generated
    object_type = FormsObjects.data_source_argument

    case_info = Unknown("CLIENT_INFO")
    next_object: Obj[DataSourceArgument] = Object("NEXT")
    previous_object: Obj[DataSourceArgument] = Object("PREVIOUS")
    argument_mode: Constant[ArgumentMode] = Constant("DSA_MODE", ArgumentMode)
    argument_name = Text("DSA_NAM")
    argument_type: Constant[ArgumentType] = Constant("DSA_TYP", ArgumentType)
    argument_value = Text("DSA_VAL")
    argument_type_name = Text("DSA_TYP_NAM")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


# todo: this is special, has own create functions in C
@forms_object
class DataSourceColumn(GenericObject):
    # auto-generated
    object_type = FormsObjects.data_source_column

    case_info = Unknown("CLIENT_INFO")
    next_object: Obj[DataSourceColumn] = Object("NEXT")
    previous_object: Obj[DataSourceColumn] = Object("PREVIOUS")
    data_source_column_name = Text("DSC_NAM")
    data_source_column_type: Constant[ColumnType] = Constant("DSC_TYP", ColumnType)
    length = Number("DSC_LEN")
    mandatory = Bool("DSC_MANDATORY")
    precision = Number("DSC_PRECISION")
    scale = Number("DSC_SCALE")
    column_type_name = Text("DSC_TYPE_NAME")
    parent_column = Text("DSC_PARENT_NAME")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Editor(GenericObject):
    # auto-generated
    object_type = FormsObjects.editor

    background_color = Text("BACK_COLOR")
    bottom_title = Text("BTM_TTL")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    show_horizontal_scroll_bar = Bool("SHOW_HORZ_SCRLBR")
    name = Text("NAME")
    next_object: Obj[Editor] = Object("NEXT")
    title = Text("TITLE")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    show_vertical_scroll_bar = Bool("SHOW_VERT_SCRLBR")
    width = Number("WIDTH")
    wrap_style: Constant[WrapStyle] = Constant("WRAP_STY", WrapStyle)
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    previous_object: Obj[Editor] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class LOV(GenericObject):
    # auto-generated
    object_type = FormsObjects.lov

    automatic_select = Bool("AUTO_SLCT")
    automatic_display = Bool("AUTO_DISP")
    automatic_refresh = Bool("AUTO_RFRSH")
    automatic_skip = Bool("AUTO_SKP")
    background_color = Text("BACK_COLOR")
    case_info = Unknown("CLIENT_INFO")
    column_mapping_object: Obj[LOVColumnMap] = Object("COL_MAP")
    comments = Text("COMMENT")
    direction: Constant[Direction] = Constant("LANG_DIR", Direction)
    fill_pattern = Text("FILL_PAT")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    foreground_color = Text("FORE_COLOR")
    height = Number("HEIGHT")
    filter_before_display = Bool("FLTR_BEFORE_DISP")
    list_type: Constant[ListType] = Constant("LST_TYP", ListType)
    name = Text("NAME")
    next_object: Obj[LOV] = Object("NEXT")
    old_lov_text = Text("OLD_LOV_TXT")
    record_group = Text("REC_GRP_NAM")
    record_group_object_pointer: Obj[RecordGroup] = Object("REC_GRP_OBJ")
    title = Text("TITLE")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    width = Number("WIDTH")
    x_position = Number("X_POS")
    y_position = Number("Y_POS")
    previous_object: Obj[LOV] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    automatic_position = Bool("AUTO_POS")
    automatic_column_width = Bool("AUTO_COL_WID")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class LOVColumnMap(GenericObject):
    # auto-generated
    object_type = FormsObjects.lov_column_map

    case_info = Unknown("CLIENT_INFO")
    display_width = Number("DISP_WID")
    name = Text("NAME")
    next_object: Obj[LOVColumnMap] = Object("NEXT")
    return_item = Text("RTRN_ITM")
    title = Text("TITLE")
    previous_object: Obj[LOVColumnMap] = Object("PREVIOUS")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class Menu(GenericObject):
    # auto-generated
    object_type = FormsObjects.menu

    bottom_title = Text("BTM_TTL")
    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    menu_item_object: Obj[MenuItem] = Object("MNU_ITM")
    name = Text("NAME")
    next_object: Obj[Menu] = Object("NEXT")
    sub_title = Text("SUB_TTL")
    tear_off_menu = Bool("TEAR_OFF_MNU")
    title = Text("TITLE")
    previous_object: Obj[Menu] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class MenuItem(GenericObject):
    # auto-generated
    object_type = FormsObjects.menu_item

    keyboard_accelerator = Text("KBRD_ACC")
    case_info = Unknown("CLIENT_INFO")
    command_text = Text("COM_TXT")
    command_type: Constant[CommandType] = Constant("COM_TYP", CommandType)
    comments = Text("COMMENT")
    visible = Bool("VISIBLE")
    display_without_privilege = Bool("DISP_NO_PRIV")
    enabled = Bool("ENABLED")
    font_name = Text("FONT_NAM")
    font_size = Number("FONT_SIZ")
    font_style: Constant[FontStyle] = Constant("FONT_STY", FontStyle)
    font_weight: Constant[FontWeight] = Constant("FONT_WGHT", FontWeight)
    font_spacing: Constant[FontSpacing] = Constant("FONT_SPCING", FontSpacing)
    hint = Text("HINT")
    icon_filename = Text("ICON_FLNAM")
    label = Text("LABEL")
    magic_item: Constant[MagicItem] = Constant("MAGIC_ITM", MagicItem)
    menu_item_type: Constant[ItemType] = Constant("MNU_ITM_TYP", ItemType)
    menu_item_radio_group = Text("MNU_ITM_RAD_GRP")
    name = Text("NAME")
    next_object: Obj[MenuItem] = Object("NEXT")
    visual_attribute_group = Text("VAT_NAM")
    va_object: Obj[VisualAttribute] = Object("VAT_OBJ")
    previous_object: Obj[MenuItem] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    visible_in_vertical_menu_toolbar = Bool("VSBL_IN_VERT_MNU_TLBR")
    visible_in_horizontal_menu_toolbar = Bool("VSBL_IN_HORZ_MNU_TLBR")
    visible_in_menu = Bool("VSBL_IN_MENU")
    icon_in_menu = Bool("ICON_IN_MNU")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    count_of_roles = Number("ROLE_COUNT")
    submenu_name = Text("SUB_MNU_NAM")
    submenu_object: Obj[BaseObject] = Object("SUB_MNU_OBJ")
    menu_item_code = Text("MNU_ITM_CODE")
    parent_objects_first_level_owners_name = Text("PAR_SL1OBJ_NAM")
    parent_objects_first_level_owners_type = Number("PAR_SL1OBJ_TYP")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class ObjectGroup(GenericObject):
    # auto-generated
    object_type = FormsObjects.object_group

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    name = Text("NAME")
    next_object: Obj[ObjectGroup] = Object("NEXT")
    object_group_child_object: Obj[ObjectGroup] = Object("OG_CHILD")
    previous_object: Obj[ObjectGroup] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    object_group_type = Number("OBJ_GRP_TYP")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class ObjectChild(GenericObject):
    # auto-generated
    object_type = FormsObjects.object_child

    case_info = Unknown("CLIENT_INFO")
    name = Text("NAME")
    next_object: Obj[ObjectChild] = Object("NEXT")
    previous_object: Obj[ObjectChild] = Object("PREVIOUS")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    real_object_pointed_to_by_the_object_group_child: Obj[BaseObject] = Object(
        "OBJ_GRP_CHILD_REAL_OBJ"
    )
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class RecordGroup(GenericObject):
    # auto-generated
    object_type = FormsObjects.record_group

    case_info = Unknown("CLIENT_INFO")
    record_group_colspecs: ObjectList[RecordGroupColspec] = Subobjects("COL_SPEC")
    comments = Text("COMMENT")
    name = Text("NAME")
    next_object: Obj[RecordGroup] = Object("NEXT")
    record_group_query = Text("REC_GRP_QRY")
    record_group_type: Constant[RecordGroupType] = Constant(
        "REC_GRP_TYP", RecordGroupType
    )
    previous_object: Obj[RecordGroup] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    record_group_fetch_size = Number("REC_GRP_FETCH_SIZ")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")


@forms_object
class RecordGroupColspec(GenericObject):
    # auto-generated
    object_type = FormsObjects.record_group_colspec

    case_info = Unknown("CLIENT_INFO")
    column_data_type: Constant[ColumnDataType] = Constant("COL_DAT_TYP", ColumnDataType)
    maximum_length = Number("MAX_LEN")
    name = Text("NAME")
    next_object: Obj[RecordGroupColspec] = Object("NEXT")
    previous_object: Obj[RecordGroupColspec] = Object("PREVIOUS")
    count_of_data_items_in_the_column = Number("COL_VALS_COUNT")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    column_value: ObjectList[ColumnValue] = Subobjects("COLUMN_VALUE")
    data_length_semantics: Constant[DataLengthSemantics] = Constant(
        "DATA_LEN_SEMANTICS", DataLengthSemantics
    )


@forms_object
class Report(GenericObject):
    # auto-generated
    object_type = FormsObjects.report

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    filename = Text("FLNAM")
    execution_mode: Constant[ExecutionMode] = Constant("EXEC_MODE", ExecutionMode)
    name = Text("NAME")
    next_object: Obj[Report] = Object("NEXT")
    previous_object: Obj[Report] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    communication_mode: Constant[CommunicationMode] = Constant(
        "COMM_MODE", CommunicationMode
    )
    data_source_data_block = Text("DAT_SRC_BLK")
    query_name = Text("QUERY_NAME")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    report_destination_type: Constant[ReportDestinationType] = Constant(
        "RPT_DESTINATION_TYP", ReportDestinationType
    )
    report_destination_name = Text("RPT_DESTINATION_NAM")
    report_destination_format = Text("RPT_DESTINATION_FMT")
    report_server = Text("RPT_SRVR")
    other_reports_parameters = Text("RPT_PARAMS")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    report_object_type = Number("RPT_OBJECT_TYPE")
    delivery_type = Number("RPT_DEL_TYPE")
    ssl_connection = Number("RPT_SSL_CONN")
    service_location = Text("RPT_SRVC_LOC")
    report_path = Text("RPT_ABS_PATH")
    report_locale = Text("RPT_LOCALE")
    report_format = Text("RPT_OPT_FMT")
    template_name = Text("RPT_TEMPLATE_NAME")
    report_parameters = Text("RPT_BIP_PARAMS")
    ftp_server_name = Text("RPT_FTP_SERVER")
    ftp_user = Text("RPT_FTP_USER")
    ftp_file_name = Text("RPT_FTP_FILENAME")
    secure_ftp = Bool("RPT_FTP_SECURED")
    number = Text("RPT_FAX_NUMBER")
    fax_server_name = Text("RPT_FAX_SERVER")
    to_email = Text("RPT_MAIL_TO")
    from_email = Text("RPT_MAIL_FROM")
    cc_email = Text("RPT_MAIL_CC")
    bcc_email = Text("RPT_MAIL_BCC")
    reply_to = Text("RPT_MAIL_REPLYTO")
    subject = Text("RPT_MAIL_SUBJECT")
    body = Text("RPT_MAIL_BODY")
    mail_server_name = Text("RPT_MAIL_SERVER")
    local_file_name = Text("RPT_LOCAL_FILENAME")
    number_of_copies = Number("RPT_PRINT_NUMBEROFCOPY")
    orientation = Number("RPT_PRINT_ORIENTATION")
    page_range = Text("RPT_PRINT_PAGERANGE")
    side = Number("RPT_PRINT_SIDE")
    tray = Number("RPT_PRINT_TRAY")
    print_server_name = Text("RPT_PRINT_NAME")
    webdav_auth_type = Number("RPT_WEBDAV_AUTHTYPE")
    webdav_user = Text("RPT_WEBDAV_USER")
    webdav_file_path = Text("RPT_WEBDAV_FILE")
    webdav_server_name = Text("RPT_WEBDAV_SERVER")


@forms_object
class Event(GenericObject):
    # auto-generated
    object_type = FormsObjects.event

    case_info = Unknown("CLIENT_INFO")
    comments = Text("COMMENT")
    name = Text("NAME")
    next_object: Obj[Event] = Object("NEXT")
    triggers: ObjectList[Trigger] = Subobjects("TRIGGER")
    previous_object: Obj[Event] = Object("PREVIOUS")
    owning_object: Obj[BaseObject] = Object("OWNER")
    owning_module: Obj[Module] = Object("MODULE")
    source_object: Obj[PropertyClass] = Object("SOURCE")
    parent_objects_module = Text("PAR_MODULE")
    parent_objects_module_type = Number("PAR_MODTYP")
    parent_object_name = Text("PAR_NAM")
    parent_objects_file_name = Text("PAR_FLNAM")
    parent_objects_file_path = Text("PAR_FLPATH")
    parent_objects_type = Number("PAR_TYP")
    persistent_client_info_storage = Unknown("PERSIST_CLIENT_INFO")
    persistent_client_info_storage_length = Number("PERSIST_CLT_INF_LEN")
    event_type: Constant[EventType] = Constant("EVENT_TYPE", EventType)
    subscription_name = Text("EVENT_SUBS_NAME")
    scope: Constant[Scope] = Constant("EVENT_SCOPE", Scope)
    auto_subscribe = Bool("EVENT_ENABLED")
    event_implementation_class = Text("EVENT_IMPLCLASS")
    correlation_id = Text("EVENT_CORRID")
    priority_mode = Number("EVENT_PRIORITY_MODE")
    view_mode: Constant[ViewMode] = Constant("EVENT_VIEW_MODE", ViewMode)


@forms_object
class ColumnValue(Any):
    # auto-generated
    object_type = FormsObjects.column_value
