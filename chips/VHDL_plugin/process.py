#!/usr/bin/env python
"""VHDL generation of processes"""

import hazard_remover
import common
from math import ceil, log

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
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

################################################################################
#CALCULATE PROCESS PARAMETERS
################################################################################
    pc_to_execute_latency = 2
    register_to_execution_latency = 1

    process_instructions = tuple(process.instructions)
    process_instructions = hazard_remover.optimize(process_instructions)
    operations = []
    states = ["STALL", "EXECUTE"]
    left_shifts = []
    right_shifts = []
    availables = []

    #save logic by turning off features if not used
    for instruction in process_instructions:
        for j in ["OP_DIV", "OP_MOD", "OP_MUL", "OP_ADD", "OP_SUB", "OP_BAND",
                "OP_BOR", "OP_BXOR", "OP_SL", "OP_SR", "OP_EQ", "OP_NE", 
                "OP_GE", "OP_GT", "OP_WAIT_US", "OP_JMP", "OP_JMPF", "OP_MOVE",
                "OP_IMM", "OP_WAIT_US", "OP_LNOT", "OP_ABS", "OP_INVERT",
                "OP_NOOP"]:
            if instruction.operation == j:
                if j not in operations:
                    operations.append(j)
        if instruction.operation.startswith("OP_SLN_"):
            if instruction.operation not in operations:
                operations.append(instruction.operation)
            left_shifts.append(int(instruction.operation[7:]))
        if instruction.operation.startswith("OP_SRN_"):
            if instruction.operation not in operations:
                operations.append(instruction.operation)
            right_shifts.append(int(instruction.operation[7:]))
        if instruction.operation.startswith("OP_AVAILABLE_"):
            if instruction.operation not in operations:
                operations.append(instruction.operation)
                input_ident = int(instruction.operation[13:])
                availables.append(input_ident)
        if instruction.operation == "OP_DIV" or instruction.operation == "OP_MOD":
            if "DIVIDE_0" not in states:
                states.extend(["DIVIDE_0", "DIVIDE_1", "DIVIDE_2"])
        if instruction.operation == "OP_WAIT_US":
            if "WAIT_US" not in states:
                states.append("WAIT_US")

    #calculate processor parameters
    number_of_operations = len(operations) + len(process.inputs) + len(process.outputs)
    process_id = process.get_identifier()
    process_bits = process.get_bits()
    num_instructions = len(process_instructions)
    registers = [i.srca for i in process_instructions] + [i.srcb for i in process_instructions]
    num_registers = max([0] +registers) + 1
    instruction_address_bits = address_bits(num_instructions)
    register_address_bits = address_bits(num_registers)
    num_registers = 2**register_address_bits
    operation_bits = address_bits(number_of_operations)
    instruction_bits = operation_bits + register_address_bits + max((register_address_bits, process_bits))


################################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR READING INPUT STREAMS
################################################################################

    reset_streams = []
    read_inputs = []
    input_instructions = []
    for i in process.inputs:
        input_instructions.extend([
"          when OP_READ_{0}_{1} =>".format(i.get_identifier(), process_id),
"            STATE_{0} <= READ_STREAM_{1};".format(process_id, i.get_identifier()),
"            PC_{0} <= PC_{0};".format(process_id),
        ])
        read_inputs.extend([
"      when READ_STREAM_{0} =>".format(i.get_identifier()),
"        if STREAM_{0}_STB = '1' then".format(i.get_identifier()),
"          STREAM_{0}_ACK <= '1';".format(i.get_identifier()),
"          REGISTER_EN_2_{0} <= '1';".format(process_id),
"          RESULT_2_{0} <= STD_RESIZE(STREAM_{1}, {2});".format(process_id, i.get_identifier(), process_bits),
"          STATE_{0} <= ACK_STREAM_{1};".format(process.get_identifier(), i.get_identifier()),
"        end if;",
"      when ACK_STREAM_{0} =>".format(i.get_identifier()),
"        STREAM_{0}_ACK <= '0';".format(i.get_identifier()),
"        STATE_{0} <= EXECUTE;".format(process.get_identifier()),
"        PC_{0} <= PC_{0} + 1;".format(process_id),
        ])
        operations.append("OP_READ_{0}".format(i.get_identifier()))
        states.append("READ_STREAM_{0}".format(i.get_identifier()))
        states.append("ACK_STREAM_{0}".format(i.get_identifier()))
        reset_streams.append(
"      STREAM_{0}_ACK <= '0';".format(i.get_identifier()),
        )

