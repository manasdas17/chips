"""VHDL generation of the asynchronous OutputPort"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

import common

def write(stream):

    identifier = stream.a.get_identifier()
    name = stream.name
    bits = stream.get_bits()

    ports = [
    "    OUT_{0} : out std_logic_vector({1} downto 0)".format(name, bits - 1),
    ]

    declarations = [
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --OutPort({0}, {1}, {2})".format(identifier, name, bits),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier),
    "    if STREAM_{0}_STB = '1' then".format(identifier),
    "      STREAM_{0}_ACK <= '1';".format(identifier),
    "      OUT_{1} <= STREAM_{0};".format(identifier,  name),
    "    end if;"
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
