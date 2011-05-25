#!/usr/bin/env python
"""VHDL generation of processes"""

from math import ceil, log
from chips.common import calculate_jumps

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


def resize(val, bits):
    mask_bits = (2**(bits-1))-1
    return val | ~mask_bits if val < 0 else val & mask_bits

def address_bits(length):
    if length <= 1:
        return 1
    else:
        return int(ceil(log(length, 2)))

def write_process(process, plugin):

#############################################################################
#CALCULATE PROCESS PARAMETERS
#############################################################################
    process_instructions = calculate_jumps(tuple(process.instructions))
    operations = ["OP_DIV", "OP_MOD", "OP_MUL", "OP_ADD", "OP_SUB",
            "OP_BAND", "OP_BOR", "OP_BXOR", "OP_SL", "OP_SR", "OP_EQ",
            "OP_NE", "OP_GE", "OP_GT", "OP_WAIT_US", "OP_JMP", "OP_JMPF",
            "OP_MOVE", "OP_IMM", "OP_ABS", "OP_LNOT", "OP_INVERT"]

    left_shifts = []
    right_shifts = []
    availables = []

    for i in process_instructions:
        if i.operation.startswith("OP_SLN_"):
            if i.operation not in operations:
                operations.append(i.operation)
                left_shifts.append(int(i.operation[7:]))

    for i in process_instructions:
        if i.operation.startswith("OP_SRN_"):
            if i.operation not in operations:
                operations.append(i.operation)
                right_shifts.append(int(i.operation[7:]))

    for i in process_instructions:
        if i.operation.startswith("OP_AVAILABLE_"):
            if i.operation not in operations:
                input_ident = int(i.operation[13:])
                operations.append(i.operation)
                availables.append(input_ident)

    #calculate processor parameters
    number_of_operations = (
        len(operations) + 
        len(process.inputs) + 
        len(process.outputs)
    )
    process_id = process.get_identifier()
    process_bits = process.get_bits()
    num_instructions = len(process_instructions)
    registers = (
        [i.srca for i in process_instructions] + 
        [i.srcb for i in process_instructions]
    )
    num_registers = max([0] +registers) + 1
    instruction_address_bits = address_bits(num_instructions)
    register_address_bits = address_bits(num_registers)
    num_registers = 2**register_address_bits
    operation_bits = address_bits(number_of_operations)
    instruction_bits = (
        operation_bits + 
        register_address_bits + 
        max((register_address_bits, process_bits))
    )

#############################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR READING INPUT STREAMS
#############################################################################

    input_instructions = []
    for i in process.inputs:
        input_instructions.extend([
"          case OP_READ_{0}_{1}:".format(i.get_identifier(), process_id),
"            if (buffer_{0}.stalled)".format(i.get_identifier()),
"            {",
"              buffer_{0} = get_stream_{0}();".format(i.get_identifier()),
"            }",
"            if (!buffer_{0}.stalled)".format(i.get_identifier()),
"            {",
"              registers_{0}[instruction.srca] = buffer_{1}.value;".format(process_id, i.get_identifier()),
"              pc_{0}++;".format(process_id),
"            }",
"            buffer_{0}.stalled = true;".format(i.get_identifier()),
"            break;",
        ])
        operations.append("OP_READ_{0}".format(i.get_identifier()))

