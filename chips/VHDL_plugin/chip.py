"""VHDL generation of the overall VHDL component"""

import sys
from datetime import datetime

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(
        dependencies, 
        ports, 
        declarations, 
        definitions, 
        outputfile, 
        internal_clock = False, 
        internal_reset = False,
        clk_frequency = 50000000
    ):

    system_ports = []
    if not internal_clock:
        system_ports.append(
"    CLK           : in  std_logic",
        )
    if not internal_reset:
        system_ports.append(
"    RST           : in  std_logic",
        )
    system_ports.extend(ports)
    if system_ports:
        system_ports = '\n'.join([
"  port(", 
";\n".join(system_ports), 
"  );"
        ])
    else:
        system_ports = ""

    clock_generator = []
    clock_signal = ""
    if internal_clock:
        clock_signal = "  signal CLK : std_logic;"
        clock_generator = [
"  --internal clock generator",
"  process",
"  begin",
"    while True loop",
"      CLK <= '0';",
"      wait for 5 ns;",
"      CLK <= '1';",
"      wait for 5 ns;",
"    end loop;",
"    wait;",
"  end process;",
"",
        ]

    reset_generator = []
    reset_signal = ""
    if internal_reset:
        reset_signal = "  signal RST : std_logic;"
        reset_generator = [
"  --internal reset generator",
"  process",
"  begin",
"    RST <= '1';",
"    wait for 20 ns;",
"    RST <= '0';",
"    wait;",
"  end process;",
"",
        ]

    system = [
"--+============================================================================+",
"--|   **THIS FILE WAS AUTOMATICALLY GENERATED BY THE PYTHON CHIPS LIBRARY**    |",
"--+ ============================================================================+",
"--|                    _       ________________                                |",
"--|                   (_)---->/               /     _                          |",
"--|                    _     / PYTHON CHIPS  /---->(_)                         |",
"--|                   (_)-->/_______________/                                  |",
"--|                                                                            |",
"--+============================================================================+",
"",
"-- generated by python streams library",
"-- date generated  : {0}".format(datetime.utcnow().strftime("UTC %Y-%m-%d %H:%M:%S")),
"-- platform        : {0}".format(sys.platform),
"-- python version  : {0}".format(' '.join(sys.version.split())),
"-- streams version : {0}".format(__version__),
"",
"--+============================================================================+",
"--|                             **END OF HEADER**                              |",
"--+============================================================================+",
"",
"--                                   ***                                       ",
"",
"--+============================================================================+",
"--|                    **START OF EXTERNAL DEPENDENCIES**                      |",
"--+============================================================================+",
"",
"\n".join(dependencies),
"",
"--+============================================================================+",
"--|                     **END OF EXTERNAL DEPENDENCIES**                       |",
"--+============================================================================+",
"",
"--                                   ***                                       ",
"",
"--+============================================================================+",
"--|                     **START OF AUTO GENERATED CODE**                       |",
"--+============================================================================+",
"",
"library ieee;",
"use ieee.std_logic_1164.all;",
"use ieee.numeric_std.all;",
"use std.textio.all;",
"",
"entity STREAMS_VHDL_MODEL is",
system_ports,
"end entity STREAMS_VHDL_MODEL;",
"",
"architecture RTL of STREAMS_VHDL_MODEL is",
"",
"",
"  --returns the greater of the two parameters",
"  function MAX(",
"    A : integer;",
"    B : integer) return integer is",
"  begin",
"    if A > B then",
"      return A;",
"    else",
"      return B;",
"    end if;",
"  end MAX;",
"",
"  --returns a std_logic_vector sum of the two parameters",
"  function ADD(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), MAX(A'length, B'length) + 1) + ",
"      resize(signed(B), MAX(A'length, B'length) + 1));",
"    end ADD;",
"",
"  --returns a std_logic_vector product of the two parameters",
"  function MUL(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      signed(A) *",
"      signed(B));",
"    end MUL;",
"",
"  --returns a std_logic_vector difference of the two parameters",
"  function SUB(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), MAX(A'length, B'length) + 1) - ",
"      resize(signed(B), MAX(A'length, B'length) + 1));",
"  end SUB;",
"",
"  --returns A shifted right (arithmetic) by A",
"  function SR(",
"    A  : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(shift_right(signed(A), to_integer(signed(B))));",
"  end SR;",
"",
"  --returns A shifted left by B",
"  function SL(",
"    A  : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(shift_left(signed(A), to_integer(signed(B))));",
"  end SL;",
"",
"  --returns bitwise and of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function BAND(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) and",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));",
"  end BAND;",
"",
"  --returns bitwise or of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function BOR(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) or",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));",
"  end BOR;",
"",
"  --returns bitwise xor of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function BXOR(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) xor",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)));",
"  end BXOR;",
"",
"  --equality comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function EQ(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) =",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end EQ;",
"",
"  --inequality comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function NE(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"    resize(signed(A), MAX(A'LENGTH, B'LENGTH)) /=",
"    resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end NE;",
"",
"  --greater than comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function GT(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) >",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end GT;",
"",
"  --greater than or equal comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function GE(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) >=",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end GE;",
"",
"  --less than comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function LT(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) <",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end LT;",
"",
"  --less than or equal comparison of A and B",
"  --(A and B are resized to the length of the larger first)",
"  function LE(",
"    A : std_logic_vector; ",
"    B : std_logic_vector) return std_logic_vector is",
"  begin",
"    if ",
"      resize(signed(A), MAX(A'LENGTH, B'LENGTH)) <=",
"      resize(signed(B), MAX(A'LENGTH, B'LENGTH)) then",
'      return "1";',
"    else",
'      return "0";',
"    end if;",
"  end LE;",
"",
"  --resize A to B bits",
"  function STD_RESIZE(",
"    A : std_logic_vector; ",
"    B : integer) return std_logic_vector is",
"  begin",
"    return std_logic_vector(",
"      resize(signed(A), B));",
"  end STD_RESIZE;",
"",
"  type BINARY_STATE_TYPE is (BINARY_INPUT, BINARY_OUTPUT);",
"  type UNARY_STATE_TYPE is (UNARY_INPUT, UNARY_OUTPUT);",
"  type TEE_STATE_TYPE is (TEE_INPUT_A, TEE_WAIT_YZ, TEE_WAIT_Y, TEE_WAIT_Z);",
"  type DIVIDER_STATE_TYPE is (READ_A_B, DIVIDE_1, DIVIDE_2, WRITE_Z);",
"  type SERIAL_IN_STATE_TYPE is (IDLE, START, RX0, RX1, RX2, RX3, RX4, RX5, RX6, RX7, STOP, OUTPUT_DATA);",
"  type SERIAL_OUT_STATE_TYPE is (IDLE, START, WAIT_EN, TX0, TX1, TX2, TX3, TX4, TX5, TX6, TX7, STOP);",
"  type PRINTER_STATE_TYPE is (INPUT_A, SHIFT, OUTPUT_SIGN, OUTPUT_Z, OUTPUT_NL);",
"  type HEX_PRINTER_STATE_TYPE is (INPUT_A, OUTPUT_SIGN, OUTPUT_DIGITS);",
"",
"  constant TIMER_1us_MAX : integer := {0};".format((clk_frequency/1000000)-1),
"  signal TIMER_1us_COUNT : integer range 0 to TIMER_1us_MAX;",
"  signal TIMER_1us : std_logic;",
"  constant TIMER_10us_MAX : integer := {0};".format((clk_frequency/1000000)-1),
"  signal TIMER_10us_COUNT : integer range 0 to TIMER_1us_MAX;",
"  signal TIMER_10us : std_logic;",
"  constant TIMER_100us_MAX : integer := {0};".format((clk_frequency/1000000)-1),
"  signal TIMER_100us_COUNT : integer range 0 to TIMER_1us_MAX;",
"  signal TIMER_100us : std_logic;",
"  constant TIMER_1ms_MAX : integer := {0};".format((clk_frequency/1000000)-1),
"  signal TIMER_1ms_COUNT : integer range 0 to TIMER_1us_MAX;",
"  signal TIMER_1ms : std_logic;",
"",
clock_signal, reset_signal,
"\n".join(declarations),
"",
"begin",
"",
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    TIMER_1us <= '0';",
"    TIMER_10us <= '0';",
"    TIMER_100us <= '0';",
"    TIMER_1ms <= '0';",
"    if TIMER_1us_COUNT = 0 then",
"       TIMER_1us_COUNT <= TIMER_1us_MAX;",
"       TIMER_1us <= '1';",
"       if TIMER_10us_COUNT = 0 then",
"         TIMER_10us_COUNT <= TIMER_10us_MAX;",
"         TIMER_10us <= '1';",
"         if TIMER_100us_COUNT = 0 then",
"           TIMER_100us_COUNT <= TIMER_100us_MAX;",
"           TIMER_100us <= '1';",
"           if TIMER_1ms_COUNT = 0 then",
"             TIMER_1ms_COUNT <= TIMER_1ms_MAX;",
"             TIMER_1ms <= '1';",
"           else",
"             TIMER_1ms_COUNT <= TIMER_1ms_COUNT - 1;",
"           end if;",
"         else",
"           TIMER_100us_COUNT <= TIMER_100us_COUNT - 1;",
"         end if;",
"       else",
"         TIMER_10us_COUNT <= TIMER_10us_COUNT - 1;",
"       end if;",
"    else",
"       TIMER_1us_COUNT <= TIMER_1us_COUNT - 1;",
"    end if;",
"    if RST = '1' then",
"       TIMER_1us_COUNT <= TIMER_1us_MAX;",
"       TIMER_1us <= '0';",
"       TIMER_10us_COUNT <= TIMER_10us_MAX;",
"       TIMER_10us <= '0';",
"       TIMER_100us_COUNT <= TIMER_100us_MAX;",
"       TIMER_100us <= '0';",
"       TIMER_1ms_COUNT <= TIMER_1ms_MAX;",
"       TIMER_1ms <= '0';",
"    end if;",
"  end process;",
"",
"\n".join(clock_generator),
"\n".join(reset_generator),
"\n".join(definitions),
"",
"end architecture RTL;",
"",
"--+============================================================================+",
"--|                       **END OF AUTO GENERATED CODE**                       |",
"--+============================================================================+",
    ]
    outputfile.write("\n".join(system))