################################################################################
#GENERATE ADDITIONAL INSTRUCTIONS FOR WRITING OUTPUT STREAMS
################################################################################

    write_outputs = []
    output_instructions = []
    output_instructions_fetch = []
    for i in process.outputs:
        plugin.declarations.extend([
"  signal STREAM_{0}       : std_logic_vector({1} downto 0);".format(i.get_identifier(), i.get_bits()-1),
"  signal STREAM_{0}_STB   : std_logic;".format(i.get_identifier()),
"  signal STREAM_{0}_ACK   : std_logic;".format(i.get_identifier()),
        ])
        output_instructions.extend([
"          when OP_WRITE_{0}_{1} =>".format(i.get_identifier(), process_id),
"            STATE_{0} <= WRITE_STREAM_{1};".format(process_id, i.get_identifier()),
"            STREAM_{0} <= STD_RESIZE(REGA_1_{1}, {2});".format(i.get_identifier(), process_id, i.get_bits()),
"            STREAM_{0}_STB <= '0';".format(i.get_identifier()),
"            PC_{0} <= PC_{0};".format(process_id),
        ])
        write_outputs.extend([
"      when WRITE_STREAM_{0} =>".format(i.get_identifier()),
"        STREAM_{0}_STB <= '1';".format(i.get_identifier()),
"        if STREAM_{0}_ACK = '1' then".format(i.get_identifier()),
"          STREAM_{0}_STB <= '0';".format(i.get_identifier()),
"          STATE_{0} <= EXECUTE;".format(process.get_identifier(), i.get_identifier()),
"          PC_{0} <= PC_{0} + 1;".format(process_id),
"        end if;",
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
    for index, instruction in enumerate(process_instructions):
        operation = instruction.operation
        srca = instruction.srca if instruction.srca else 0
        srcb = instruction.srcb if instruction.srcb else 0
        immediate = instruction.immediate if instruction.immediate else 0
        if index == len(process_instructions)-1:
            instructions.append(
                "{0} => {1}_{2} & {3} & {4}); -- file: {5} line: {6}".format(
                    index, 
                    operation, 
                    process_id,
                    common.binary(srca, register_address_bits),
                    common.binary(resize(immediate, process_bits) | srcb, process_bits),
                    instruction.filename,
                    instruction.lineno
                )
            )
        else:
            instructions.append(
                "{0} => {1}_{2} & {3} & {4}, -- file: {5} line: {6}".format(
                    index, 
                    operation, 
                    process_id,
                    common.binary(srca, register_address_bits),
                    common.binary(resize(immediate, process_bits) | srcb, process_bits),
                    instruction.filename,
                    instruction.lineno
                )
            )


    for index, operation in enumerate(operations):
        plugin.declarations.append(
"  constant {0}_{1} : std_logic_vector({2} downto 0) := {3};".format(
                operation, process_id, operation_bits-1, common.binary(index, operation_bits)
            )
        )

################################################################################
#DIVIDER
################################################################################
    divider_fetch = []
    divider_decode = []
    divider_logic = []
    divider_arithmetic = []
    if ("OP_DIV" in operations) or ("OP_MOD" in operations):
        divider_decode = []
        if "OP_DIV" in operations:
            divider_decode.extend([
"          when OP_DIV_{0} =>".format(process_id),
"            MOD_DIV_{0} <= '1';".format(process_id),
"            A_{0} <= std_logic_vector(abs(signed(REGA_1_{0})));".format(process_id),
"            B_{0} <= std_logic_vector(abs(signed(REGB_1_{0})));".format(process_id),
"            SIGN_{0} <= REGA_1_{0}({1}) xor REGB_1_{0}({1});".format(process_id, process_bits-1),
"            STATE_{0} <= DIVIDE_0;".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id),])
        if "OP_MOD" in operations:
            divider_decode.extend([
"          when OP_MOD_{0} =>".format(process_id),
"            MOD_DIV_{0} <= '0';".format(process_id),
"            A_{0} <= std_logic_vector(abs(signed(REGA_1_{0})));".format(process_id),
"            B_{0} <= std_logic_vector(abs(signed(REGB_1_{0})));".format(process_id),
"            SIGN_{0} <= REGA_1_{0}({1});".format(process_id, process_bits-1),
"            STATE_{0} <= DIVIDE_0;".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id)])
        divider_logic = [
"",
"      when DIVIDE_0 =>",
"        QUOTIENT_{0} <= (others => '0');".format(process_id),
"        SHIFTER_{0} <= (others => '0');".format(process_id),
"        SHIFTER_{0}(0) <= A_{0}({1});".format(process_id, process_bits-1),
"        A_{0} <= A_{0}({1} downto 0) & '0';".format(process_id, process_bits-2),
"        COUNT_{0} <= {1};".format(process_id, process_bits-1),
"        STATE_{0} <= DIVIDE_1;".format(process_id),
"",
"      when DIVIDE_1 => --subtract",
"       --if SHIFTER - B is positive or zero",
"       if REMAINDER_{0}({1}) = '0' then".format(process_id, process_bits-1),
"         SHIFTER_{0}({1} downto 1) <= REMAINDER_{0}({2} downto 0);".format(process_id, process_bits-1, process_bits-2),
"       else",
"         SHIFTER_{0}({1} downto 1) <= SHIFTER_{0}({2} downto 0);".format(process_id, process_bits-1, process_bits-2),
"       end if;",
"       SHIFTER_{0}(0) <= A_{0}({1});".format(process_id, process_bits-1),
"       A_{0} <= A_{0}({1} downto 0) & '0';".format(process_id, process_bits-2),
"       QUOTIENT_{0} <= QUOTIENT_{0}({2} downto 0) & not(REMAINDER_{0}({1}));".format(process_id, process_bits-1, process_bits-2),
"       if COUNT_{0} = 0 then".format(process_id),
"         STATE_{0} <= DIVIDE_2;".format(process_id),
"       else",
"         COUNT_{0} <= COUNT_{0} - 1;".format(process_id),
"       end if;",
"",
"     when DIVIDE_2 =>",
"      REGISTER_EN_2_{0} <= '1';".format(process_id),
"      if MOD_DIV_{0} = '1' then --if division".format(process_id),
"        if SIGN_{0} = '1' then --if negative".format(process_id),
"          RESULT_2_{0} <= std_logic_vector(-signed(QUOTIENT_{0}));".format(process_id),
"        else",
"          RESULT_2_{0} <= QUOTIENT_{0};".format(process_id),
"        end if;",
"      else",
"        MODULO := unsigned(SHIFTER_{0})/2;".format(process_id),
"        if SIGN_{0} = '1' then --if negative".format(process_id),
"          RESULT_2_{0} <= std_logic_vector(0-MODULO);".format(process_id),
"        else",
"          RESULT_2_{0} <= std_logic_vector(  MODULO);".format(process_id),
"        end if;",
"      end if;",
"      STATE_{0} <= EXECUTE;".format(process_id),
"      PC_{0} <= PC_{0} + 1;".format(process_id),
        ]
        divider_arithmetic = [
"",
"  --subtractor",
"  REMAINDER_{0} <= std_logic_vector(unsigned(SHIFTER_{0}) - resize(unsigned(B_{0}), {1}));".format(process_id, process_bits),
        ]


