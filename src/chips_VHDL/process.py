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
    process_instructions = tuple(process.instructions)
    operations = []
    states = ["STALL", "EXECUTE"]

    #save logic by turning off features if not used
    for instruction in process_instructions:
        for j in ["OP_DIV", "OP_MOD", "OP_MUL", "OP_ADD", "OP_SUB", "OP_BAND",
                "OP_BOR", "OP_BXOR", "OP_SL", "OP_SR", "OP_EQ", "OP_NE", 
                "OP_GE", "OP_GT", "OP_WAIT_US", "OP_JMP", "OP_JMPF", "OP_MOVE",
                "OP_IMM", "OP_WAIT_US"]:
            if instruction.operation == j:
                if j not in operations:
                    operations.append(j)
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
"          REGISTERS_EN := '1';",
"          RESULT := STD_RESIZE(STREAM_{1}, {2});".format(process_id, i.get_identifier(), process_bits),
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
"            DEST := SRCA_{0};".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id),
        ])
        write_outputs.extend([
"      when WRITE_STREAM_{0} =>".format(i.get_identifier()),
"        STREAM_{0}_STB <= '1';".format(i.get_identifier()),
"        STREAM_{0} <= STD_RESIZE(REGA, {1});".format(i.get_identifier(), i.get_bits()),
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
"            A_{0} <= std_logic_vector(abs(signed(REGA)));".format(process_id),
"            B_{0} <= std_logic_vector(abs(signed(REGB)));".format(process_id),
"            SIGN_{0} <= REGA({1}) xor REGB({1});".format(process_id, process_bits-1),
"            STATE_{0} <= DIVIDE_0;".format(process_id),
"            PC_{0} <= PC_{0};".format(process_id),])
        if "OP_MOD" in operations:
            divider_decode.extend([
"          when OP_MOD_{0} =>".format(process_id),
"            MOD_DIV_{0} <= '0';".format(process_id),
"            A_{0} <= std_logic_vector(abs(signed(REGA)));".format(process_id),
"            B_{0} <= std_logic_vector(abs(signed(REGB)));".format(process_id),
"            SIGN_{0} <= REGA({1});".format(process_id, process_bits-1),
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
"      REGISTERS_EN := '1';",
"      if MOD_DIV_{0} = '1' then --if division".format(process_id),
"        if SIGN_{0} = '1' then --if negative".format(process_id),
"          RESULT := std_logic_vector(-signed(QUOTIENT_{0}));".format(process_id),
"        else",
"          RESULT := QUOTIENT_{0};".format(process_id),
"        end if;",
"      else",
"        MODULO := unsigned(SHIFTER_{0})/2;".format(process_id),
"        if SIGN_{0} = '1' then --if negative".format(process_id),
"          RESULT := std_logic_vector(0-MODULO);".format(process_id),
"        else",
"          RESULT := std_logic_vector(  MODULO);".format(process_id),
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
"  signal STATE_{0}        : PROCESS_{0}_STATE_TYPE;".format(process.get_identifier()),
"  signal REGISTERS_{0}    : REGISTERS_TYPE_{0};".format(process_id),
"  signal PC_{0}           : unsigned({1} downto 0);".format(process_id, instruction_address_bits - 1),
"  signal OPERATION_{0}    : std_logic_vector({1} downto 0);".format(process_id, operation_bits-1),
"  signal SRCA_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal SRCB_{0}         : std_logic_vector({1} downto 0);".format(process_id, register_address_bits-1),
"  signal IMMEDIATE_{0}    : std_logic_vector({1} downto 0);".format(process_id, process_bits-1),
"  signal ZERO_{0}         : std_logic;".format(process_id),
"  signal A_{0}            : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal B_{0}            : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal QUOTIENT_{0}     : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal SHIFTER_{0}      : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal REMAINDER_{0}    : std_logic_vector({1} downto 0);".format(process_id, process_bits - 1),
"  signal COUNT_{0}        : integer range 0 to {1};".format(process_id, process_bits),
"  signal SIGN_{0}         : std_logic;".format(process_id),
"  signal INSTRUCTIONS_{0} : INSTRUCTIONS_TYPE_{0} := (\n{1}".format(process_id, '\n'.join(instructions)),
"  signal MOD_DIV_{0}      : std_logic;".format(process_id),
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
"    variable REGA         : std_logic_vector({0} downto 0);".format(process_bits-1),
"    variable REGB         : std_logic_vector({0} downto 0);".format(process_bits-1),
"    variable DEST         : std_logic_vector({0} downto 0);".format(register_address_bits-1),
"    variable RESULT       : std_logic_vector({0} downto 0);".format(process_bits-1),
"    variable RESULT_DEL   : std_logic_vector({0} downto 0);".format(process_bits-1),
"    variable REGISTERS_EN : std_logic;".format(process_bits-1),
"    variable MODULO       : unsigned({0} downto 0);".format(process_bits-1)])

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
"    REGISTERS_EN := '0';",
"    case STATE_{0} is".format(process_id),
"      when STALL =>",
"        PC_{0} <= PC_{0} + 1;".format(process_id),
"        STATE_{0} <= EXECUTE;".format(process_id),
"      when EXECUTE =>",
"        REGA := REGISTERS_{0}(to_integer(unsigned(SRCA_{0})));".format(process_id),
"        REGB := REGISTERS_{0}(to_integer(unsigned(SRCB_{0})));".format(process_id),
"        DEST := SRCA_{0};".format(process_id),
"        RESULT := REGA;".format(process_id),
"        PC_{0} <= PC_{0} + 1;".format(process_id),
""])

    if ("OP_EQ" in operations) or ("OP_NE" in operations) or ("OP_GE" in operations):
        plugin.definitions.extend([
"        --share comparator logic",
"        if REGA = REGB then".format(process_id),
"          FLAG_EQ := '1';".format(process_id),
"        else",
"          FLAG_EQ := '0';".format(process_id),
"        end if;",
""])

    if ("OP_NE" in operations):
        plugin.definitions.extend([
"        FLAG_NE := not FLAG_EQ;".format(process_id),
""])

    if ("OP_GT" in operations) or ("OP_GE" in operations):
        plugin.definitions.extend([
"        if signed(REGA) > signed(REGB) then".format(process_id),
"          FLAG_GT := '1';".format(process_id),
"        else",
"          FLAG_GT := '0';".format(process_id),
"        end if;",
""])

    if ("OP_GE" in operations):
        plugin.definitions.extend([
"        FLAG_GE := FLAG_GT or FLAG_EQ;".format(process_id),
""])

    plugin.definitions.extend([
"        --execute instructions",
"        case OPERATION_{0} is".format(process_id)])

    if ("OP_MOVE" in operations):
        plugin.definitions.extend([
"          when OP_MOVE_{0} => ".format(process_id),
"            RESULT := REGB;".format(process_id, process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_MUL" in operations):
        plugin.definitions.extend([
"          when OP_MUL_{0}  => ".format(process_id),
"            RESULT := STD_RESIZE( MUL(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_ADD" in operations):
        plugin.definitions.extend([
"          when OP_ADD_{0}  => ".format(process_id),
"            RESULT := STD_RESIZE( ADD(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_SUB" in operations):
        plugin.definitions.extend([
"          when OP_SUB_{0}  => ".format(process_id),
"            RESULT := STD_RESIZE( SUB(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_BAND" in operations):
        plugin.definitions.extend([
"          when OP_BAND_{0} => ".format(process_id),
"            RESULT := STD_RESIZE(BAND(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_BOR" in operations):
        plugin.definitions.extend([
"          when OP_BOR_{0}  => ".format(process_id),
"            RESULT := STD_RESIZE( BOR(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_BXOR" in operations):
        plugin.definitions.extend([
"          when OP_BXOR_{0} => ".format(process_id),
"            RESULT := STD_RESIZE(BXOR(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_SL" in operations):
        plugin.definitions.extend([
"          when OP_SL_{0}   => ".format(process_id),
"            RESULT := STD_RESIZE(  SL(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_SR" in operations):
        plugin.definitions.extend([
"          when OP_SR_{0}   => ".format(process_id),
"            RESULT := STD_RESIZE(  SR(REGA, REGB), {0});".format(process_bits),
"            REGISTERS_EN := '1';"])

    if ("OP_EQ" in operations):
        plugin.definitions.extend([
"          when OP_EQ_{0}   => ".format(process_id),
"            RESULT := (others => FLAG_EQ);".format(process_id),
"            REGISTERS_EN := '1';"])

    if ("OP_NE" in operations):
        plugin.definitions.extend([
"          when OP_NE_{0}   => ".format(process_id),
"            RESULT := (others => FLAG_NE);".format(process_id),
"            REGISTERS_EN := '1';"])

    if ("OP_GT" in operations):
        plugin.definitions.extend([
"          when OP_GT_{0}   => ".format(process_id),
"            RESULT := (others => FLAG_GT);".format(process_id),
"            REGISTERS_EN := '1';"])

    if ("OP_GE" in operations):
        plugin.definitions.extend([
"          when OP_GE_{0}   => ".format(process_id),
"            RESULT := (others => FLAG_GE);".format(process_id),
"            REGISTERS_EN := '1';"])

    if ("OP_IMM" in operations):
        plugin.definitions.extend([
"          when OP_IMM_{0}  => ".format(process_id),
"            RESULT := IMMEDIATE_{0};".format(process_id),
"            REGISTERS_EN := '1';"])

    if ("OP_JMP" in operations):
        plugin.definitions.extend([
"          when OP_JMP_{0} =>".format(process_id),
"            STATE_{0} <= STALL;".format(process_id),
"            PC_{0} <= resize(unsigned(IMMEDIATE_{0}), {1});".format(process_id, instruction_address_bits)])

    if ("OP_JMPF" in operations):
        plugin.definitions.extend([
"          when OP_JMPF_{0} =>".format(process_id),
"            if RESULT_DEL = {1} then".format(process_id, common.binary(0, process_bits)),
"              STATE_{0} <= STALL;".format(process_id),
"              PC_{0} <= resize(unsigned(IMMEDIATE_{0}), {1});".format(process_id, instruction_address_bits),
"            end if;".format(process_id),])

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
"        --write back results",
"        RESULT_DEL := RESULT;".format(process_id, common.binary(0, process_bits)),
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
"      PC_{0} <= {1};".format(process_id, common.binary(0, instruction_address_bits)),
"\n".join(reset_streams),
"    end if;",
"    if REGISTERS_EN = '1' then".format(process_id),
"      REGISTERS_{0}(to_integer(unsigned(DEST))) <= RESULT;".format(process_id),
"    end if;".format(process_id),
"  end process;",
"",
"\n".join(divider_arithmetic),
    ])

