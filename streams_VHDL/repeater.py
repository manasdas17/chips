"""VHDL generation of the Repeater Primitive"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import common

def write(stream):

    value = stream.value
    identifier = stream.get_identifier()
    bits = stream.get_bits()

    ports = [
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "",
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --STREAM {0} Repeater({1}, {2})".format(identifier, value, bits),
    "  STREAM_{0} <= {1};".format(identifier, common.binary(value, bits)),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_STB <= not STREAM_{0}_ACK;".format(identifier),
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
