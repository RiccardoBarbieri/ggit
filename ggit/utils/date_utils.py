import re
import argparse

from ggit.utils.constants import date_regex

def date_iso_8601(arg_value, pattern=re.compile(date_regex)):
    if not pattern.match(arg_value):
        raise argparse.ArgumentTypeError("Not a valid date")
    return arg_value