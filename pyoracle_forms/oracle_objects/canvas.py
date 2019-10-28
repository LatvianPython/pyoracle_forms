from pyoracle_forms.constants import Properties, FormsObjects
from pyoracle_forms.misc import forms_object
from pyoracle_forms.oracle_objects.generic import GenericObject
from pyoracle_forms.oracle_objects.graphic import Graphic
from pyoracle_forms.oracle_objects.tab_page import TabPage
from pyoracle_forms.utils import Subobjects


@forms_object(object_type=FormsObjects.canvas)
class Canvas(GenericObject):
    graphics = Subobjects(Properties.GRAPHIC, Graphic)
    tab_pages = Subobjects(Properties.TAB_PAGE, TabPage)
