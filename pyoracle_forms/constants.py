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


# todo: should scrape these from the C headers
#  should really scrape these from the C headers..., sorta have already, only need to implement them...
if version in ('12c', '10g'):
    class Properties(enum.IntEnum):
        LABEL = 118
        NAME = 154
        NEXT = 159
        CANVAS = 24
        BLOCK = 21
        ALERT = 3
        ATTACHED_LIBRARY = 11
        EDITOR = 64
        FORM_PARAMETER = 89
        PROGRAM_UNIT = 179
        PROPERTY_CLASS = 180
        TRIGGER = 232
        VISUAL_ATTRIBUTE = 258
        WINDOW = 264
        GRAPHIC = 23
        GRAPHIC_FONT_NAME = 493
        TAB_PAGE = 356
        ITEM = 105
        PROMPT = 288
        FOREGROUND_COLOR = 87
        BACKGROUND_COLOR = 17
        FONT_NAME = 82
        FONT_NAME_PROMPT = 214
else:
    class Properties(enum.IntEnum):
        LABEL = 243
        NAME = 300
        NEXT = 302
        CANVAS = 40
        BLOCK = 29
        ALERT = 3
        ATTACHED_LIBRARY = 15
        EDITOR = 8
        FORM_PARAMETER = 11
        PROGRAM_UNIT = 376
        PROPERTY_CLASS = 377
        TRIGGER = 232
        VISUAL_ATTRIBUTE = 516
        WINDOW = 530
        GRAPHIC = 180
        GRAPHIC_FONT_NAME = 184
        TAB_PAGE = 465
        ITEM = 229
        PROMPT = 355
        FOREGROUND_COLOR = 159
        BACKGROUND_COLOR = 25
        FONT_NAME = 153
        FONT_NAME_PROMPT = 363
