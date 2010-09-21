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
    process = instruction.variable.parent.get_identifier()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}".format(instruction.get_identifier())
           ]
    idef = [
"      when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"        STREAM_{0} <= VARIABLE_{1};".format(stream, variable),
"        STREAM_{0}_STB <= '1';".format(stream),
"        if STREAM_{0}_ACK = '1' then".format(stream),
"          STREAM_{0}_STB <= '0';".format(stream),
"          STATE_{0} <= INSTRUCTION_{1};".format(process, next_instruction),
"        end if;",
           ]

    return idec, idef

def write_read(instruction):
    stream = instruction.instream.get_identifier()
    process = instruction.variable.parent.get_identifier()
    process_bits = instruction.variable.parent.get_bits()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}".format(instruction.get_identifier()),
"INSTRUCTION_{0}_1".format(instruction.get_identifier())
           ]
    idef = [
"      when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"        VARIABLE_{0} <= STD_RESIZE(STREAM_{1}, {2});".format(variable, stream, process_bits),
"        if STREAM_{0}_STB = '1' then".format(stream),
"          STREAM_{0}_ACK <= '1';".format(stream),
"          STATE_{0} <= INSTRUCTION_{1}_1;".format(process, instruction.get_identifier()),
"        end if;",
"      when INSTRUCTION_{0}_1 =>".format(instruction.get_identifier()),
"        STREAM_{0}_ACK <= '0';".format(stream),
"        STATE_{0} <= INSTRUCTION_{1};".format(process, next_instruction),
           ]

    return idec, idef

def write_set(instruction):
    process = instruction.get_enclosing_process()
    variable = instruction.variable.get_identifier()
    other = instruction.other.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}".format(instruction.get_identifier()),
           ]
    idef = [
"      when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"        VARIABLE_{0} <= VARIABLE_{1};".format(variable, other),
"        STATE_{0} <= INSTRUCTION_{1};".format(process.get_identifier(), next_instruction),
           ]

    return idec, idef

def write_loop(instruction, plugin):

    process = instruction.get_enclosing_process()

    if instruction.instructions:
        next_instruction = instruction.instructions[0].get_identifier()
    else:
        next_instruction = instruction.get_identifier()

    idefinitions = [
"      --Loop",
"      when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"        STATE_{0} <= INSTRUCTION_{1};".format(process.get_identifier(), next_instruction),
    ]

    ideclarations = [
"INSTRUCTION_{0}".format(instruction.get_identifier()),
    ]
    for i in instruction.instructions:
        idec, idef = i.write_code(plugin)
        idefinitions.extend(idef)
        ideclarations.extend(idec)
    idefinitions.extend([
"      --End Loop",
    ])

    return ideclarations, idefinitions

def write_break(instruction, plugin):

    process = instruction.get_enclosing_process()
    loop = instruction.get_enclosing_loop()

    idefinitions = [
"      --Break",
"      when INSTRUCTION_{0} =>".format(instruction.get_identifier()),
"        STATE_{0} <= INSTRUCTION_{1};".format(process.get_identifier(), loop.next_instruction.get_identifier()),
    ]

    ideclarations = [
"INSTRUCTION_{0}".format(instruction.get_identifier()),
    ]

    return ideclarations, idefinitions
