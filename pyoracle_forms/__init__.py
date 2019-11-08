from .context import context
from .error_handling import FormsException
from .forms_api import read_api_objects
from .forms_objects import Alert
from .forms_objects import AttachedLibrary
from .forms_objects import Canvas
from .forms_objects import DataBlock
from .forms_objects import FormParameter
from .forms_objects import GenericObject
from .forms_objects import Graphic
from .forms_objects import Item
from .forms_objects import Module
from .forms_objects import ProgramUnit
from .forms_objects import PropertyClass
from .forms_objects import RadioButton
from .forms_objects import Relation
from .forms_objects import TabPage
from .forms_objects import Trigger
from .forms_objects import VisualAttribute
from .forms_objects import Window
from .misc import add_properties
from .misc import registered_objects

__version__ = "0.2.2"


def initialize_context(version="12c", encoding="utf-8"):
    context.init(version=version, encoding=encoding)

    api_objects = read_api_objects(version)

    for forms_object in registered_objects.values():
        add_properties(forms_object, api_objects)
