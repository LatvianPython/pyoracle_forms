from pyoracle_forms import Item


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
