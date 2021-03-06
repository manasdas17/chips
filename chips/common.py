#!/usr/bin/env python

"""Common utilities for Streams library"""

from math import log
from copy import copy

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def resize(val, bits):
    mask = (2**(bits))-1
    sign_bit = (2**(bits-1))
    val = val&mask
    if val & sign_bit: 
        val=val|~mask
    return val

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

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

def calculate_jumps(instructions):
    address = 0
    new_instructions = []
    labels = {}

    for instruction in instructions:
        if instruction.label:
            labels[instruction.label] = address
        else:
            address += 1
            new_instructions.append(copy(instruction))

    for instruction in new_instructions:
        if type(instruction.immediate) is str:
            instruction.immediate = labels[instruction.immediate]

    return new_instructions
