import glob


def test_module_has_name(module):
    assert module.name == 'MODULE1'


def test_can_set_module_name(module):
    new_name = 'DUMMY'
    module.name = new_name
    assert module.name == new_name


def test_module_has_data_blocks(module):
    assert len(module.data_blocks) > 0


def test_module_has_canvases(module):
    assert len(module.canvases) > 0


def test_data_block_has_items(data_block):
    assert len(data_block.items) > 0


def test_can_create_new_modules(new_module):
    assert new_module.name == 'new_module'.upper()


def test_can_save_module(new_module, test_dir):
    save_to = f'{test_dir}/test_module1.fmb'

    new_module.save(save_to)

    assert glob.glob(save_to)
