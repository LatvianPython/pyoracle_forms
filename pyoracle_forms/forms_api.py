import json
import pathlib
from ctypes import *
from os import pathsep, environ
from os.path import exists, abspath, join

# todo: this does not really work, ambiguity with 10g and 12c, and should be revised, user chooses during startup?
dll_names = {
    '12c': ('frmd2f.dll', 'msvcr100'),
    '10g': ('frmd2f.dll', 'msvcrt'),
    '6i': ('ifd2f60.dll', 'msvcrt'),
}


def find_dll(dll_name):
    search_path = environ["PATH"]
    for path in search_path.split(pathsep):
        if exists(join(path, dll_name)):
            return abspath(path)


for version, (api_dll, msvcrt) in dll_names.items():
    if find_dll(api_dll):
        api = cdll.LoadLibrary(api_dll)
        free = cdll.LoadLibrary(msvcrt).free
        break
else:
    raise ImportError('No Oracle Forms API found')

file_path = pathlib.Path(__file__).parent.parent / 'forms_api' / f'parsed_{version}.json'

with open(file_path, mode='r', encoding='utf-8') as file:
    api_objects = json.load(file)
