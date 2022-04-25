def test_subclass(new_item, property_class):
    new_item.set_subclass(property_class)

    assert new_item.source_object == property_class


def test_un_subclass(subclassed_item):
    subclass = subclassed_item.source_object

    subclassed_item.remove_subclass()

    assert subclass.source_object != subclass
    assert not subclassed_item.source_object


def test_is_not_subclassed(new_item):
    assert not new_item.is_subclassed()


def test_is_subclassed(subclassed_item):
    assert subclassed_item.is_subclassed()
