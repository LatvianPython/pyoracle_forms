import enum


class Justification(enum.IntEnum):
    left = 0
    right = 1
    center = 2
    start = 3
    end = 4


class DefaultAlertButton(enum.IntEnum):
    button_1 = 0
    button_2 = 1
    button_3 = 2


class AlertStyle(enum.IntEnum):
    stop = 0
    caution = 1
    note = 2


class Bevel(enum.IntEnum):
    raised = 0
    lowered = 1
    none = 2
    inset = 3
    outset = 4
    plain = 5


class CaseRestriction(enum.IntEnum):
    mixed = 0
    upper = 1
    lower = 2


class CheckBoxMappingofOtherValues(enum.IntEnum):
    not_allowed = 0
    checked = 1
    unchecked = 2


class CanvasType(enum.IntEnum):
    content = 0
    stacked = 1
    vertical_toolbar = 2
    horizontal_toolbar = 3
    tab = 4


class ColumnDataType(enum.IntEnum):
    character = 0
    number = 1
    date = 2
    long = 3
    object_ref = 4


class CommandType(enum.IntEnum):
    null = 0
    menu = 1
    plsql = 2


class ImageFormat(enum.IntEnum):
    bmp = 0
    cals = 1
    gif = 2
    jfif = 3
    pict = 4
    ras = 5
    tiff = 6
    tpic = 7
    native = 8


class ImageDepth(enum.IntEnum):
    original = 0
    monochrome = 1
    gray = 2
    lut = 3
    rgb = 4


class CoordinateSystem(enum.IntEnum):
    character = 0
    real = 1


class CursorMode(enum.IntEnum):
    open = 0
    close = 1


class DeleteRecordBehavior(enum.IntEnum):
    cascading = 0
    isolated = 1
    non_isolated = 2


class InitialKeyboardState(enum.IntEnum):
    default = 0
    roman = 1
    local = 2


class Direction(enum.IntEnum):
    default = 0
    left_to_right = 1
    right_to_left = 2


class ExecutionHierarchy(enum.IntEnum):
    override = 0
    before = 1
    after = 2


class FontStyle(enum.IntEnum):
    plain = 0
    italic = 1
    oblique = 2
    underline = 3
    outline = 4
    shadow = 5
    inverted = 6
    overstrike = 7
    blink = 8


class FontWeight(enum.IntEnum):
    ultralight = 0
    extralight = 1
    light = 2
    demilight = 3
    medium = 4
    demibold = 5
    bold = 6
    extrabold = 7
    ultrabold = 8


class FontSpacing(enum.IntEnum):
    ultradense = 0
    extradense = 1
    dense = 2
    semidense = 3
    normal = 4
    semiexpand = 5
    expand = 6
    extraexpand = 7
    ultraexpand = 8


class ParameterDataType(enum.IntEnum):
    char = 0
    number = 1
    date = 2


class ExecutionMode(enum.IntEnum):
    batch = 0
    runtime = 1


class ItemType(enum.IntEnum):
    bean_area = 0
    check_box = 1
    display_item = 2
    hierarchical_tree = 3
    image = 4
    list_item = 5
    push_button = 6
    radio_group = 7
    text_item = 8
    user_area = 9
    activex_control_obsolete = 10
    chart_item_obsolete = 11
    ole_container_obsolete = 12
    sound_obsolete = 13
    vbx_control_obsolete = 14


class DataType(enum.IntEnum):
    char = 0
    number = 1
    date = 2
    alpha = 3
    integer = 4
    datetime = 5
    long = 6
    rnumber = 7
    jdate = 8
    edate = 9
    time = 10
    rinteger = 11
    money = 12
    rmoney = 13
    object_ref = 14
    nchar = 15


class KeyMode(enum.IntEnum):
    unique = 0
    updateable = 1
    non_updateable = 2
    automatic = 3


class PLSQLLibrarySource(enum.IntEnum):
    file = 0
    database = 1


class LockingMode(enum.IntEnum):
    immediate = 0
    delayed = 1
    automatic = 2


class ListType(enum.IntEnum):
    record_group = 0
    old = 1


class ListStyle(enum.IntEnum):
    poplist = 0
    tlist = 1
    combo_box = 2


class MagicItem(enum.IntEnum):
    none = 0
    cut = 1
    copy = 2
    paste = 3
    clear = 4
    undo = 5
    help = 6
    about = 7
    quit = 8
    window = 9
    page_setup_obsolete = 10


class MenuItemType(enum.IntEnum):
    plain = 0
    check = 1
    radio = 2
    separator = 3
    magic = 4


class CompressionQuality(enum.IntEnum):
    none = 0
    minimum = 1
    low = 2
    medium = 3
    high = 4
    maximum = 5


