from .context import context
from .context import move
from .error_handling import FormsException
from .forms_api import read_api_objects
from .forms_objects import Alert
from .forms_objects import AttachedLibrary
from .forms_objects import Canvas
from .forms_objects import ColumnValue
from .forms_objects import DataBlock
from .forms_objects import DataSourceArgument
from .forms_objects import DataSourceColumn
from .forms_objects import Editor
from .forms_objects import Event
from .forms_objects import FormParameter
from .forms_objects import GenericObject
from .forms_objects import Graphic
from .forms_objects import Item
from .forms_objects import LOV
from .forms_objects import LOVColumnMap
from .forms_objects import Menu
from .forms_objects import MenuItem
from .forms_objects import Module
from .forms_objects import ObjectChild
from .forms_objects import ObjectGroup
from .forms_objects import Point
from .forms_objects import ProgramUnit
from .forms_objects import PropertyClass
from .forms_objects import RadioButton
from .forms_objects import RecordGroup
from .forms_objects import RecordGroupColspec
from .forms_objects import Relation
from .forms_objects import Report
from .forms_objects import TabPage
from .forms_objects import Trigger
from .forms_objects import VisualAttribute
from .forms_objects import Window
from .misc import add_properties
from .misc import registered_objects

__version__ = "0.2.8"


def initialize_context(version: str = "12c", encoding: str = "utf-8") -> None:
    context.init(version=version, encoding=encoding)

    api_objects = read_api_objects(version=version)

    for forms_object in registered_objects.values():
        add_properties(forms_object, api_objects)
