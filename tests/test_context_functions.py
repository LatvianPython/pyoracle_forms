from pyoracle_forms.context import context


def test_object_name():
    assert context.object_name(1) == "ALERT"


def test_object_number():
    assert context.object_number("ALERT") == 1
