import pytest

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
