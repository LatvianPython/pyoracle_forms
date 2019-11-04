##################################################################
pyoracle_forms
##################################################################

.. image:: https://raw.githubusercontent.com/LatvianPython/pyoracle_forms/master/media/coverage.svg?sanitize=true
    :target: https://github.com/LatvianPython/pyoracle_forms

.. image:: https://img.shields.io/pypi/pyversions/pyoracle_forms
    :target: https://www.python.org/downloads/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/pypi/v/pyoracle_forms
    :target: https://pypi.org/project/pyoracle-forms/

.. image:: https://travis-ci.org/LatvianPython/pyoracle_forms.svg?branch=master
    :target: https://travis-ci.org/LatvianPython/pyoracle_forms

Wraps the Oracle Forms API under Python, so that you can write scripts to
make programmatic changes to Oracle Forms .fmb files with ease.

##################################################################
Installation and usage
##################################################################

******************************************************************
Installation
******************************************************************
The package can be installed from PyPI with ``pip install pyoracle-forms``

******************************************************************
Usage
******************************************************************
.. code-block:: python

    from pyoracle_forms import Module

    with Module.load("./your_form.fmb") as module:
        for data_block in module.data_blocks:
            for item in data_block.items:
                item.font_name = "Comic Sans MS"

        module.save()

Best used with an interactive environment, such as Jupyter Notebook, as you get better autocomplete
there due to attributes getting determined dynamically.

You also need access to successfully installed version of Oracle Forms, otherwise the scripts won't work,
as this solution depends on the Oracle Forms API.


******************************************************************
Caveats
******************************************************************

By default forms API version is assumed to be 12c, and the encoding of .fmb file text as utf-8,
to use a different version or encoding you must currently use the following code before importing ``pyoracle_forms``.
Versions supported are 12c, 10g and 6i of the Oracle forms API.

.. code-block:: python

    import builtins

    builtins.pyoracle_forms_VERSION = "12c"
    builtins.pyoracle_forms_ENCODING = "utf-8"

    from pyoracle_forms import ...
