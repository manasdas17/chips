#!/usr/bin/env python
"""VHDL generation of unary operators"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(stream):

    identifier = stream.get_identifier()
    bits = stream.get_bits()
    identifier_a = stream.a.get_identifier()
    constant = stream.constant

    expressions = {
    'srn' : "STREAM_{0} <= SR( STREAM_{1}, {2})",
    'sln' : "STREAM_{0} <= SL( STREAM_{1}, {2})",
    'abs' : "STREAM_{0} <= ABSOLUTE(STREAM_{1})",
    'invert' : "STREAM_{0} <= not STREAM_{1}",
    'not'  : "STREAM_{0} <= LNOT(STREAM_{1})",
    }

    expression = expressions[stream.function].format(identifier, identifier_a, common.binary(constant, bits))
    expression = "          {0};".format(expression)

    ports = [
    ]

    declarations = [
    "  signal STATE_{0}      : BINARY_STATE_TYPE;".format(identifier),
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "",
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --STREAM {0} Unary({1}, {2}, '{3}')".format(identifier, identifier_a, constant, stream.function),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    case STATE_{0} is".format(identifier),
    "      when BINARY_INPUT =>",
    "        if STREAM_{0}_STB = '1' then".format(identifier_a),
    "          STREAM_{0}_ACK <= '1';".format(identifier_a),
    expression,
    "          STREAM_{0}_STB <= '1';".format(identifier),
    "          STATE_{0} <= BINARY_OUTPUT;".format(identifier),
    "        end if;",
    "      when BINARY_OUTPUT =>",
    "        STREAM_{0}_ACK <= '0';".format(identifier_a),
    "        if STREAM_{0}_ACK = '1' then".format(identifier),
    "           STREAM_{0}_STB <= '0';".format(identifier),
    "           STATE_{0} <= BINARY_INPUT;".format(identifier),
    "        end if;",
    "     end case;",
    "     if RST = '1' then",
    "       STREAM_{0}_STB <= '0';".format(identifier),
    "       STREAM_{0}_ACK <= '0';".format(identifier_a),
    "       STATE_{0} <= BINARY_INPUT;".format(identifier),
    "     end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
