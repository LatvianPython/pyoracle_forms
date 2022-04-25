import pytest

from pyoracle_forms import Properties, FormsObjects
from pyoracle_forms import Item, FormsException


def test_item_has_name(item):
    assert item.name == "TEXT_ITEM4"


def test_can_create_new_items(data_block):
    old_item_count = len(data_block.items)
    Item.create(data_block, "NEW_ITEM")
    assert len(data_block.items) > old_item_count


def test_created_items_have_passed_name(data_block):
    assert Item.create(data_block, "MY_ITEM").name == "MY_ITEM"


def test_has_property(item):
    assert item.has_property(154)


def test_has_no_such_property(item):
    assert not item.has_property(100)


def test_invalid_property(item):
    with pytest.raises(FormsException):
        assert not item.has_property(1000)


def test_can_delete_items(data_block, make_item):
    for i in range(10):
        make_item(data_block, f"ITM_{i}")

    items = len(data_block.items)

    data_block.items[0].destroy()
    assert len(data_block.items) < items


def test_equality(data_block):
    assert data_block.items[0] == data_block.items[0]


def test_inequality(data_block, make_item):
    assert make_item(data_block, "ITM_1") != make_item(data_block, "ITM_2")


def test_equality_not_implemented(data_block):
    assert not data_block == 1


def test_query_type(new_item):
    assert new_item.query_type() == 15


@pytest.mark.xfail
def test_duplicate(new_item):
    duplicated = new_item.duplicate(new_item.owning_object, "DUPLICATED_ITM")

    assert duplicated.name == "DUPLICATED_ITEM"


@pytest.mark.xfail
def test_replicate(new_item):
    replicated = new_item.replicate(new_item.owning_object, "REPLICATED_ITM")

    assert replicated.name == "REPLICATED_ITEM"


@pytest.mark.xfail
def test_find_object(new_item):
    to_find = new_item.name

    assert (
        new_item.owning_object.find_object(to_find, FormsObjects.item).name == to_find
    )


@pytest.mark.xfail
def test_inherit_property(new_item):
    assert new_item.inherit_property(Properties.x_position)


@pytest.mark.xfail
def test_is_property_inherited(new_item):
    assert new_item.is_property_inherited(Properties.x_position)


@pytest.mark.xfail
def test_is_property_default(new_item):
    assert new_item.is_property_default(Properties.x_position)


@pytest.mark.xfail
def test_is_subclassed(new_item):
    assert new_item.is_subclassed()
