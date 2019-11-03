import builtins
import shutil

import pytest

builtins.pyoracle_forms_VERSION = "12c"
builtins.pyoracle_forms_ENCODING = "utf-8"


from pyoracle_forms import Module, Item, DataBlock, Canvas, Window


@pytest.fixture(scope="session")
def module():
    with Module.load("./tests/test_modules/simple_module.fmb") as module:
        yield module


@pytest.fixture(scope="session")
def data_block(module):
    return module.data_blocks[0]


@pytest.fixture(scope="session")
def item(data_block):
    return data_block.items[0]


@pytest.fixture(scope="session")
def canvas(module):
    return module.canvases[0]


@pytest.fixture(scope="session")
def test_dir(tmpdir_factory):
    test_directory = tmpdir_factory.mktemp("forms")
    yield test_directory
    shutil.rmtree(test_directory)


@pytest.fixture(scope="function")
def new_module():
    with Module.create("new_module") as module:
        yield module


@pytest.fixture(scope="function")
def make_new_item():
    def _make_data_block(new_data_block, name):
        return Item.create(new_data_block, name)

    return _make_data_block


@pytest.fixture(scope="function")
def make_data_block(new_module):
    def _make_data_block(name):
        return DataBlock.create(new_module, name)

    return _make_data_block


@pytest.fixture(scope="function")
def make_canvas(new_module):
    def _make_canvas(name):
        return Canvas.create(new_module, name)

    return _make_canvas


@pytest.fixture(scope="function")
def make_window(new_module):
    def _make_window(name):
        return Window.create(new_module, name)

    return _make_window


@pytest.fixture(scope="function")
def new_canvas(make_canvas):
    return make_canvas("CNV")


@pytest.fixture(scope="function")
def new_item(make_data_block, make_new_item):
    return make_new_item(make_data_block("BLK"), "ITM")
