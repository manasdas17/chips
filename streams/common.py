#!/usr/bin/env python

"""common utilities for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

class Unique:
    identno = 0
    def __init__(self):
        self.identifier = str(Unique.identno)
        Unique.identno += 1

    def get_identifier(self):
        return self.identifier

class Stream:

    def __add__(self, other): return Binary(self, other, 'add')
    def __sub__(self, other): return Binary(self, other, 'sub')
    def __mul__(self, other): return Binary(self, other, 'mul')
    def __mod__(self, other): return Binary(self, other, 'mod')
    def __floordiv__(self, other): return Binary(self, other, 'div')
    def __and__(self, other): return Binary(self, other, 'and')
    def __or__(self, other): return Binary(self, other, 'or')
    def __xor__(self, other): return Binary(self, other, 'xor')
    def __rshift__(self, other): return Binary(self, other, 'sr')
    def __lshift__(self, other): return Binary(self, other, 'sl')
    def __eq__(self, other): return Binary(self, other, 'eq')
    def __ne__(self, other): return Binary(self, other, 'ne')
    def __gt__(self, other): return Binary(self, other, 'gt')
    def __ge__(self, other): return Binary(self, other, 'ge')
    def __lt__(self, other): return Binary(self, other, 'lt')
    def __le__(self, other): return Binary(self, other, 'le')
    def read(self, variable):
        return Read(self, variable)

class Read(Unique):
    def __init__(self, instream, variable):
        Unique.__init__(self)
        self.variable = variable
        self.instream = instream

    def write_code(self, plugin): 
        return plugin.write_read(self)

    def __repr__(self):
        return '\n'.join([
"    variable{0} <- stream{1}".format(self.variable.get_identifier(), self.instream.get_identifier()),
        ])

class  Binary(Stream, Unique):

    def __init__(self, a, b, function):
        self.a, self.b, self.function = a, b, function
        Unique.__init__(self)

    def get_bits(self):
        bit_function = {
        'add' : lambda x, y : max((x, y)) + 1,
        'sub' : lambda x, y : max((x, y)) + 1,
        'mul' : lambda x, y : x + y,
        'div' : lambda x, y : max((x, y)) + 1,
        'and' : lambda x, y : max((x, y)),
        'or'  : lambda x, y : max((x, y)),
        'xor' : lambda x, y : max((x, y)),
        'sl'  : lambda x, y : x+((2**(y-1))-1),
        'sr'  : lambda x, y : x,
        'eq'  : lambda x, y : 1,
        'ne'  : lambda x, y : 1,
        'lt'  : lambda x, y : 1,
        'le'  : lambda x, y : 1,
        'gt'  : lambda x, y : 1,
        'ge'  : lambda x, y : 1,
        }
        return bit_function[self.function](self.a.get_bits(), self.b.get_bits())

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        self.b.write_code(plugin)
        plugin.write_binary(self)
