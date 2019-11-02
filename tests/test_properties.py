from pyoracle_forms.properties import property_name, property_constant_name, property_type


def test_property_name():
    assert property_name(154) == 'Name'


def test_property_constant_name():
    assert property_constant_name(154) == 'NAME'


def test_property_type():
    text_property = 3
    assert property_type(154) == text_property
