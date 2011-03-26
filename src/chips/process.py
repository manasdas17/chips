#!/usr/bin/env python

"""Primitive Operations for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from common import Unique, resize
from instruction import Write, Block
from inspect import currentframe, getsourcefile
from exceptions import StreamsConstructionError

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

class Process(Unique):

    def __init__(self, bits, *instructions):
        Unique.__init__(self)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.bits = int(bits)
        self.variables = []
        self.inputs = []
        self.outputs = []
        self.timeouts = {}
        self.timer_number = 0
        for i in instructions:
            i.set_process(self)
        for i in self.inputs:
            if hasattr(i, "receiver"):
                raise ChipConstructionError("stream allready has a receiver", self.filename, self.lineno)
            i.receiver = self
        self.receivers = {}
        self.transmitters = {}
        for i in self.inputs:
            self.transmitters[i.get_identifier()] = i
        for i in self.outputs:
            self.receivers[i.get_identifier()] = i
        self.instructions = tuple(Block(instructions))
        self.instruction_memory = dict(enumerate(self.instructions))

    def set_chip(self, chip):
        if self not in chip.processes:
            chip.processes.append(self)
            for i in self.inputs:
                i.set_chip(chip)

    def is_process(self):
        return True

    def get_bits(self):
        return self.bits

    def write_code(self, plugin): 
        plugin.write_process(self)

    def reset(self):

        self.registers = {}
        self.pc = 0

    def execute(self):
        instruction = self.instruction_memory[self.pc]
        if instruction.operation == "OP_ADD":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega+regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_SUB":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega-regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_MUL":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega*regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_DIV":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(c_style_division(rega, regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_MOD":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(c_style_modulo(rega, regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_SL":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega<<regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_SR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega>>regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_BAND":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega&regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_BOR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega|regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_BXOR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega^regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_EQ":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(-int(rega==regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_NE":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(-int(rega!=regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_GT":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(-int(rega>regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_GE":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(-int(rega>=regb), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_MOVE":
            self.registers[instruction.srca] = self.registers[instruction.srcb]
            self.pc += 1
        elif instruction.operation == "OP_IMM":
            self.registers[instruction.srca] = instruction.immediate
            self.pc += 1
        elif instruction.operation == "OP_JMP":
            self.pc = instruction.immediate
        elif instruction.operation == "OP_JMPF":
            if self.registers[instruction.srca]:
                self.pc += 1
            else:
                self.pc = instruction.immediate
        elif instruction.operation.startswith("OP_WRITE"):
            key = instruction.operation[9:]
            receiver = self.receivers[key]
            data = self.registers[instruction.srca]
            receiver.put(resize(data, self.bits))
            self.pc += 1
        elif instruction.operation.startswith("OP_READ"):
            key = instruction.operation[8:]
            transmitter = self.transmitters[key]
            read_data = transmitter.get()
            if read_data is not None:
                self.registers[instruction.srca] = resize(read_data, self.bits)
                self.pc += 1

    def __repr__(self):
        return '\n'.join([
            "Process(",
            "    bits = {0},".format(self.bits),
            "    instructions = {0},".format(self.instructions),
            ")"
        ])