################################################################################
#GENERATE PROCESS DECLARATIONS
################################################################################

    plugin.declarations.extend([
"  type PROCESS_{0}_STATE_TYPE is ({1});".format(process.get_identifier(), ', '.join(states)),
"  type INSTRUCTIONS_TYPE_{0}  is array (0 to {1}) of std_logic_vector({2} downto 0);".format(process_id, num_instructions-1, instruction_bits-1),
"  type REGISTERS_TYPE_{0}     is array (0 to {1}) of std_logic_vector({2} downto 0);".format(process_id, num_registers-1, process_bits-1),
"",
"  --Pipeline stage 0 outputs",
"  signal OPERATION_0_{0}  : std_logic_vector({1} downto 0);".format(process_id, operation_bits-1),
"  signal SRCA_0_{0}       : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal SRCB_0_{0}       : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal IMMEDIATE_0_{0}  : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),

"  --Pipeline stage 1 outputs",
"  signal OPERATION_1_{0}    : std_logic_vector({1} downto 0);".format(process_id, operation_bits-1),
"  signal IMMEDIATE_1_{0}    : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal REGA_1_{0}         : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal REGB_1_{0}         : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal DEST_1_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),

"  --Pipeline stage 2 outputs",
"  signal RESULT_2_{0}       : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal DEST_2_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal REGISTER_EN_2_{0}  : std_logic;".format(process_id),

"  --Pipeline stage 2 outputs",
"  signal STATE_{0}          : PROCESS_{0}_STATE_TYPE;".format(process.get_identifier()),
"  signal PC_{0}             : unsigned({1} downto 0);".format(process_id, instruction_address_bits - 1),
"  signal ZERO_{0}           : std_logic;".format(process_id),
"  signal A_{0}              : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal B_{0}              : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal QUOTIENT_{0}       : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal SHIFTER_{0}        : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal REMAINDER_{0}      : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal COUNT_{0}          : integer range 0 to {1};".format(process_id, process_bits),
"  signal SIGN_{0}           : std_logic;".format(process_id),
"  signal INSTRUCTIONS_{0}   : INSTRUCTIONS_TYPE_{0} := (\n{1}".format(process_id, '\n'.join(instructions)),
"  signal MOD_DIV_{0}        : std_logic;".format(process_id),
    ])

