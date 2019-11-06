import enum

from pyoracle_forms.context import context
from pyoracle_forms.misc import forms_object
from . import GenericObject


class FormsObjects(enum.Enum):
    canvas = "D2FFO_CANVAS"
    alert = "D2FFO_ALERT"
    attached_library = "D2FFO_ATT_LIB"
    data_block = "D2FFO_BLOCK"
    form_parameter = "D2FFO_FORM_PARAM"
    graphic = "D2FFO_GRAPHIC"
    item = "D2FFO_ITEM"
    program_unit = "D2FFO_PROG_UNIT"
    property_class = "D2FFO_PROP_CLASS"
    radio_button = "D2FFO_RADIO_BUTTON"
    relation = "D2FFO_RELATION"
    tab_page = "D2FFO_TAB_PAGE"
    trigger = "D2FFO_TRIGGER"
    visual_attribute = "D2FFO_VIS_ATTR"
    window = "D2FFO_WINDOW"
    module = "D2FFO_FORM_MODULE"


@forms_object
class Module(GenericObject):
    object_type = FormsObjects.module

    def __init__(self, module, path=None):
        super().__init__(module)
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @classmethod
    def create(cls, module, **kwargs):
        return cls(context.create_module(module))

    @classmethod
    def load(cls, path):
        return cls(context.load_module(path), path=path)

    def save(self, path=None):
        context.save_module(self, path or self.path)


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
