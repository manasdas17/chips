from __future__ import division

"""VHDL generation of the HexPrinter primitive"""

from math import ceil

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
    bits_a = stream.a.get_bits()
    identifier_a = stream.a.get_identifier()
    num_digits = stream.get_num_digits()

    def upper(x):
        return min(((x*4)+3, bits_a-1))

    def lower(x):
        return i*4

    def padding(x):
        bits = (upper(x) - lower(x)) + 1
        padding = 4-bits
        if padding == 0:
            return ""
        else:
            string = ['"']
            for i in range(bits):
                string.append("0")
            string.append('" & ')
            return ''.join(string)

    nibbles = []
    for i in range(num_digits):
        nibbles.append(
"        NIBBLE({0}) := {1}BINARY_{2}({3} downto {4});".format(i, padding(i), identifier, upper(i), lower(i))
        )


    ports = [
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal SIGN_{0}       : std_logic;".format(identifier),
    "  signal STATE_{0}      : HEX_FORMATER_STATE_TYPE;".format(identifier),
    "  signal BINARY_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits_a - 1),
    "  signal CURSOR_{0}     : integer range 0 to {1};".format(identifier, num_digits-1),
    "",
    ]


    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --STREAM {0} HexPrinter({1})".format(identifier, identifier_a),
"  process",
"    type NIBBLE_TYPE is array (0 to {0}) of std_logic_vector(3 downto 0);".format(num_digits-1),
"    variable NIBBLE : NIBBLE_TYPE;",
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(identifier),

"      when INPUT_A =>",
"        if STREAM_{0}_STB = '1' then".format(identifier_a),
"          STREAM_{0}_ACK <= '1';".format(identifier_a),
"          SIGN_{0} <= STREAM_{1}({2});".format(identifier, identifier_a, bits_a-1),
"          BINARY_{0} <= std_logic_vector(abs(signed(STREAM_{1})));".format(identifier, identifier_a),
"          CURSOR_{0} <= {1};".format(identifier, num_digits-1),
"          STATE_{0} <= OUTPUT_SIGN;".format(identifier),
"        end if;",
"",
"      when OUTPUT_SIGN =>",
"        if SIGN_{0} = '1' then".format(identifier),
'          STREAM_{0} <= "00101101";'.format(identifier),
"          STREAM_{0}_STB <= '1';".format(identifier),
"          if STREAM_{0}_ACK = '1' then".format(identifier),
"            STREAM_{0}_STB <= '0';".format(identifier),
"            STATE_{0} <= OUTPUT_DIGITS;".format(identifier),
"          end if;",
"        end if;",
"",
"      when OUTPUT_DIGITS =>",
"        STREAM_{0}_ACK <= '0';".format(identifier_a),
"\n".join(nibbles),
"        case NIBBLE(CURSOR_{0}) is".format(identifier),
'            when X"0" => STREAM_{0} <= X"30";'.format(identifier),
'            when X"1" => STREAM_{0} <= X"31";'.format(identifier),
'            when X"2" => STREAM_{0} <= X"32";'.format(identifier),
'            when X"3" => STREAM_{0} <= X"33";'.format(identifier),
'            when X"4" => STREAM_{0} <= X"34";'.format(identifier),
'            when X"5" => STREAM_{0} <= X"35";'.format(identifier),
'            when X"6" => STREAM_{0} <= X"36";'.format(identifier),
'            when X"7" => STREAM_{0} <= X"37";'.format(identifier),
'            when X"8" => STREAM_{0} <= X"38";'.format(identifier),
'            when X"9" => STREAM_{0} <= X"39";'.format(identifier),
'            when X"A" => STREAM_{0} <= X"61";'.format(identifier),
'            when X"B" => STREAM_{0} <= X"62";'.format(identifier),
'            when X"C" => STREAM_{0} <= X"63";'.format(identifier),
'            when X"D" => STREAM_{0} <= X"64";'.format(identifier),
'            when X"E" => STREAM_{0} <= X"65";'.format(identifier),
'            when X"F" => STREAM_{0} <= X"66";'.format(identifier),
'            when others => null;',
"        end case;",
"        STREAM_{0}_STB <= '1';".format(identifier),
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"          STREAM_{0}_STB <= '0';".format(identifier),
"          if CURSOR_{0} = 0 then".format(identifier),
"            STATE_{0} <= INPUT_A;".format(identifier),
"          else",
"            CURSOR_{0} <= CURSOR_{0} - 1;".format(identifier),
"          end if;",
"        end if;",
"",
"     end case;",
"     if RST = '1' then",
"       STREAM_{0}_STB <= '0';".format(identifier),
"       STREAM_{0}_ACK <= '0';".format(identifier_a),
"       STATE_{0} <= INPUT_A;".format(identifier),
"     end if;",
"  end process;",
"",
    ]

    return ports, declarations, definitions
