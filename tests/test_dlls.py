import pytest
from pyoracle_forms.forms_api import find_dll, dlls


def test_dll_not_exists():
    with pytest.raises(ImportError):
        dlls("6i")


# find_dll("")
# dlls
