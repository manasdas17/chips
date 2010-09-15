#!/usr/bin/env python
"""VHDL generation of binary operators"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import divider

def write(stream):

    identifier = stream.get_identifier()
    bits = stream.get_bits()
    identifier_a = stream.a.get_identifier()
    identifier_b = stream.b.get_identifier()

    if stream.function == 'div':
        return divider.write(stream)

    expressions = {
    'add' : "STREAM_{0} <= ADD( STREAM_{1}, STREAM_{2})",
    'sub' : "STREAM_{0} <= SUB( STREAM_{1}, STREAM_{2})",
    'mul' : "STREAM_{0} <= MUL( STREAM_{1}, STREAM_{2})",
    'and' : "STREAM_{0} <= BAND(STREAM_{1}, STREAM_{2})",
    'or'  : "STREAM_{0} <= BOR( STREAM_{1}, STREAM_{2})",
    'xor' : "STREAM_{0} <= BXOR(STREAM_{1}, STREAM_{2})",
    'sl'  : "STREAM_{0} <= SL(  STREAM_{1}, STREAM_{2})",
    'sr'  : "STREAM_{0} <= SR(  STREAM_{1}, STREAM_{2})",
    'eq'  : "STREAM_{0} <= EQ(  STREAM_{1}, STREAM_{2})",
    'ne'  : "STREAM_{0} <= NE(  STREAM_{1}, STREAM_{2})",
    'lt'  : "STREAM_{0} <= LT(  STREAM_{1}, STREAM_{2})",
    'le'  : "STREAM_{0} <= LE(  STREAM_{1}, STREAM_{2})",
    'gt'  : "STREAM_{0} <= GT(  STREAM_{1}, STREAM_{2})",
    'ge'  : "STREAM_{0} <= GE(  STREAM_{1}, STREAM_{2})",
    }

    expression = expressions[stream.function].format(identifier, identifier_a, identifier_b)
    expression = "          {0};".format(expression)

    ports = [
    ]

    declarations = [
    "  signal STATE_{0}      : BINARY_STATE_TYPE;".format(identifier),
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal STREAM_{0}_BRK : std_logic;".format(identifier),
    "  signal STREAM_{0}_SKP : std_logic;".format(identifier),
    "",
    ]

    definitions = [
    "  --STREAM {0} Binary({1}, {2}, '{3}')".format(identifier, identifier_a, identifier_b, stream.function),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    case STATE_{0} is".format(identifier),
    "      when BINARY_INPUT =>",
    "        if STREAM_{0}_STB = '1' and STREAM_{1}_STB = '1' then".format(identifier_a, identifier_b),
    "          STREAM_{0}_ACK <= '1'; STREAM_{1}_ACK <= '1';".format(identifier_a, identifier_b),
    expression,
    "          STREAM_{0}_STB <= '1';".format(identifier),
    "          STATE_{0} <= BINARY_OUTPUT;".format(identifier),
    "        end if;",
    "      when BINARY_OUTPUT =>",
    "        STREAM_{0}_ACK <= '0'; STREAM_{1}_ACK <= '0';".format(identifier_a, identifier_b),
    "        if STREAM_{0}_ACK = '1' then".format(identifier),
    "           STREAM_{0}_STB <= '0';".format(identifier),
    "           STATE_{0} <= BINARY_INPUT;".format(identifier),
    "        end if;",
    "     end case;",
    "     if RST = '1' then",
    "       STREAM_{0}_STB <= '0';".format(identifier),
    "       STREAM_{0}_ACK <= '0';".format(identifier_a),
    "       STREAM_{0}_ACK <= '0';".format(identifier_b),
    "       STATE_{0} <= BINARY_INPUT;".format(identifier),
    "     end if;",
    "  end process;",
    "  STREAM_{0}_BRK <= '0';".format(identifier),
    "  STREAM_{0}_SKP <= '0';".format(identifier),
    "",
    ]

    return ports, declarations, definitions
