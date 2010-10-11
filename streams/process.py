#!/usr/bin/env python

"""Primitive Operations for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from common import Unique
from instruction import Write, Block
from inspect import currentframe, getsourcefile

class Process(Unique):

    def __init__(self, bits=8, *instructions):
        Unique.__init__(self)
        self.bits = bits
        self.instructions = Block(instructions)
        self.variables = []
        self.inputs = []
        self.outputs = []
        self.timeouts = {}
        self.timer_number = 0
        for i in instructions:
            i.set_process(self)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

    def is_process(self):
        return True

    def get_bits(self):
        return self.bits

    def write_code(self, plugin): 
        if not self in plugin.processes:
            plugin.processes.append(self)
            for i in self.inputs:
                i.write_code(plugin)
            plugin.write_process(self)

    def __repr__(self):
        return '\n'.join([
            "Process(",
            "    bits = {0},".format(self.bits),
            "    instructions = {0},".format(self.instructions),
            ")"
        ])
