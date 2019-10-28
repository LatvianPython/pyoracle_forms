def test_item_has_name(simple_item):
    assert simple_item.name == 'TEXT_ITEM4'


def test_can_set_color(simple_item):
    old_color = simple_item.background_color
    r, g, b = 255, 0, 0
    new_color = f'r{r}g{g}b{b}'

    simple_item.background_color = new_color

    assert simple_item.background_color != old_color and simple_item.background_color == new_color
