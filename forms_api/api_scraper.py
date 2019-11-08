import json
import re
from collections import deque, defaultdict
from itertools import repeat, chain


def file_lines(filepath):
    with open(filepath, mode="r", encoding="utf-8") as file:
        return file.readlines()


def scrape_constants(filepath, prefix):
    constant_re = re.compile(r"#define (\w+?) +(\d+)")

    def parse_line(line):
        constant, value = constant_re.match(line).groups()
        return constant, int(value)

    return dict(
        parse_line(line)
        for line in file_lines(filepath)
        if line.startswith(f"#define {prefix}")
    )


def collect_macros(lines):
    deq = deque(lines)
    deq.rotate(-1)
    return (
        "".join((convenience, signature)).replace("\n", "")
        for convenience, signature in zip(lines, deq)
        if convenience.startswith("#define d2f")
    )


def all_macros(filepath):
    return collect_macros(file_lines(filepath))


ABBREVIATIONS = {
    "ob": "D2FFO_ANY",
    "alt": "D2FFO_ALERT",
    "alb": "D2FFO_ATT_LIB",
    "blk": "D2FFO_BLOCK",
    "cnv": "D2FFO_CANVAS",
    "crd": "D2FFO_COORD",
    "dsa": "D2FFO_DAT_SRC_ARG",
    "dsc": "D2FFO_DAT_SRC_COL",
    "edt": "D2FFO_EDITOR",
    "fnt": "D2FFO_FONT",
    "fmd": "D2FFO_FORM_MODULE",
    "fpm": "D2FFO_FORM_PARAM",
    "gra": "D2FFO_GRAPHIC",
    "itm": "D2FFO_ITEM",
    "lpu": "D2FFO_LIB_PROG_UNIT",
    "lib": "D2FFO_LIBRARY_MODULE",
    "lov": "D2FFO_LOV",
    "lcm": "D2FFO_LV_COLMAP",
    "mnu": "D2FFO_MENU",
    "mni": "D2FFO_MENU_ITEM",
    "mmd": "D2FFO_MENU_MODULE",
    "mpm": "D2FFO_MENU_PARAM",
    "obg": "D2FFO_OBJ_GROUP",
    "ogc": "D2FFO_OBG_CHILD",
    "olb": "D2FFO_OBJ_LIB",
    "olt": "D2FFO_OBJ_LIB_TAB",
    "pgu": "D2FFO_PROG_UNIT",
    "ppc": "D2FFO_PROP_CLASS",
    "rdb": "D2FFO_RADIO_BUTTON",
    "rcg": "D2FFO_REC_GROUP",
    "rcs": "D2FFO_RG_COLSPEC",
    "rel": "D2FFO_RELATION",
    "rpt": "D2FFO_REPORT",
    "tbp": "D2FFO_TAB_PAGE",
    "trg": "D2FFO_TRIGGER",
    "vat": "D2FFO_VIS_ATTR",
    "win": "D2FFO_WINDOW",
}


def parse_headers(api_version):

    properties = scrape_constants(f"./{api_version}/d2fdef.h", "D2FP_")
    objects = scrape_constants(f"./{api_version}/d2fdef.h", "D2FFO_")

    abbreviations = {
        abbreviation: (object_type, objects[object_type])
        for abbreviation, object_type in ABBREVIATIONS.items()
        if object_type in objects.keys()
    }

    macro_regex = re.compile(
        r"#define d2f\w+?[gs]_(\w+?)\(.+(?:(?:Get)|(?:Set))(.+?)Prop.+,(\w+),val\)"
    )

    macros = chain.from_iterable(
        zip(all_macros(f"./{api_version}/d2f{abbreviation}.h"), repeat(object_type))
        for abbreviation, object_type in abbreviations.items()
    )

    object_properties = defaultdict(set)

    for macro, object_type in macros:
        match = macro_regex.match(macro)
        if match:
            prop_name, prop_type, prop = match.groups()
            object_properties[object_type].add(
                (prop_name, prop_type.lower(), prop, properties[prop])
            )

    parsed = {
        obj_name: {
            "object_number": obj_type,
            "properties": sorted(
                [
                    {
                        "short_name": short_name,
                        "data_type": data_type,
                        "macro_name": macro_name,
                        "property_number": property_name,
                    }
                    for (short_name, data_type, macro_name, property_name) in properties
                ],
                key=lambda x: x["property_number"],
            ),
        }
        for (obj_name, obj_type), properties in object_properties.items()
    }

    return parsed


def parse_all():
    versions = ["6i", "10g", "12c"]

    for version in versions:
        with open(
            f"../pyoracle_forms/forms_api/parsed_{version}.json",
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(parse_headers(version), file, indent=2)


def main():
    parse_all()


if __name__ == "__main__":
    main()
