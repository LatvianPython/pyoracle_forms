from pyoracle_forms.context import object_name
from pyoracle_forms.context import object_number
from pyoracle_forms.context import property_type


def test_object_name():
    assert object_name(1) == "ALERT"


def test_object_number():
    assert object_number("ALERT") == 1


def test_property_type():
    assert property_type(167) == 2
