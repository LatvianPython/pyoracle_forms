from pyoracle_forms.constants import FormsObjects
from pyoracle_forms.constants import Properties
from pyoracle_forms.misc import forms_object
from pyoracle_forms.oracle_objects.generic import GenericObject
from pyoracle_forms.oracle_objects.item import Item
from pyoracle_forms.utils import Subobjects


@forms_object(object_type=FormsObjects.data_block)
class DataBlock(GenericObject):
    items = Subobjects(Properties.ITEM, Item)
