from typing import Any

from flask import json, jsonify, request, abort

INVALID_INTEGER_VALUE_MESSAGE = "Error: '%s' not present, not integer or invalid value"
INVALID_STRING_VALUE_MESSAGE = "Error: '%s' not present, not string or invalid value"
INVALID_NUMBERS_ARRAY_MESSAGE_TEMPLATE = "Error: '%s' not present or not a numeric list"


def extract_incoming_json(request) -> json:
    data: json = jsonify("")

    try:
        if request.is_json and json.loads(request.get_data()):
            data = request.get_json()
        else:
            raise ValueError("Error: incorrect MIME-Type")
    except ValueError:
        abort(400, description="Error: payload is not a valid json")

    return data


def has_key(data: dict, key: str) -> bool:
    """ Checks if a dctionary (dict) contains a key """
    return key in data


def check_string(maybe_string: Any) -> bool:
    """ Checks if variable is of type string """
    return isinstance(maybe_string, str)


def check_strings_list(lst: Any) -> bool:
    """ Checks if variable is a list, not empty with members of type str, i.e. List[str] """
    return isinstance(lst, list) and \
           len(lst) > 0 and \
           all((isinstance(x, str) for x in lst))


def check_float(maybe_float: Any) -> bool:
    """ Checks if variable is of type float """
    return isinstance(maybe_float, float)


def check_int(maybe_int: Any) -> bool:
    """ Checks if variable is of type int """
    return isinstance(maybe_int, int) or str(maybe_int).isdigit()


def check_numbers_list(lst: Any) -> bool:
    """ Checks if variable is a list, not empty with members of type int of float, i.e. List[int] or List[float] """
    return isinstance(lst, list) and \
           len(lst) > 0 and \
           all((isinstance(x, int) and str(x).isdigit()) or isinstance(x, float) for x in lst)


def valid_string(data: dict, key: str) -> bool:
    """ Checks dict contains key whose associated values represent a string """
    return has_key(data, key) and \
           check_string(data[key])


def valid_int(data: dict, key: str) -> bool:
    """ Checks dict contains key whose associated values represent a string """
    return has_key(data, key) and \
           check_int(data[key])


def valid_strings_array(data: dict, key: str) -> bool:
    """ Checks if dict contains a key whose associated value represents a list o number (int or float) """
    return has_key(data, key) and \
           check_strings_list(data[key])


def valid_numbers_array(data: dict, key: str) -> bool:
    """ Checks if dict contains a key whose associated value represents a list o number (int or float) """
    return has_key(data, key) and \
           check_numbers_list(data[key])
