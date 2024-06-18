import re


def camelcase_name_to_words(init_string: str):
    """Converts a camelCase string to a string with words separated by spaces."""
    string_ = [s for s in re.split("([A-Z][^A-Z]*)", init_string) if s]
    result = " ".join(string_)
    return result
