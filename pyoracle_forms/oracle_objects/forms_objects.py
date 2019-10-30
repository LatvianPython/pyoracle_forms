from pyoracle_forms.constants import FormsObjects
from pyoracle_forms.misc import forms_object
from pyoracle_forms.oracle_objects.generic import GenericObject


@forms_object(object_type=FormsObjects.attached_library)
class AttachedLibrary(GenericObject):
    pass


@forms_object(object_type=FormsObjects.alert)
class Alert(GenericObject):
    pass


@forms_object(object_type=FormsObjects.canvas)
class Canvas(GenericObject):
    pass


@forms_object(object_type=FormsObjects.data_block)
class DataBlock(GenericObject):
    pass


@forms_object(object_type=FormsObjects.form_parameter)
class FormParameter(GenericObject):
    pass


@forms_object(object_type=FormsObjects.graphic)
class Graphic(GenericObject):
    pass


@forms_object(object_type=FormsObjects.item)
class Item(GenericObject):
    pass


@forms_object(object_type=FormsObjects.program_unit)
class ProgramUnit(GenericObject):
    pass


@forms_object(object_type=FormsObjects.property_class)
class PropertyClass(GenericObject):
    pass


@forms_object(object_type=FormsObjects.radio_button)
class RadioButton(GenericObject):
    pass


@forms_object(object_type=FormsObjects.relation)
class Relation(GenericObject):
    pass


@forms_object(object_type=FormsObjects.tab_page)
class TabPage(GenericObject):
    pass


@forms_object(object_type=FormsObjects.trigger)
class Trigger(GenericObject):
    pass


@forms_object(object_type=FormsObjects.visual_attribute)
class VisualAttribute(GenericObject):
    pass


@forms_object(object_type=FormsObjects.window)
class Window(GenericObject):
    pass
