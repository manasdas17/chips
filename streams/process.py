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

#class Write(Unique, Instruction):
#
#    def __init__(self, outstream, variable):
#        Unique.__init__(self)
#        self.outstream = outstream
#        self.variable = variable
#
#    def write_code(self, plugin): 
#        return plugin.write_write(self)
#
#    def __repr__(self):
#        return "Write({0}, {1})".format(self.outstream, self.variable)

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