################################################################################
#GENERATE PROCESS DEFINITIONS
################################################################################

    operation_hi = instruction_bits-1
    operation_lo = operation_hi-operation_bits+1
    srca_hi = operation_lo-1
    srca_lo = srca_hi-register_address_bits+1
    srcb_lo = 0
    srcb_hi = srcb_lo+register_address_bits-1
    immediate_hi = srca_lo-1
    immediate_lo = 0

    plugin.definitions.extend([
"  -- PIPELINE STAGE 0",
"  process",
"    variable INSTRUCTION : std_logic_vector({1} downto 0);".format(process_id, instruction_bits-1),
"  begin",
"    wait until rising_edge(CLK);",
"    INSTRUCTION := INSTRUCTIONS_{0}(to_integer(PC_{0}));".format(process_id),
"    SRCA_0_{0}      <= INSTRUCTION({1} downto {2});".format(process_id, srca_hi, srca_lo), 
"    SRCB_0_{0}      <= INSTRUCTION({1} downto {2});".format(process_id, srcb_hi, srcb_lo), 
"    IMMEDIATE_0_{0} <= INSTRUCTION({1} downto {2});".format(process_id, immediate_hi, immediate_lo), 
"    OPERATION_0_{0} <= INSTRUCTION({1} downto {2});".format(process_id, operation_hi, operation_lo), 
"  end process;",
"",
"  -- PIPELINE STAGE 1",
"  process",
"    variable REGISTERS : REGISTERS_TYPE_{0};".format(process_id),
"  begin",
"    wait until rising_edge(CLK);",
"    REGA_1_{0}      <= REGISTERS(to_integer(unsigned(SRCA_0_{0})));".format(process_id),
"    REGB_1_{0}      <= REGISTERS(to_integer(unsigned(SRCB_0_{0})));".format(process_id),
"    DEST_1_{0}      <= SRCA_0_{0};".format(process_id),
"    OPERATION_1_{0} <= OPERATION_0_{0};".format(process_id), 
"    IMMEDIATE_1_{0} <= IMMEDIATE_0_{0};".format(process_id), 
"    if REGISTER_EN_2_{0} = '1' then".format(process_id),
"      REGISTERS(to_integer(unsigned(DEST_2_{0}))) := RESULT_2_{0};".format(process_id),
"    end if;".format(process_id),
"  end process;",
"",
"  -- PIPELINE STAGE 2",
"  process",
"    variable MODULO       : unsigned({0} downto 0);".format(process_bits-1),
"    variable STALL_COUNT  : integer range 0 to {0};".format(pc_to_execute_latency - 1)])

    if ("OP_EQ" in operations) or ("OP_NE" in operations) or ("OP_GE" in operations):
        plugin.definitions.append("    variable FLAG_EQ      : std_logic;")
    if ("OP_NE" in operations):
        plugin.definitions.append("    variable FLAG_NE      : std_logic;")
    if ("OP_GT" in operations) or ("OP_GE" in operations):
        plugin.definitions.append("    variable FLAG_GT      : std_logic;")
    if ("OP_GE" in operations):
        plugin.definitions.append("    variable FLAG_GE      : std_logic;")

    plugin.definitions.extend([
"  begin",
"    wait until rising_edge(CLK);",
"    REGISTER_EN_2_{0} <= '0';".format(process_id),
"    case STATE_{0} is".format(process_id),
"      when STALL =>",
"        PC_{0} <= PC_{0} + 1;".format(process_id),
"        if STALL_COUNT = 0 then",
"          STATE_{0} <= EXECUTE;".format(process_id),
"        else",
"          STALL_COUNT := STALL_COUNT - 1;",
"        end if;",
"      when EXECUTE =>",
"        DEST_2_{0} <= DEST_1_{0};".format(process_id),
"        RESULT_2_{0} <= REGA_1_{0};".format(process_id),
"        PC_{0} <= PC_{0} + 1;".format(process_id),
""])

    if ("OP_EQ" in operations) or ("OP_NE" in operations) or ("OP_GE" in operations):
        plugin.definitions.extend([
"        --share comparator logic",
"        if REGA_1_{0} = REGB_1_{0} then".format(process_id),
"          FLAG_EQ := '1';",
"        else",
"          FLAG_EQ := '0';",
"        end if;",
""])

    if ("OP_NE" in operations):
        plugin.definitions.extend([
"        FLAG_NE := not FLAG_EQ;",
""])

    if ("OP_GT" in operations) or ("OP_GE" in operations):
        plugin.definitions.extend([
"        if signed(REGA_1_{0}) > signed(REGB_1_{0}) then".format(process_id),
"          FLAG_GT := '1';",
"        else",
"          FLAG_GT := '0';",
"        end if;",
""])

    if ("OP_GE" in operations):
        plugin.definitions.extend([
"        FLAG_GE := FLAG_GT or FLAG_EQ;".format(process_id),
""])

    plugin.definitions.extend([
"        --execute instructions",
"        case OPERATION_1_{0} is".format(process_id)])

    if ("OP_MOVE" in operations):
        plugin.definitions.extend([
"          when OP_MOVE_{0} => ".format(process_id),
"            RESULT_2_{0} <= REGB_1_{0};".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_NOOP" in operations):
        plugin.definitions.extend([
"          when OP_NOOP_{0} => ".format(process_id),
"            REGISTER_EN_2_{0} <= '0';".format(process_id)])

    if ("OP_MUL" in operations):
        plugin.definitions.extend([
"          when OP_MUL_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( MUL(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_ADD" in operations):
        plugin.definitions.extend([
"          when OP_ADD_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( ADD(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_SUB" in operations):
        plugin.definitions.extend([
"          when OP_SUB_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( SUB(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_BAND" in operations):
        plugin.definitions.extend([
"          when OP_BAND_{0} => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE(BAND(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_BOR" in operations):
        plugin.definitions.extend([
"          when OP_BOR_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( BOR(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_BXOR" in operations):
        plugin.definitions.extend([
"          when OP_BXOR_{0} => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE(BXOR(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_SL" in operations):
        plugin.definitions.extend([
"          when OP_SL_{0}   => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE(  SL(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_SR" in operations):
        plugin.definitions.extend([
"          when OP_SR_{0}   => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE(  SR(REGA_1_{0}, REGB_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_EQ" in operations):
        plugin.definitions.extend([
"          when OP_EQ_{0}   => ".format(process_id),
"            RESULT_2_{0} <= (others => FLAG_EQ);".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_NE" in operations):
        plugin.definitions.extend([
"          when OP_NE_{0}   => ".format(process_id),
"            RESULT_2_{0} <= (others => FLAG_NE);".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_GT" in operations):
        plugin.definitions.extend([
"          when OP_GT_{0}   => ".format(process_id),
"            RESULT_2_{0} <= (others => FLAG_GT);".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_GE" in operations):
        plugin.definitions.extend([
"          when OP_GE_{0}   => ".format(process_id),
"            RESULT_2_{0} <= (others => FLAG_GE);".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_IMM" in operations):
        plugin.definitions.extend([
"          when OP_IMM_{0}  => ".format(process_id),
"            RESULT_2_{0} <= IMMEDIATE_1_{0};".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_ABS" in operations):
        plugin.definitions.extend([
"          when OP_ABS_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( ABSOLUTE(REGA_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_INVERT" in operations):
        plugin.definitions.extend([
"          when OP_INVERT_{0}  => ".format(process_id),
"            RESULT_2_{0} <= not REGA_1_{0};".format(process_id),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    for i in left_shifts:
        plugin.definitions.extend([
"          when OP_SLN_{0}_{1}  => ".format(i, process_id),
"            RESULT_2_{0} <= STD_RESIZE( SL(REGA_1_{0}, {1}), {2});".format(process_id, common.binary(i, process_bits), process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    for i in right_shifts:
        plugin.definitions.extend([
"          when OP_SRN_{0}_{1}  => ".format(i, process_id),
"            RESULT_2_{0} <= STD_RESIZE( SR(REGA_1_{0}, {1}), {2});".format(process_id, common.binary(i, process_bits), process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    for i in availables:
        plugin.definitions.extend([
"          when OP_AVAILABLE_{0}_{1}  => ".format(i, process_id),
"            if STREAM_{0}_STB = '1' then".format(i),
"              RESULT_2_{0} <= {1};".format(process_id, common.binary(-1, process_bits)),
"            else",
"              RESULT_2_{0} <= {1};".format(process_id, common.binary(0, process_bits)),
"            end if;",
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_LNOT" in operations):
        plugin.definitions.extend([
"          when OP_LNOT_{0}  => ".format(process_id),
"            RESULT_2_{0} <= STD_RESIZE( LNOT(REGA_1_{0}), {1});".format(process_id, process_bits),
"            REGISTER_EN_2_{0} <= '1';".format(process_id)])

    if ("OP_JMP" in operations):
        plugin.definitions.extend([
"          when OP_JMP_{0} =>".format(process_id),
"            STATE_{0} <= STALL;".format(process_id),
"            STALL_COUNT := {0};".format(pc_to_execute_latency - 1),
"            PC_{0} <= resize(unsigned(IMMEDIATE_1_{0}), {1});".format(process_id, instruction_address_bits)])

    if ("OP_JMPF" in operations):
        plugin.definitions.extend([
"          when OP_JMPF_{0} =>".format(process_id),
"            if RESULT_2_{0} = {1} then".format(process_id, common.binary(0, process_bits)),
"              STATE_{0} <= STALL;".format(process_id),
"              STALL_COUNT := {0};".format(pc_to_execute_latency - 1),
"              PC_{0} <= resize(unsigned(IMMEDIATE_1_{0}), {1});".format(process_id, instruction_address_bits),
"            end if;".format(process_id)])

    if ("OP_WAIT_US" in operations):
        plugin.definitions.extend([
"          when OP_WAIT_US_{0} =>".format(process_id),
"            STATE_{0} <= WAIT_US;".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id)])

    plugin.definitions.extend([
'\n'.join(divider_decode),
'\n'.join(output_instructions),
'\n'.join(input_instructions),
"          when others => null;",
"        end case;",
"",
'\n'.join(divider_logic),
'\n'.join(read_inputs),
'\n'.join(write_outputs)])

    if ("OP_WAIT_US" in operations):
        plugin.definitions.extend([
"      when WAIT_US =>",
"        if TIMER_1uS = '1'then".format(process_id),
"          PC_{0} <= PC_{0} + 1;".format(process_id),
"          STATE_{0} <= EXECUTE;".format(process_id),
"        end if;".format(process_id)])

    plugin.definitions.extend([
"    end case;",
"",
"    if RST = '1' then",
"      STATE_{0} <= STALL;".format(process_id),
"      STALL_COUNT := {0};".format(pc_to_execute_latency - 1),
"      PC_{0} <= {1};".format(process_id, common.binary(0, instruction_address_bits)),
"\n".join(reset_streams),
"    end if;",
"  end process;",
"",
"\n".join(divider_arithmetic),
    ])

