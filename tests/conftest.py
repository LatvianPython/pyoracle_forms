import shutil

import pytest

from pyoracle_forms import Module


@pytest.fixture(scope='session')
def module():
    with Module.load('./tests/test_modules/simple_module.fmb') as module:
        yield module


@pytest.fixture(scope='function')
def new_module():
    with Module.create('new_module') as module:
        yield module


@pytest.fixture(scope='session')
def data_block(module):
    return module.data_blocks[0]


@pytest.fixture(scope='session')
def item(data_block):
    return data_block.items[0]


@pytest.fixture(scope='session')
def canvas(module):
    return module.canvases[0]


@pytest.fixture(scope='session')
def test_dir(tmpdir_factory):
    test_directory = tmpdir_factory.mktemp('forms')
    yield test_directory
    shutil.rmtree(test_directory)
