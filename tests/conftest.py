from pyoracle_forms import Module

import pytest


@pytest.fixture(scope='session')
def simple_module():
    with Module.load('./test_modules/simple_module.fmb') as module:
        yield module


@pytest.fixture(scope='session')
def simple_data_block(simple_module):
    return next(iter(simple_module.data_blocks))


@pytest.fixture(scope='session')
def simple_item(simple_data_block):
    return next(iter(simple_data_block.items))


@pytest.fixture(scope='session')
def simple_canvas(simple_module):
    return next(iter(simple_module.canvases))
