import enum

from pyoracle_forms.forms_api import version


class ValueTypes(enum.IntEnum):
    UNKNOWN = 0
    BOOLEAN = 1
    NUMBER = 2
    TEXT = 3
    OBJECT = 4


class FormsObjects(enum.Enum):
    canvas = 'D2FFO_CANVAS'
    alert = 'D2FFO_ALERT'
    attached_library = 'D2FFO_ATT_LIB'
    data_block = 'D2FFO_BLOCK'
    form_parameter = 'D2FFO_FORM_PARAM'
    graphic = 'D2FFO_GRAPHIC'
    item = 'D2FFO_ITEM'
    program_unit = 'D2FFO_PROG_UNIT'
    property_class = 'D2FFO_PROP_CLASS'
    radio_button = 'D2FFO_RADIO_BUTTON'
    relation = 'D2FFO_RELATION'
    tab_page = 'D2FFO_TAB_PAGE'
    trigger = 'D2FFO_TRIGGER'
    visual_attribute = 'D2FFO_VIS_ATTR'
    window = 'D2FFO_WINDOW'
    module = 'D2FFO_FORM_MODULE'


class ObjectProperties(enum.Enum):
    canvases = 'D2FP_CANVAS'
    alerts = 'D2FP_ALERT'
    attached_libraries = 'D2FP_ATT_LIB'
    data_blocks = 'D2FP_BLOCK'
    form_parameters = 'D2FP_FORM_PARAM'
    graphics = 'D2FP_GRAPHIC'
    items = 'D2FP_ITEM'
    program_units = 'D2FP_PROG_UNIT'
    property_classes = 'D2FP_PROP_CLASS'
    radio_buttons = 'D2FP_RADIO_BUTTON'
    relations = 'D2FP_RELATION'
    tab_pages = 'D2FP_TAB_PAGE'
    triggers = 'D2FP_TRIGGER'
    visual_attributes = 'D2FP_VIS_ATTR'
    windows = 'D2FP_WINDOW'
