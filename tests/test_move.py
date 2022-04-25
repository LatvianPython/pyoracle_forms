import pytest

from pyoracle_forms import move


@pytest.fixture(scope="function")
def new_items(new_data_block, make_item):
    for i in range(0, 10):
        make_item(new_data_block, f"ITM_{i}")

    return new_data_block, new_data_block.items[0]


def test_move_standalone(new_items):
    data_block, first_item = new_items

    move(first_item, None)

    assert data_block.items[-1] == first_item


def test_move_object_method(new_items):
    data_block, first_item = new_items

    first_item.move(None)

    assert data_block.items[-1] == first_item


def test_move_object_second(new_items):
    data_block, first_item = new_items

    third_item = data_block.items[2]

    first_item.move(third_item)

    assert data_block.items[1] == first_item
