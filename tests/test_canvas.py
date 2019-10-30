def test_canvas_has_graphics(simple_canvas):
    assert len(simple_canvas.graphics) > 0


def test_canvas_has_no_tab_pages(simple_canvas):
    assert len(simple_canvas.tab_pages) == 0
