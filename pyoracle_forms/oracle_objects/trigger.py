from pyoracle_forms.constants import FormsObjects
from pyoracle_forms.misc import forms_object
from pyoracle_forms.oracle_objects.generic import GenericObject


@forms_object(object_type=FormsObjects.trigger)
class Trigger(GenericObject):
    pass
