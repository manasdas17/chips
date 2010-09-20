"""VHDL generation of the Lookup Primitive"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import common

def write(stream):

    identifier = stream.get_identifier()
    bits = stream.get_bits()
    args = stream.args
    identifier_a = stream.a.get_identifier()

    ports = [
    ]

    values = [common.binary(int(i), bits) for i in args]
    values = enumerate(values)
    values = ["{0} => {1}".format(i, j) for i, j in values]
    values = ',\n'.join(values)


    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal STATE_{0} : UNARY_STATE_TYPE;".format(identifier),
    "  type LOOKUP_{0}_TYPE is array (0 to {1}) of std_logic_vector({2} downto 0);".format(identifier, len(args)-1, bits-1),
    "  signal LOOKUP_{0} : LOOKUP_{0}_TYPE := (".format(identifier),
    values,
    "  );",
    "",
    ]

    definitions = [
    "  --STREAM {0} Lookup()".format(identifier),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    case STATE_{0} is".format(identifier),
    "      when UNARY_INPUT =>",
    "        if STREAM_{0}_STB = '1' then".format(identifier_a),
    "          STREAM_{0}_ACK <= '1';".format(identifier_a),
    "          STREAM_{0}_STB <= '1';".format(identifier),
    "          STREAM_{0} <= LOOKUP_{0}(to_integer(unsigned(STREAM_{1})));".format(identifier, identifier_a),
    "          STATE_{0} <= UNARY_OUTPUT;".format(identifier),
    "        end if;",
    "      when UNARY_OUTPUT =>",
    "        STREAM_{0}_ACK <= '0';".format(identifier_a),
    "        if STREAM_{0}_ACK = '1' then".format(identifier),
    "           STREAM_{0}_STB <= '0';".format(identifier),
    "           STATE_{0} <= UNARY_INPUT;".format(identifier),
    "        end if;",
    "     end case;",
    "     if RST = '1' then",
    "       STREAM_{0}_STB <= '0';".format(identifier),
    "       STREAM_{0}_ACK <= '0';".format(identifier_a),
    "       STATE_{0} <= UNARY_INPUT;".format(identifier),
    "     end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
