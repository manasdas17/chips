#!/usr/bin/env python
"""VHDL generation of process instructions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import common

temp = 0

def write_write(instruction, plugin):
    stream = instruction.outstream.get_identifier()
    process = instruction.variable.parent.get_identifier()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier())
           ]
    idef = [
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        STREAM_{0} <= VARIABLE_{1};".format(stream, variable),
"        STREAM_{0}_STB <= '1';".format(stream),
"        if STREAM_{0}_ACK = '1' then".format(stream),
"          STREAM_{0}_STB <= '0';".format(stream),
"          STATE_{0} <= INSTRUCTION_{1}_0;".format(process, next_instruction),
"        end if;",
           ]

    return idec, idef

def write_read(instruction, plugin):
    stream = instruction.instream.get_identifier()
    process = instruction.variable.parent.get_identifier()
    process_bits = instruction.variable.parent.get_bits()
    variable = instruction.variable.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier()),
"INSTRUCTION_{0}_1".format(instruction.get_identifier())
           ]
    idef = [
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        VARIABLE_{0} <= STD_RESIZE(STREAM_{1}, {2});".format(variable, stream, process_bits),
"        if STREAM_{0}_STB = '1' then".format(stream),
"          STREAM_{0}_ACK <= '1';".format(stream),
"          STATE_{0} <= INSTRUCTION_{1}_1;".format(process, instruction.get_identifier()),
"        end if;",
"      when INSTRUCTION_{0}_1 =>".format(instruction.get_identifier()),
"        STREAM_{0}_ACK <= '0';".format(stream),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process, next_instruction),
           ]

    return idec, idef

def write_set(instruction, plugin):
    process = instruction.get_enclosing_process()
    variable = instruction.variable.get_identifier()
    other = instruction.other.get_identifier()
    next_instruction = instruction.next_instruction.get_identifier()

    idec = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier()),
           ]
    idef = [
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        VARIABLE_{0} <= VARIABLE_{1};".format(variable, other),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), next_instruction),
           ]

    return idec, idef

def write_constant(instruction, plugin):
    global temp
    temp = instruction.get_identifier()
    process = instruction.get_enclosing_process()
    next_instruction = instruction.next_instruction.get_identifier()

    plugin.declarations.append(
"  signal TEMP_{0} : std_logic_vector({1} downto 0);".format(temp, process.get_bits()),
           )
    idec = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier()),
           ]
    idef = [
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        TEMP_{0} <= {1};".format(temp, common.binary(instruction.value, process.get_bits())),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), next_instruction),
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
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), next_instruction),
    ]

    ideclarations = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier()),
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
"      when INSTRUCTION_{0}_0 =>".format(instruction.get_identifier()),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), loop.next_instruction.get_identifier()),
    ]

    ideclarations = [
"INSTRUCTION_{0}_0".format(instruction.get_identifier()),
    ]

    return ideclarations, idefinitions

def write_if(instruction, plugin):
    global temp

    process = instruction.get_enclosing_process()

    ideclarations = []
    idefinitions = []
    for index, conditional in enumerate(instruction.conditionals):
        last_conditional = conditional is instruction.conditionals[-1]

        condition, instructions = conditional

        ideclarations.extend([
"INSTRUCTION_{0}_{1}".format(instruction.get_identifier(), 2*index),
"INSTRUCTION_{0}_{1}".format(instruction.get_identifier(), 2*index+1),
        ])

        if condition == "true":#Else jump to the first instruction whatever
            first_instruction = instructions[0].get_identifier()
            idefinitions.extend([
"      --Else",
"      when INSTRUCTION_{0}_{1} =>".format(instruction.get_identifier(), 2*index + 1),
"        STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), first_instruction),
            ])
        else:
            for i in condition:
                idec, idef = i.write_code(plugin)
                idefinitions.extend(idef)
                ideclarations.extend(idec)

            first_instruction = instructions[0].get_identifier()

            if last_conditional:
                idefinitions.extend([
"      --{0}".format("If" if index == 0 else "Elsif"),
"      when INSTRUCTION_{0}_{1} =>".format(instruction.get_identifier(), 2*index + 1),
'        if NE(TEMP_{0}, "00") then'.format(temp),
"          STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), first_instruction),
"        else",
#this is the last conditional clause, nothing else to try
"          STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), instruction.next_instruction.get_identifier()),
"        end if;",
"      --Then",
                ])
            else:
                idefinitions.extend([
"      --{0}".format("If" if index == 0 else "Elsif"),
"      when INSTRUCTION_{0}_{1} =>".format(instruction.get_identifier(), 2*index + 1),
'        if NE(TEMP_{0}, "00") then'.format(temp),
"          STATE_{0} <= INSTRUCTION_{1}_0;".format(process.get_identifier(), first_instruction),
"        else",
#go to the next conditional claue
"          STATE_{0} <= INSTRUCTION_{1}_{2};".format(process.get_identifier(), 2*index + 2),
"        end if;",
"      --Then",
                ])


        for i in instructions:
            idec, idef = i.write_code(plugin)
            idefinitions.extend(idef)
            ideclarations.extend(idec)

    idefinitions.extend([
"      --End if",
    ])

    return ideclarations, idefinitions
