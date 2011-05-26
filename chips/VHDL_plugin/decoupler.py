"""VHDL generation of the Lookup Primitive"""

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

    ports = [
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal RDY_{0}        : std_logic;".format(identifier),
    "",
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --STREAM {0} Decoupler()".format(identifier),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier_a),
    "    if STREAM_{0}_STB = '1' then".format(identifier_a),
    "      STREAM_{0}_ACK <= '1';".format(identifier_a),
    "      STREAM_{0} <= STREAM_{1};".format(identifier, identifier_a),
    "      RDY_{0} <= '1';".format(identifier_a),
    "    end if;",
    "    if RST = '1' then",
    "      STREAM_{0}_ACK <= '0';".format(identifier_a),
    "      RDY_{0} <= '0';".format(identifier_a),
    "    end if;",
    "  end process;",
    "",
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_STB <= RDY_{0};".format(identifier),
    "    if STREAM_{0}_ACK = '1' then".format(identifier),
    "      STREAM_{0}_STB <= '0';".format(identifier),
    "    end if;",
    "  end process;",
    ]

    return ports, declarations, definitions
