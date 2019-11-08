from functools import wraps

error_mapping = {
    0: "Operation Succeeded",
    1: "Operation Failed",
    2: "Operation returned YES",
    3: "Operation returned NO",
    4: "Bad context provided",
    5: "Bad property",
    6: "One of the args is wrong",
    7: "Object type is unknown",
    8: "Unexpected object",
    9: "Unexpected parent",
    10: "Null object passed",
    11: "Null pointer to object",
    12: "Null property",
    13: "Not connected to DB",
    14: "Out of memory",
    15: "Message file not found",
    16: "Generation failed",
    17: "Not implemented yet",
    18: "Passed in type does not match the actual object",
    19: "The operation failed partially, but the error was not fatal",
    20: "Null Data Passed in",
    21: "Data Passed in is invalid",
    22: "Index in is invalid",
    23: "The Object does not have the given property",
    24: "Initialization failed because a NULL Instance Handle passed (Applies to Windows only)",
    25: "The operation failed because the object being created/placed was not unique. "
    "An object with this name already exists",
    26: "The Object was not found",
    27: "Function can only be called in translation mode",
    28: "The database context passed in is invalid",
    29: "A subclassed module could not be found during loading",
    30: "Duplicate String ID (This slot in the string table has already been used).",
    31: "A supplied value parameter was out of the legal range",
    32: "The specified file was not found",
    33: "An attached library could not be found",
}


class FormsException(Exception):
    pass


def raise_for_code(error_code):
    raise FormsException(error_code, f"{error_mapping[error_code]}")


def handle_error_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_code, return_value = func(*args, **kwargs)
        if error_code:
            raise_for_code(error_code)
        return return_value

    return wrapper
