def test_object_library_has_tabs(object_library):
    assert len(object_library.object_library_tabs) > 0


def test_object_library_tab_has_objects(object_library):
    assert all(
        len(library_tab.objects) > 0
        for library_tab in object_library.object_library_tabs
    )


def test_can_copy_from_object_library(object_library, module):

    for library_tab in object_library.object_library_tabs:
        for obj in library_tab.objects:
            new = obj.duplicate(module, obj.name + "_duplicate")

            assert new.name != obj.name
            assert new._as_parameter_ != obj._as_parameter_
            assert new.owning_object.name == module.name
