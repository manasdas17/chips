#!/usr/bin/env python
"""VHDL generation of processes"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import common
from math import ceil, log

def address_bits(length):
    if length == 0:
        return 1
    else:
        return int(ceil(log(length, 2)))

def write_process(process, plugin):

################################################################################
#CALCULATE PROCESS PARAMETERS
################################################################################
    states = ["STALL", "EXECUTE", "DIVIDE_0"]
    operations = [
      "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV", "OP_BAND", "OP_BOR", "OP_BXOR", 
      "OP_SL", "OP_SR", "OP_EQ", "OP_NE", "OP_GT", "OP_GE", "OP_JMP", "OP_JMPF", 
      "OP_IMM"
    ]
    number_of_operations = len(operations) + len(process.inputs) + len(process.outputs)
    process_id = process.get_identifier()
    process_bits = process.get_bits()
    num_instructions = len(process.instructions)
    registers = [i.srca for i in process.instructions] + [i.srcb for i in process.instructions]
    num_registers = max([0] +registers) + 1
    instruction_address_bits = address_bits(num_instructions)
    register_address_bits = address_bits(num_registers)
    operation_bits = address_bits(number_of_operations)
    instruction_bits = operation_bits + register_address_bits + max((register_address_bits, process_bits))

################################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR READING INPUT STREAMS
################################################################################

    reset_streams = []
    read_inputs = []
    input_instructions = []
    for i in process.inputs:
        read_inputs.extend([
"      when READ_STREAM_{0} =>".format(i.get_identifier()),
"        if STREAM_{0}_STB = '1' then".format(i.get_identifier()),
"          STREAM_{0}_ACK <= '1';".format(i.get_identifier()),
"          REGISTERS_{0}(to_integer(unsigned(SRCA_{0}))) <= STD_RESIZE(STREAM_{1}, {2});".format(process_id, i.get_identifier(), process_bits),
"          STATE_{0} <= ACK_STREAM_{1};".format(process.get_identifier(), i.get_identifier()),
"        end if;",
"      when ACK_STREAM_{0} =>".format(i.get_identifier()),
"        STREAM_{0}_ACK <= '0';".format(i.get_identifier()),
"        STATE_{0} <= EXECUTE_{0};".format(process.get_identifier()),
        ])
        input_instructions.extend([
"          when OP_READ_{0}_{1} =>".format(i.get_identifier(), process_id),
"            STATE_{0} <= READ_STREAM_{1};".format(process_id, i.get_identifier()),
"            PC_{0} <= PC_{0};".format(process_id),
"            RESULT := REGA;".format(process_id),
        ])
        operations.append("OP_READ_{0}".format(i.get_identifier()))
        states.append("READ_STREAM_{0}".format(i.get_identifier()))
        states.append("ACK_STREAM_{0}".format(i.get_identifier()))
        reset_streams.append(
"      STREAM_{0}_ACK <= '0';".format(i.instream.get_identifier()),
        )

################################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR WRITEING OUTPUT STREAMS
################################################################################

    write_outputs = []
    output_instructions = []
    for i in process.outputs:
        plugin.declarations.extend([
"  signal STREAM_{0}       : std_logic_vector({1} downto 0);".format(i.get_identifier(), i.get_bits()-1),
"  signal STREAM_{0}_STB   : std_logic;".format(i.get_identifier()),
"  signal STREAM_{0}_ACK   : std_logic;".format(i.get_identifier()),
        ])
        write_outputs.extend([
"      when WRITE_STREAM_{0} =>".format(i.get_identifier()),
"        STREAM_{0}_STB <= '1';".format(i.get_identifier()),
"        STREAM_{0} <= STD_RESIZE(REGA, {1});".format(i.get_identifier(), i.get_bits()),
"        if STREAM_{0}_ACK = '1' then".format(i.get_identifier()),
"          STREAM_{0}_STB <= '0';".format(i.get_identifier()),
"          STATE_{0} <= EXECUTE;".format(process.get_identifier(), i.get_identifier()),
"        end if;",
        ])
        output_instructions.extend([
"          when OP_WRITE_{0}_{1} =>".format(i.get_identifier(), process_id),
"            STATE_{0} <= WRITE_STREAM_{1};".format(process_id, i.get_identifier()),
"            PC_{0} <= PC_{0};".format(process_id),
"            RESULT := REGA;".format(process_id),
        ])
        operations.append("OP_WRITE_{0}".format(i.get_identifier()))
        states.append("WRITE_STREAM_{0}".format(i.get_identifier()))
        reset_streams.append(
"      STREAM_{0}_STB <= '0';".format(i.get_identifier()),
        )

################################################################################
#GENERATE INSTRUCTION CONSTANTS
################################################################################

    instructions = []
    for index, instruction in enumerate(process.instructions):
        operation = instruction.operation
        srca = instruction.srca if instruction.srca else 0
        srcb = instruction.srcb if instruction.srcb else 0
        immediate = instruction.immediate if instruction.immediate else 0
        instructions.append(
            "{0} => {1}_{2} & {3} & {4}".format(
                index, 
                operation, 
                process_id,
                common.binary(srca, register_address_bits),
                common.binary(immediate | srcb, process_bits)
            )
        )

    for index, operation in enumerate(operations):
        plugin.declarations.append(
"  constant {0}_{1} : std_logic_vector({2} downto 0) := {3};".format(
                operation, process_id, operation_bits-1, common.binary(index, operation_bits)
            )
        )

################################################################################
#GENERATE PROCESS DECLARATIONS
################################################################################

    plugin.declarations.extend([
"  type PROCESS_{0}_STATE_TYPE is ({1});".format(process.get_identifier(), ', '.join(states)),
"  type INSTRUCTIONS_TYPE_{0}  is array (0 to {1}) of std_logic_vector({2} downto 0);".format(process_id, num_instructions-1, instruction_bits-1),
"  type REGISTERS_TYPE_{0}     is array (0 to {1}) of std_logic_vector({2} downto 0);".format(process_id, num_registers-1, process_bits-1),
"  signal STATE_{0}        : PROCESS_{0}_STATE_TYPE;".format(process.get_identifier()),
"  signal REGISTERS_{0}    : REGISTERS_TYPE_{0};".format(process_id),
"  signal PC_{0}           : unsigned({1} downto 0);".format(process_id, instruction_address_bits - 1),
"  signal OPERATION_{0}    : std_logic_vector({1} downto 0);".format(process_id, operation_bits-1),
"  signal SRCA_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal SRCB_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal IMMEDIATE_{0}    : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal ZERO_{0}         : std_logic;".format(process_id),
"  signal INSTRUCTIONS_{0} : INSTRUCTIONS_TYPE_{0} := (\n{1});".format(process_id, ',\n'.join(instructions)),
    ])
    


################################################################################
#GENERATE PROCESS DEFINITIONS
################################################################################

    operation_hi = instruction_bits-1
    operation_lo = operation_hi-operation_bits+1
    srca_hi = operation_lo-1
    srca_lo = srca_hi-register_address_bits+1
    srcb_hi = srca_lo-1
    srcb_lo = srcb_hi-register_address_bits+1
    immediate_hi = srcb_hi
    immediate_lo = 0

    plugin.definitions.extend([
"  -- process",
"  process",
"    variable INSTRUCTION : std_logic_vector({1} downto 0);".format(process_id, instruction_bits-1),
"  begin",
"    wait until rising_edge(CLK);",
"    INSTRUCTION := INSTRUCTIONS_{0}(to_integer(PC_{0}));".format(process_id),
"    OPERATION_{0} <= INSTRUCTION({1} downto {2});".format(process_id, operation_hi, operation_lo), 
"    SRCA_{0}      <= INSTRUCTION({1} downto {2});".format(process_id, srca_hi, srca_lo), 
"    SRCB_{0}      <= INSTRUCTION({1} downto {2});".format(process_id, srcb_hi, srcb_lo), 
"    IMMEDIATE_{0} <= INSTRUCTION({1} downto {2});".format(process_id, immediate_hi, immediate_lo), 
"  end process;",
"",
"  process",
"    variable REGA    : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"    variable REGB    : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"    variable RESULT  : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"    variable FLAG_EQ : std_logic;".format(process_id),
"    variable FLAG_NE : std_logic;".format(process_id),
"    variable FLAG_GT : std_logic;".format(process_id),
"    variable FLAG_GE : std_logic;".format(process_id),
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(process_id),
"      when STALL =>",
"        PC_{0} <= PC_{0} + 1;".format(process_id),
"        STATE_{0} <= EXECUTE;".format(process_id),
"      when EXECUTE =>",
"        PC_{0} <= PC_{0} + 1;".format(process_id),
"",
"        --fetch register operands",
"        REGA := REGISTERS_{0}(to_integer(unsigned(SRCA_{0})));".format(process_id),
"        REGB := REGISTERS_{0}(to_integer(unsigned(SRCB_{0})));".format(process_id),
"",
"        --share comparator logic",
"        if REGA = REGB then".format(process_id),
"          FLAG_EQ := '1';".format(process_id),
"        else",
"          FLAG_EQ := '0';".format(process_id),
"        end if;",
"",
"        if signed(REGA) > signed(REGB) then".format(process_id),
"          FLAG_GT := '1';".format(process_id),
"        else",
"          FLAG_GT := '0';".format(process_id),
"        end if;",
"",
"        FLAG_NE := not FLAG_EQ;".format(process_id),
"        FLAG_GE := FLAG_GT or FLAG_EQ;".format(process_id),
"",
"        --execute instructions",
"        case OPERATION_{0} is".format(process_id),
"          when OP_MUL_{0}  => RESULT := STD_RESIZE( MUL(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_ADD_{0}  => RESULT := STD_RESIZE( ADD(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_SUB_{0}  => RESULT := STD_RESIZE( SUB(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_BAND_{0} => RESULT := STD_RESIZE(BAND(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_BOR_{0}  => RESULT := STD_RESIZE( BOR(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_BXOR_{0} => RESULT := STD_RESIZE(BXOR(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_SL_{0}   => RESULT := STD_RESIZE(  SL(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_SR_{0}   => RESULT := STD_RESIZE(  SR(REGA, REGB), {0});".format(process_id, process_bits),
"          when OP_EQ_{0}   => RESULT := (others => FLAG_EQ);".format(process_id),
"          when OP_NE_{0}   => RESULT := (others => FLAG_NE);".format(process_id),
"          when OP_GT_{0}   => RESULT := (others => FLAG_GT);".format(process_id),
"          when OP_GE_{0}   => RESULT := (others => FLAG_GE);".format(process_id),
"          when OP_IMM_{0}  => RESULT := IMMEDIATE_{0};".format(process_id),
"          when OP_DIV_{0} =>".format(process_id),
"            STATE_{0} <= DIVIDE_0;".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id),
"            RESULT := REGA;",
"          when OP_JMP_{0} =>".format(process_id),
"            STATE_{0} <= STALL;".format(process_id),
"            PC_{0} <= resize(unsigned(IMMEDIATE_{0}), {1});".format(process_id, instruction_address_bits),
"            RESULT := REGA;",
"          when OP_JMPF_{0} =>".format(process_id),
"            if ZERO_{0} = '1' then".format(process_id),
"              STATE_{0} <= STALL;".format(process_id),
"              PC_{0} <= resize(unsigned(IMMEDIATE_{0}), {1});".format(process_id, instruction_address_bits),
"            end if;".format(process_id),
"            RESULT := REGA;",
'\n'.join(output_instructions),
'\n'.join(input_instructions),
"          when others => null;",
"        end case;",
"        --write back results",
"        REGISTERS_{0}(to_integer(unsigned(SRCA_{0}))) <= RESULT;".format(process_id),
"        if RESULT = {1} then".format(process_id, common.binary(0, process_bits)),
"          ZERO_{0} <= '1';".format(process_id),
"        else",
"          ZERO_{0} <= '0';".format(process_id),
"        end if;",
'\n'.join(read_inputs),
'\n'.join(write_outputs),
"      when DIVIDE_0 => STATE_{0} <= EXECUTE;".format(process_id),
"    end case;",
"    if RST = '1' then",
"      STATE_{0} <= STALL;".format(process_id),
"      PC_{0} <= {1};".format(process_id, common.binary(0, instruction_address_bits)),
"\n".join(reset_streams),
"    end if;",
"  end process;",
    ])

