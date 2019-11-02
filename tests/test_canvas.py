def test_canvas_has_graphics(canvas):
    assert len(canvas.graphics) > 0


def test_canvas_has_no_tab_pages(canvas):
    assert len(canvas.tab_pages) == 0
