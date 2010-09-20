#!/usr/bin/env python
"""VHDL generation of process instructions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"


def write_write(instruction):
    stream = instruction.outstream.get_identifier()
    process = instruction.variable.process.get_identifier()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}".format(instruction.get_identifier())
           ]
    idef = [
"     when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"       STREAM_{0} <= VARIABLE_{1};".format(stream, variable),
"       STREAM_{0}_STB <= '1';".format(stream),
"       if STREAM_{0}_ACK = '1' then".format(stream),
"         STREAM_{0}_STB <= '0';".format(stream),
"         STATE_{0} <= INSTRUCTION_{1};".format(process, next_instruction),
"       end if;",
           ]

    return idec, idef

def write_read(instruction):
    stream = instruction.instream.get_identifier()
    process = instruction.variable.process.get_identifier()
    process_bits = instruction.variable.process.get_bits()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}".format(instruction.get_identifier()),
"INSTRUCTION_{0}_1".format(instruction.get_identifier())
           ]
    idef = [
"     when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"       VARIABLE_{0} <= STD_RESIZE(STREAM_{1}, {2});".format(variable, stream, process_bits),
"       if STREAM_{0}_STB = '1' then".format(stream),
"         STREAM_{0}_ACK <= '1';".format(stream),
"         STATE_{0} <= INSTRUCTION_{1}_1;".format(process, instruction.get_identifier()),
"       end if;",
"     when INSTRUCTION_{0}_1 =>".format(instruction.get_identifier()),
"       STREAM_{0}_ACK <= '0';".format(stream),
"       STATE_{0} <= INSTRUCTION_{1};".format(process, next_instruction),
           ]

    return idec, idef
