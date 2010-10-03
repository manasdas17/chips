#!/usr/bin/env python

"""common utilities for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from math import log

def how_many_bits(num):
    if num > 0 :
        return int(log(num, 2)) + 2
    elif num < -1:
        return int(log(abs(num)-1, 2)) + 2
    else:
        return 1

class Unique:
    identno = 0
    def __init__(self):
        self.identifier = str(Unique.identno)
        Unique.identno += 1

    def get_identifier(self):
        return self.identifier
