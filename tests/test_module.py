from pyoracle_forms import Module


def test_module_has_name(simple_module):
    assert simple_module.name == 'MODULE1'


def test_can_set_module_name(simple_module):
    old_name = simple_module.name
    new_name = old_name[::-1]

    simple_module.name = new_name

    assert simple_module.name == new_name


def test_module_has_data_blocks(simple_module):
    assert len(list(simple_module.data_blocks)) > 0


def test_module_has_canvases(simple_module):
    assert len(list(simple_module.canvases)) > 0


def test_data_block_has_five_items(simple_data_block):
    assert len(simple_data_block.items) == 5


def test_can_create_new_modules():
    name = 'test_module'

    with Module.create(name) as module:
        assert module.name == name.upper()
