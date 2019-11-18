from pyoracle_forms import move


def test_move(new_data_block, make_item):
    for i in range(0, 10):
        make_item(new_data_block, f"ITM_{i}")

    first_item = new_data_block.items[0]

    move(first_item, None)

    assert new_data_block.items[-1].name == first_item.name
