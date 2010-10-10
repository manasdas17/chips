#!/usr/bin/env python
"""python generation of processes"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from collections import deque

def resize(val, bits):
    sign_bits = -(2**(bits-1))
    return val | sign_bits if val & sign_bits else val & ~sign_bits


class Process:

    def __init__(self, process):
        self.instructions = dict(enumerate(process.instructions))
        self.registers = {}
        self.pc = 0
        self.input_iterators={}
        self.output_queues={}
        self.bits = process.get_bits()
        for i in process.inputs:
            self.input_iterators[i.get_identifier()]=i.generator()
        for i in process.outputs:
            queue = deque()
            self.output_queues[i.get_identifier()]=queue
            def output():
                while True:
                    self.execute()
                    try:
                        yield queue.popleft()
                    except IndexError:
                        yield None
            i.generator = output

    def execute(self):
        instruction = self.instructions[self.pc]
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
            self.registers[instruction.srca] = resize(int((1.0*rega)/(1.0*regb)), self.bits)
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
            queue = self.output_queues[key]
            data = self.registers[instruction.srca]
            queue.append(resize(data, self.bits))
            self.pc += 1
        elif instruction.operation.startswith("OP_READ"):
            key = instruction.operation[8:]
            iterator = self.input_iterators[key]
            read_data = next(iterator)
            if read_data is not None:
                self.registers[instruction.srca] = resize(read_data, self.bits)
                self.pc += 1

