from __future__ import division

"""VHDL generation of the Printer primitive"""

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
    digit_bits = num_digits * 4

    ports = [
    ]

    declarations = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --STREAM {0} Printer({1})".format(identifier, identifier_a),
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal SIGN_{0}       : std_logic;".format(identifier),
    "  signal STATE_{0}      : PRINTER_STATE_TYPE;".format(identifier),
    "  type SHIFTER_{0}_TYPE is array (0 to {1}) of std_logic_vector(3 downto 0);".format(identifier, num_digits - 1),
    "  signal BINARY_{0}     : std_logic_vector({1} downto 0);".format(identifier, digit_bits - 1),
    "  signal SHIFTER_{0}    : SHIFTER_{0}_TYPE;".format(identifier),
    "  signal COUNT_{0}      : integer range 0 to {1};".format(identifier, digit_bits-1),
    "  signal CURSOR_{0}     : integer range 0 to {1};".format(identifier, num_digits-1),
    "",
    ]


    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --STREAM {0} Printer({1})".format(identifier, identifier_a),
"  process",
"    variable CARRY_{0} : std_logic_vector({1} downto 0);".format(identifier, num_digits),
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(identifier),

"      when INPUT_A =>",
"        if STREAM_{0}_STB = '1' then".format(identifier_a),
"          STREAM_{0}_ACK <= '1';".format(identifier_a),
"          SIGN_{0} <= STREAM_{1}({2});".format(identifier, identifier_a, bits_a-1),
'          SHIFTER_{0} <= (others => "0000");'.format(identifier),
'          BINARY_{0} <= STD_RESIZE(ABSOLUTE(STREAM_{1}), {2});'.format(identifier, identifier_a, digit_bits),
"          COUNT_{0} <= {1};".format(identifier, digit_bits-1),
"          STATE_{0} <= SHIFT;".format(identifier),
"        end if;",
"",
"      when SHIFT =>",
"        STREAM_{0}_ACK <= '0';".format(identifier_a),
"        CARRY_{0} := (Others => '0');".format(identifier),
"        CARRY_{0}(0) := BINARY_{0}({1});".format(identifier, digit_bits-1),
"        for DIGIT in 0 to {1} loop".format(identifier, num_digits-1),
"            case SHIFTER_{0}(DIGIT) is".format(identifier),
'                when "0101" =>',
"                  CARRY_{0}(DIGIT+1) := '1';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= "000" & CARRY_{0}(DIGIT);'.format(identifier),
'                when "0110" =>',
"                  CARRY_{0}(DIGIT+1) := '1';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= "001" & CARRY_{0}(DIGIT);'.format(identifier),
'                when "0111" =>',
"                  CARRY_{0}(DIGIT+1) := '1';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= "010" & CARRY_{0}(DIGIT);'.format(identifier),
'                when "1000" =>',
"                  CARRY_{0}(DIGIT+1) := '1';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= "011" & CARRY_{0}(DIGIT);'.format(identifier),
'                when "1001" =>',
"                  CARRY_{0}(DIGIT+1) := '1';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= "100" & CARRY_{0}(DIGIT);'.format(identifier),
"                when others =>",
"                  CARRY_{0}(DIGIT+1) := '0';".format(identifier),
'                  SHIFTER_{0}(DIGIT) <= SHIFTER_{0}(DIGIT)(2 downto 0) & CARRY_{0}(DIGIT);'.format(identifier),
"            end case;",
"        end loop;",
"        BINARY_{0} <= BINARY_{0}({1} downto 0) & '0';".format(identifier, digit_bits-2),
"        if COUNT_{0} = 0 then".format(identifier),
"          STATE_{0} <= OUTPUT_SIGN;".format(identifier),
"          CURSOR_{0} <= {1};".format(identifier, num_digits-1),
"        else",
"          COUNT_{0} <= COUNT_{0} - 1;".format(identifier),
"        end if;",
"",
"      when OUTPUT_SIGN =>",
"        if SIGN_{0} = '1' then".format(identifier),
'          STREAM_{0} <= "00101101";'.format(identifier),
"          STREAM_{0}_STB <= '1';".format(identifier),
"          if STREAM_{0}_ACK = '1' then".format(identifier),
"            STREAM_{0}_STB <= '0';".format(identifier),
"            STATE_{0} <= OUTPUT_Z;".format(identifier),
"          end if;",
"        else",
"          STATE_{0} <= OUTPUT_Z;".format(identifier),
"        end if;",
"",
"      when OUTPUT_Z =>",
"        STREAM_{0}_STB <= '1';".format(identifier),
'        STREAM_{0} <= "0011" & SHIFTER_{0}(CURSOR_{0});'.format(identifier, num_digits-1),
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"          STREAM_{0}_STB <= '0';".format(identifier),
"          if CURSOR_{0} = 0 then".format(identifier),
"            STATE_{0} <= OUTPUT_NL;".format(identifier),
"          else",
"            CURSOR_{0} <= CURSOR_{0} - 1;".format(identifier),
"          end if;",
"        end if;",
"",
"      when OUTPUT_NL =>",
"        STREAM_{0}_STB <= '1';".format(identifier),
'        STREAM_{0} <= X"0A";'.format(identifier),
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"          STREAM_{0}_STB <= '0';".format(identifier),
"          STATE_{0} <= INPUT_A;".format(identifier),
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
