def test_subclass(new_item, property_class):
    new_item.subclass(property_class)

    assert new_item.source_object == property_class


def test_un_subclass(subclassed_item):
    subclass = subclassed_item.source_object

    subclassed_item.un_subclass()

    assert subclass.source_object != subclass
    assert not subclassed_item.source_object
