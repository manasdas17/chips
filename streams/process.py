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

def is_process(thing):
    if hasattr(thing, "what_are_you"):
        if thing.what_are_you() == 'Process':
            return True
    return False

def is_loop(thing):
    if hasattr(thing, "what_are_you"):
        if thing.what_are_you() == 'Loop':
            return True
    return False

class Instruction:

    def get_enclosing_process(self):
        if is_process(self.parent):
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.get_enclosing_process()
        else:
            raise SyntaxError()

    def get_enclosing_loop(self):
        if is_loop(self.parent):
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.get_enclosing_loop()
        else:
            raise SyntaxError()

class Variable(Unique):

    def __init__(self, initial):
        self.initial = initial
        Unique.__init__(self)

    def set(self, value):
        return Set(self, value)

    def get_bits(self):
        return self.parent.get_bits()

    def __repr__(self):
        return "Variable({0})".format(self.initial)

class Set(Unique, Instruction):

    def __init__(self, variable, other):
        Unique.__init__(self)
        self.variable = variable
        self.other = other

    def write_code(self, plugin): 
        return plugin.write_set(self)

    def __repr__(self):
        return "Set({0}, {1})".format(self.variable, self.other)

class Output(Stream, Unique):

    def __init__(self):
        Unique.__init__(self)

    def write(self, variable): 
        return Write(self, variable)

    def get_bits(self):
        return self.parent.get_bits()

    def write_code(self, plugin): 
        pass

    def __repr__(self):
        return "Output()"

class Write(Unique, Instruction):

    def __init__(self, outstream, variable):
        Unique.__init__(self)
        self.outstream = outstream
        self.variable = variable

    def write_code(self, plugin): 
        return plugin.write_write(self)

    def __repr__(self):
        return "Write({0}, {1})".format(self.outstream, self.variable)

class Break(Unique, Instruction):

    def __init__(self):
        Unique.__init__(self)

    def write_code(self, plugin): 
        return plugin.write_break(self)

    def __repr__(self):
        return "Break()"

class Loop(Unique, Instruction):

    def __init__(self, *instructions):
        Unique.__init__(self)

        for child in instructions:
            child.parent = self

        self.instructions = instructions
        for instruction, next_instruction in zip(instructions, instructions[1:]+instructions[:1]):
                instruction.next_instruction = next_instruction

    def write_code(self, plugin): 
        return plugin.write_loop(self)

    def what_are_you(self):
        return "Loop"

    def __repr__(self):
        return "Loop({0})".format(self.instructions)

class If(Unique, Instruction):
    pass
#
#    def __init__(self, predicate):
#        Unique.__init__(self)
#
#
#    def Then(self, *instructions):
#
#        for child in instructions:
#            child.parent = self
#
#        for instruction, next_instruction in zip(instructions, instructions[1:]):
#                instruction.next_instruction = next_instruction
#
#        instructions[-1].next_instruction = parent.next_instruction
#
#        self.consequent = instructions
#        return self #for method chaining
#
#    def Else(self, *instructions):
#        for child in instructions:
#            child.parent = self
#
#        for instruction, next_instruction in zip(instructions, instructions[1:]):
#                instruction.next_instruction = next_instruction
#        instructions[-1].next_instruction = parent.next_instruction
#
#        self.alternate = instructions
#        return self #for method chaining
#
#    def If(self, predicate): #for method chaining
#        _if = If(predicate)
#        _if.parent = self
#        return _if
#
#    def write_code(self, plugin): 
#        return plugin.write_if(self)
#
#    def what_are_you(self):
#        return "If"
#
#    def __repr__(self):
#        return "If({0}, {1})".format(self.condition, self.instructions)

class Process(Unique):

    def __init__(self, bits=8, inputs=(), outputs=(), variables=(), instructions=()):
        Unique.__init__(self)

        self.bits = bits
        self.inputs = inputs
        self.outputs = outputs
        self.variables = variables
        self.instructions = instructions

        for child in outputs + variables + instructions:
            child.parent = self

        for i in xrange(len(instructions)):
            if i == len(instructions)-1:
                instructions[i].next_instruction = instructions[i]
            else:
                instructions[i].next_instruction = instructions[i+1]

    def get_bits(self):
        return self.bits

    def write_code(self, plugin): 
        for i in self.inputs:
            i.write_code(plugin)
        plugin.write_process(self)

    def what_are_you(self):
        return "Process"

    def __repr__(self):
        return '\n'.join([
            "Process(",
            "    bits = {0},".format(self.bits),
            "    inputs = {0},".format(self.inputs),
            "    outputs = {0},".format(self.outputs),
            "    variables = {0},".format(self.variables),
            "    instructions = {0},".format(self.instructions),
            ")"
        ])
