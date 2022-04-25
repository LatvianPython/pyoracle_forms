import json
import pathlib
from ctypes import *
from os import pathsep, environ
from os.path import exists, abspath, join
from typing import Dict, Tuple, Optional

dll_names = {
    "12c": ("frmd2f.dll", "msvcr100"),
    "10g": ("frmd2f.dll", "msvcrt"),
    "6i": ("ifd2f60.dll", "msvcrt"),
}


def find_dll(dll_name: str) -> Optional[str]:
    search_path = environ["PATH"]
    for path in search_path.split(pathsep):
        if exists(join(path, dll_name)):
            return abspath(path)
    return None


def dlls(version: str) -> Tuple[CDLL, CDLL]:
    api_dll, cdll_name = dll_names[version]
    dll_path = find_dll(api_dll)
    if dll_path:
        from os import add_dll_directory

        msvcrt = cdll.LoadLibrary(cdll_name)
        with add_dll_directory(dll_path):
            return cdll.LoadLibrary(api_dll), msvcrt
    raise ImportError("No Oracle Forms API found")


def read_api_objects(version: str) -> Dict:  # type: ignore
    file_path = pathlib.Path(__file__).parent / "forms_api" / f"parsed_{version}.json"
    with open(file_path, mode="r", encoding="utf-8") as file:
        json_data: Dict = json.load(file)  # type: ignore
    return json_data
