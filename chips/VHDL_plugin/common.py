"""Common routines used in VHDL generation"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def binary(integer, bits=None):
    """Returns binary string representation of an integer"""
    if bits == 0 : return '"0"'
    mask = (1<<(bits-1))
    string = '"'
    while mask:
        if integer & mask:
            string += "1"
        else:
            string += "0"
        mask = mask >> 1
    string += '"'
    return string
