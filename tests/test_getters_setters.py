import pytest

from pyoracle_forms import FormsException


def test_text(new_item):
    value = "aoeu"
    new_item.name = value
    assert new_item.name == value


def test_text_empty(new_item):
    assert new_item.column_name == ""


def test_number(new_item):
    value = 10
    new_item.width = value
    assert new_item.width == value


def test_boolean_false(new_item):
    value = False
    new_item.database_item = value
    assert new_item.database_item == value


def test_boolean_true(new_item):
    value = True
    new_item.database_item = value
    assert new_item.database_item == value


def test_object(new_module, new_canvas, make_window):
    value = "WND2"
    new_window = make_window(value)
    new_canvas.window_object_pointer = new_window
    assert new_canvas.window == value


def test_null_assignment(new_canvas):
    with pytest.raises(FormsException):
        new_canvas.window_object_pointer = None
