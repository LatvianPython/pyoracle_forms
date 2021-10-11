import pytest


def test_canvas_has_graphics(canvas):
    assert len(canvas.graphics) > 0


def test_canvas_has_no_tab_pages(canvas):
    assert len(canvas.tab_pages) == 0


def test_unusable_property(canvas):
    with pytest.raises(NotImplementedError):
        canvas.persistent_client_info_storage = ""
