import json
import pathlib
import builtins

from ctypes import *
from os import pathsep, environ, add_dll_directory
from os.path import exists, abspath, join


if hasattr(builtins, "pyoracle_forms_VERSION"):
    version = builtins.pyoracle_forms_VERSION
else:
    version = "12c"

dll_names = {
    "12c": ("frmd2f.dll", "msvcr100"),
    "10g": ("frmd2f.dll", "msvcrt"),
    "6i": ("ifd2f60.dll", "msvcrt"),
}


def find_dll(dll_name):
    search_path = environ["PATH"]
    for path in search_path.split(pathsep):
        if exists(join(path, dll_name)):
            return abspath(path)


api_dll, msvcrt = dll_names[version]
if dll_path := find_dll(api_dll):
    with add_dll_directory(dll_path):
        api = cdll.LoadLibrary(api_dll)
    free = cdll.LoadLibrary(msvcrt).free
else:
    raise ImportError("No Oracle Forms API found")

file_path = pathlib.Path(__file__).parent / f"parsed_{version}.json"

with open(file_path, mode="r", encoding="utf-8") as file:
    api_objects = json.load(file)
