import inspect

from pyoracle_forms.generic_object import BaseObject


def get_user_attributes(cls):
    return [
        (name, obj)
        for (name, obj) in inspect.getmembers(cls)
        if not name.startswith("_")
        if not inspect.ismethod(obj)
    ]


def test_bruteforce(module):
    traversed_objects = set()

    def traverse_object(obj):
        try:
            pointer = obj._as_parameter_.value
        except AttributeError:
            pointer = obj._as_parameter_

        if pointer in traversed_objects or (pointer or 0) == 0:
            return

        traversed_objects.add(pointer)
        attributes = get_user_attributes(obj)

        for (name, data) in attributes:
            if isinstance(data, list):
                for item in data:
                    traverse_object(item)
            elif isinstance(data, BaseObject):
                traverse_object(data)

    traverse_object(module)

    assert len(traversed_objects) == 304
