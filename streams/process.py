#!/usr/bin/env python

"""Primitive Operations for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from common import Unique, Stream

class Expression:
    def __add__(self, other): return BinaryExpression(self, other, 'add')
    def __sub__(self, other): return BinaryExpression(self, other, 'sub')
    def __mul__(self, other): return BinaryExpression(self, other, 'mul')
    def __mod__(self, other): return BinaryExpression(self, other, 'mod')
    def __floordiv__(self, other): return BinaryExpression(self, other, 'div')
    def __and__(self, other): return BinaryExpression(self, other, 'and')
    def __or__(self, other): return BinaryExpression(self, other, 'or')
    def __xor__(self, other): return BinaryExpression(self, other, 'xor')
    def __rshift__(self, other): return BinaryExpression(self, other, 'sr')
    def __lshift__(self, other): return BinaryExpression(self, other, 'sl')
    def __eq__(self, other): return BinaryExpression(self, other, 'eq')
    def __ne__(self, other): return BinaryExpression(self, other, 'ne')
    def __gt__(self, other): return BinaryExpression(self, other, 'gt')
    def __ge__(self, other): return BinaryExpression(self, other, 'ge')
    def __lt__(self, other): return BinaryExpression(self, other, 'lt')
    def __le__(self, other): return BinaryExpression(self, other, 'le')

class  BinaryExpression(Expression):

    def __init__(self, a, b, function):
        self.a, self.b, self.function = a, b, function
        Stream.__init__(self)

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
        plugin.write_binary_expression(self)

class Variable(Unique):

    def __init__(self, process, initial):
        self.initial = initial
        self.process = process
        Unique.__init__(self)

    def set(self, value):
        return Set(self, value)

    def get(self, value):
        return Get(self)

    def get_bits(self):
        return self.process.get_bits()

class Set(Unique):

    def __init__(self, variable, other):
        Unique.__init__(self)
        self.variable = variable
        self.other = other

    def write_code(self, plugin): 
        plugin.write_get(self)

class OutStream(Stream, Unique):

    def __init__(self, process):
        Unique.__init__(self)
        self.process = process

    def write(self, variable): 
        return Write(self, variable)

    def get_bits(self):
        return self.process.get_bits()

    def write_code(self, plugin): 
        pass

class Write(Unique):

    def __init__(self, outstream, variable):
        Unique.__init__(self)
        self.outstream = outstream
        self.variable = variable

    def write_code(self, plugin): 
        return plugin.write_write(self)

class Process(Unique):

    def __init__(self, bits):
        self.bits = bits
        self.variables = []
        self.instreams = []
        self.outstreams = []
        Unique.__init__(self)

    def variable(self, initial): 
        v = Variable(self, initial)
        self.variables.append(v)
        return v

    def outstream(self): 
        o = OutStream(self)
        self.outstreams.append(o)
        return o

    def procedure(self, *instructions): 
        self.instructions = instructions
        for i in xrange(len(instructions)):
            if i == len(instructions)-1:
                instructions[i].next_instruction = instructions[i]
            else:
                instructions[i].next_instruction = instructions[i+1]

    def get_bits(self):
        return self.bits

    def write_code(self, plugin): 
        for i in self.instructions:
            if hasattr(i, 'instream'):
                i.instream.write_code(plugin)
        plugin.write_process(self)
