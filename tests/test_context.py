from pyoracle_forms import context


def test_can_destroy_context():
    ctx = context.create_context()

    context.destroy_context(ctx)

    assert not ctx
