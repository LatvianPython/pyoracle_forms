import json
import pathlib
from ctypes import *
from os import pathsep, environ
from os.path import exists, abspath, join


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


def dlls(version):
    api_dll, msvcrt = dll_names[version]
    dll_path = find_dll(api_dll)
    if dll_path:
        msvcrt = cdll.LoadLibrary(msvcrt)
        try:
            from os import add_dll_directory

            with add_dll_directory(dll_path):
                return cdll.LoadLibrary(api_dll), msvcrt.free
        except ImportError:
            return cdll.LoadLibrary(api_dll), msvcrt.free
    raise ImportError("No Oracle Forms API found")


def read_api_objects(version):
    file_path = pathlib.Path(__file__).parent / "forms_api" / f"parsed_{version}.json"
    with open(file_path, mode="r", encoding="utf-8") as file:
        return json.load(file)