################################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR WRITING OUTPUT STREAMS
################################################################################

    output_instructions = []
    for i in process.outputs:
        output_instructions.extend([
"          case OP_WRITE_{0}_{1}:".format(i.get_identifier(), process_id),
"            if (output_{0}.stalled)".format(i.get_identifier()),
"            {",
"              output_{0}.stalled = false;".format(i.get_identifier()),
"              output_{0}.value = rega;".format(i.get_identifier()),
"              pc_{0}++;".format(process_id),
"            }",
"            break;",
        ])
        operations.append("OP_WRITE_{0}".format(i.get_identifier()))


    ls_instructions = []
    for i in left_shifts:
        output_instructions.extend([
"        case OP_SLN_{0}_{1}:".format(i, process_id),
"            result = resize(rega<<{0}, {1}); ".format(i, process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
        ])

    rs_instructions = []
    for i in right_shifts:
        output_instructions.extend([
"        case OP_SRN_{0}_{1}:".format(i, process_id),
"            result = resize(rega>>{0}, {1}); ".format(i, process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
        ])

    available_instructions = []
    for i in availables:
        available_instructions.extend([
"        case OP_AVAILABLE_{0}_{1}:".format(i, process_id),
"            if (buffer_{0}.stalled)".format(i),
"            {",
"              buffer_{0} = get_stream_{0}();".format(i),
"            }",
"            if (buffer_{0}.stalled)".format(i),
"            {",
"              result = resize(0, {0}); ".format(process_bits),
"            } else {",
"              result = resize(-1, {0}); ".format(process_bits),
"            }",
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
        ])


################################################################################
#GENERATE INSTRUCTION CONSTANTS

    definitions = []
    declarations = []
    execute = []

    instructions = []
    for index, instruction in enumerate(process_instructions):
        operation = instruction.operation
        srca = instruction.srca if instruction.srca else 0
        srcb = instruction.srcb if instruction.srcb else 0
        immediate = instruction.immediate if instruction.immediate else 0
        if instruction is process_instructions[-1]:
            base_string = "  {7}{0}_{1}, {2}, {3}, {4}{8} //file: {5} line: {6}"
        else:
            base_string = "  {7}{0}_{1}, {2}, {3}, {4}{8}, //file: {5} line: {6}"
        instructions.append(
            base_string.format(
                operation, 
                process_id,
                srca,
                srcb,
                immediate,
                instruction.filename,
                instruction.lineno,
                "{",
                "}",
            )
        )
    instructions = "\n".join(instructions)

    for index, operation in enumerate(operations):
        definitions.append(
"const int {0}_{1} = {2};".format(
                operation, 
                process_id,
                index
            )
        )

################################################################################

    declarations.append("void execute_{0}();".format(process_id))
    execute.append("execute_{0}();".format(process_id))
    definitions.extend([
"struct instruction_type_{0} ".format(process_id, num_instructions),
"{",
"  int operation;",
"  int srca;",
"  int srcb;" ,
"  int immediate;",
"};",
"",
"instruction_type_{0} instructions_{0} [{1}] = ".format(process_id, num_instructions),
"{",
instructions,
"};",
"",
"//Process",
"",
"int pc_{0} = 0;".format(process_id),
"int registers_{0}[{1}];".format(process_id, num_registers),
"",
"void execute_{0}()".format(process_id),
"{",
"    instruction_type_{0} instruction = instructions_{0}[pc_{0}];".format(process_id),
"    data_type data;",
"    int result = 0;",
"    int rega = registers_{0}[instruction.srca];".format(process_id),
"    int regb = registers_{0}[instruction.srcb];".format(process_id),
"    switch(instruction.operation)",
"    {",
"        case OP_ABS_{0}:".format(process_id),
"            result = resize(abs(rega), {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_LNOT_{0}:".format(process_id),
"            result = resize(not rega, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_INVERT_{0}:".format(process_id),
"            result = resize(~rega, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_DIV_{0}:".format(process_id),
"            result = resize(rega/regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_MOD_{0}:".format(process_id),
"            result = resize(rega%regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_MUL_{0}:".format(process_id),
"            result = resize(rega*regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_ADD_{0}:".format(process_id),
"            result = resize(rega+regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_SUB_{0}:".format(process_id),
"            result = resize(rega-regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_BAND_{0}:".format(process_id),
"            result = resize(rega&regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_BOR_{0}:".format(process_id),
"            result = resize(rega|regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_BXOR_{0}:".format(process_id),
"            result = resize(rega^regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_SL_{0}:".format(process_id),
"            result = resize(rega<<regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_SR_{0}:".format(process_id),
"            result = resize(rega>>regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_EQ_{0}:".format(process_id),
"            result = -resize(rega==regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_NE_{0}:".format(process_id),
"            result = -resize(rega!=regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_GE_{0}:".format(process_id),
"            result = -resize(rega>=regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_GT_{0}:".format(process_id),
"            result = -resize(rega>regb, {0}); ".format(process_bits),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_WAIT_US_{0}:".format(process_id),
"            break;",
"        case OP_JMP_{0}:".format(process_id),
"            pc_{0} = instruction.immediate;".format(process_id),
"            break;",
"        case OP_JMPF_{0}:".format(process_id),
"            if (rega==0)",
"            {",
"              pc_{0} = instruction.immediate;".format(process_id),
"            }",
"            else",
"            {",
"              pc_{0}++;".format(process_id),
"            }",
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_MOVE_{0}:".format(process_id),
"            result = regb;".format(process_id),
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"        case OP_IMM_{0}:".format(process_id),
"            result = instruction.immediate;",
"            pc_{0}++;".format(process_id),
"            registers_{0}[instruction.srca] = result;".format(process_id),
"            break;",
"\n".join(input_instructions),
"\n".join(output_instructions),
"\n".join(ls_instructions),
"\n".join(rs_instructions),
"\n".join(available_instructions),
"        default:",
"            break;",
"    }",
"}"
    ])

    return declarations, definitions, execute
