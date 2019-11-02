pyoracle_forms
###########

    If you're not embarrassed by the first version of your product, you've launched too late
    
    -- *Reid Hoffman*


.. image:: https://raw.githubusercontent.com/LatvianPython/pyoracle_forms/master/media/coverage.svg?sanitize=true

Example usage
###########

.. code-block:: python
    from pyoracle_forms import Module

    with Module.load('./your_form.fmb') as module:
        for data_block in module.data_blocks:
            for item in data_block.items:
                item.font_name = 'Comic Sans MS'

        module.save()

Best used with an interactive environment, such as Jupyter Notebook, as you get better autocomplete there due to attributes getting determined dynamically.

You also need access to successfully installed version of Oracle Forms, otherwise the scripts won't work, as this solution depends on the Oracle Forms API.
