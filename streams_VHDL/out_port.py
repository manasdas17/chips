"""VHDL generation of the asynchronous OutputPort"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
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
    "  --OutPort({0}, {1}, {2})".format(identifier, name, bits),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    if STREAM_{0}_STB = '1' then".format(identifier),
    "      OUT_{1} <= STREAM_{0};".format(identifier,  name),
    "    end if;"
    "  end process;",
    "  STREAM_{0}_ACK <= '1';".format(identifier),
    "",
    ]

    return ports, declarations, definitions
