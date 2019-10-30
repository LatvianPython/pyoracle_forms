from pyoracle_forms.properties import property_name, property_constant_name


def test_property_name():
    assert property_name(154) == 'Name'


def test_property_constant_name():
    assert property_constant_name(105) == 'ITEM'