class MouseNavigationLimit(enum.IntEnum):
    form = 0
    data_block = 1
    record = 2
    item = 3


class NavigationStyle(enum.IntEnum):
    same_record = 0
    change_record = 1
    change_data_block = 2


class DisplayQuality(enum.IntEnum):
    high = 0
    medium = 1
    low = 2


class ReadingOrder(enum.IntEnum):
    default = 0
    left_to_right = 1
    right_to_left = 2


class RealUnit(enum.IntEnum):
    pixel = 0
    centimeter = 1
    inch = 2
    point = 3
    decipoint = 4


class RecordGroupType(enum.IntEnum):
    query = 0
    static = 1


class RecordOrientation(enum.IntEnum):
    vertical = 0
    horizontal = 1


class ScrollBarOrientation(enum.IntEnum):
    vertical = 0
    horizontal = 1


class SizingStyle(enum.IntEnum):
    crop = 0
    adjust = 1
    fill = 2


class TriggerStyle(enum.IntEnum):
    plsql = 0
    v2 = 1


class PromptFontStyle(enum.IntEnum):
    plain = 0
    italic = 1
    oblique = 2
    underline = 3
    outline = 4
    shadow = 5
    inverted = 6
    overstrike = 7
    blink = 8


class CalculationMode(enum.IntEnum):
    none = 0
    formula = 1
    summary = 2


class PromptFontWeight(enum.IntEnum):
    ultralight = 0
    extralight = 1
    light = 2
    demilight = 3
    medium = 4
    demibold = 5
    bold = 6
    extrabold = 7
    ultrabold = 8


class PromptFontSpacing(enum.IntEnum):
    ultradense = 0
    extradense = 1
    dense = 2
    semidense = 3
    normal = 4
    semiexpand = 5
    expand = 6
    extraexpand = 7
    ultraexpand = 8


class PromptDisplayStyle(enum.IntEnum):
    hidden = 0
    first_record = 1
    all_records = 2


class ValidationUnit(enum.IntEnum):
    default = 0
    form = 1
    data_block = 2
    record = 3
    item = 4


class WindowStyle(enum.IntEnum):
    document = 0
    dialog = 1


class WrapStyle(enum.IntEnum):
    none = 0
    character = 1
    word = 2


class GraphicsType(enum.IntEnum):
    arc = 0
    image = 1
    line = 2
    polygon = 3
    rectangle = 4
    rounded_rectangle = 5
    text = 6
    group = 7
    frame = 8


class ArrowStyle(enum.IntEnum):
    none = 0
    start = 1
    end = 2
    both_ends = 3
    middle_to_start = 4
    middle_to_end = 5


class PromptReadingOrder(enum.IntEnum):
    default = 0
    left_to_right = 1
    right_to_left = 2


class PromptJustification(enum.IntEnum):
    left = 0
    right = 1
    center = 2
    start = 3
    end = 4


class PromptAttachmentEdge(enum.IntEnum):
    start = 0
    end = 1
    top = 2
    bottom = 3


class PromptAlignment(enum.IntEnum):
    start = 0
    end = 1
    center = 2


class FrameTitleReadingOrder(enum.IntEnum):
    default = 0
    left_to_right = 1
    right_to_left = 2


class FrameTitleAlignment(enum.IntEnum):
    left = 0
    right = 1
    center = 2
    start = 3
    end = 4


class LayoutStyle(enum.IntEnum):
    form = 0
    tabular = 1


class FrameAlignment(enum.IntEnum):
    start = 0
    end = 1
    center = 2
    fill = 3
    column = 4


class SingleObjectAlignment(enum.IntEnum):
    start = 0
    end = 1
    center = 2


class StartPromptAlignment(enum.IntEnum):
    start = 0
    end = 1
    center = 2


class TopPromptAlignment(enum.IntEnum):
    start = 0
    end = 1
    center = 2


class UpdateLayout(enum.IntEnum):
    manually = 0
    automatically = 1
    locked = 2


class DashStyle(enum.IntEnum):
    solid = 0
    dotted = 1
    dashed = 2
    dash_dot = 3
    double_dot = 4
    long_dash = 5
    dash_double_dot = 6


class CapStyle(enum.IntEnum):
    butt = 0
    round = 1
    projecting = 2


class JoinStyle(enum.IntEnum):
    mitre = 0
    bevel = 1
    round = 2


class LineSpacing(enum.IntEnum):
    single = 0
    one_and_a_half = 1
    double = 2
    custom = 3


class HorizontalOrigin(enum.IntEnum):
    left = 0
    right = 1
    center = 2


class VerticalOrigin(enum.IntEnum):
    top = 0
    center = 1
    bottom = 2


