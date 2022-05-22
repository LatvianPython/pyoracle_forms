def test_program_units(library):
    for program_unit in library.program_units:
        assert program_unit.program_unit_text


def test_library_has_program_units(library):
    assert library.program_units
