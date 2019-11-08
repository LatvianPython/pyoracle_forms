from .error_handling import FormsException

from .oracle_objects import Alert
from .oracle_objects import AttachedLibrary
from .oracle_objects import Canvas
from .oracle_objects import DataBlock
from .oracle_objects import FormParameter
from .oracle_objects import GenericObject
from .oracle_objects import Graphic
from .oracle_objects import Item
from .oracle_objects import Module
from .oracle_objects import ProgramUnit
from .oracle_objects import PropertyClass
from .oracle_objects import RadioButton
from .oracle_objects import Relation
from .oracle_objects import TabPage
from .oracle_objects import Trigger
from .oracle_objects import VisualAttribute
from .oracle_objects import Window

from .context import context
from .misc import add_properties
from .misc import registered_objects
from .forms_api import read_api_objects

__version__ = "0.2.1"


def initialize_context(version="12c", encoding="utf-8"):
    context.init(version=version, encoding=encoding)

    api_objects = read_api_objects(version)

    for forms_object in registered_objects.values():
        add_properties(forms_object, api_objects)