class HorizontalJustification(enum.IntEnum):
    left = 0
    right = 1
    center = 2
    start = 3
    end = 4


class VerticalJustification(enum.IntEnum):
    top = 0
    center = 1
    bottom = 2


class SummaryFunction(enum.IntEnum):
    none = 0
    avg = 1
    count = 2
    max = 3
    min = 4
    stddev = 5
    sum = 6
    variance = 7


class ArgumentMode(enum.IntEnum):
    in_ = 0
    out = 1
    in_out = 2


class CommunicationMode(enum.IntEnum):
    synchronous = 0
    asynchronous = 1


class ColumnType(enum.IntEnum):
    varchar2 = 0
    number = 1
    long = 2
    rowid = 3
    date = 4
    raw = 5
    long_raw = 6
    char = 7
    mlslabel = 8
    table = 9
    record = 10
    refcursor = 11
    named_type = 12
    object_ref = 13
    varray = 14
    nested_table = 15
    blob = 16
    clob = 17
    bfile = 18
    nvarchar2 = 19
    nchar = 20
    nclob = 21


class ArgumentType(enum.IntEnum):
    varchar2 = 0
    number = 1
    long = 2
    rowid = 3
    date = 4
    raw = 5
    long_raw = 6
    char = 7
    mlslabel = 8
    table = 9
    record = 10
    refcursor = 11
    named_type = 12
    object_ref = 13
    varray = 14
    nested_table = 15
    blob = 16
    clob = 17
    bfile = 18
    nvarchar2 = 19
    nchar = 20
    nclob = 21


class QueryDataSourceType(enum.IntEnum):
    none = 0
    table = 1
    procedure = 2
    transactional_triggers = 3
    from_clause_query = 4


class DMLDataTargetType(enum.IntEnum):
    none = 0
    table = 1
    procedure = 2
    transactional_triggers = 3


class TabAttachmentEdge(enum.IntEnum):
    top = 0
    bottom = 1
    left = 2
    right = 3
    start = 4
    end = 5


class VisualAttributeType(enum.IntEnum):
    common = 0
    prompt = 1
    title = 2


class FrameTitleFontStyle(enum.IntEnum):
    plain = 0
    italic = 1
    oblique = 2
    underline = 3
    outline = 4
    shadow = 5
    inverted = 6
    overstrike = 7
    blink = 8


class FrameTitleFontWeight(enum.IntEnum):
    ultralight = 0
    extralight = 1
    light = 2
    demilight = 3
    medium = 4
    demibold = 5
    bold = 6
    extrabold = 7
    ultrabold = 8


class FrameTitleFontSpacing(enum.IntEnum):
    ultradense = 0
    extradense = 1
    dense = 2
    semidense = 3
    normal = 4
    semiexpand = 5
    expand = 6
    extraexpand = 7
    ultraexpand = 8


class CornerStyle(enum.IntEnum):
    chamfered = 0
    square = 1
    rounded = 2


class InteractionMode(enum.IntEnum):
    blocking = 0
    non_blocking = 1


class IsolationMode(enum.IntEnum):
    read_committed = 0
    serializable = 1


class ReportDestinationType(enum.IntEnum):
    preview = 0
    file = 1
    printer = 2
    mail = 3
    cache = 4
    screen = 5


class KeyboardState(enum.IntEnum):
    any = 0
    roman_only = 1
    local_only = 2


class ScrollBarAlignment(enum.IntEnum):
    start = 0
    end = 1


class ProgramUnitType(enum.IntEnum):
    unknown = 0
    procedure = 1
    function = 2
    package_spec = 3
    package_body = 4


class RuntimeCompatibilityMode(enum.IntEnum):
    v4_5 = 0
    v5_0 = 1


class GraphicFontWeight(enum.IntEnum):
    ultralight = 0
    extralight = 1
    light = 2
    demilight = 3
    medium = 4
    demibold = 5
    bold = 6
    extrabold = 7
    ultrabold = 8


class GraphicFontSpacing(enum.IntEnum):
    ultradense = 0
    extradense = 1
    dense = 2
    semidense = 3
    normal = 4
    semiexpand = 5
    expand = 6
    extraexpand = 7
    ultraexpand = 8


class RelationType(enum.IntEnum):
    join = 0
    ref = 1


class DataLengthSemantics(enum.IntEnum):
    null = 0
    byte = 1
    char = 2


class EventType(enum.IntEnum):
    database = 0
    user_defined = 1
    system_client_idle = 2
    system_db_idle = 3
    system_single_sign_off = 4
    system_notification = 5
    system_media_completion = 6


class Scope(enum.IntEnum):
    application = 0
    form = 1


class ViewMode(enum.IntEnum):
    browse = 0
    locked = 1
    removed = 2
