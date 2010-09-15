"""VHDL generation of the Skip Primitive"""

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

    ports = [
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal STREAM_{0}_BRK : std_logic;".format(identifier),
    "  signal STREAM_{0}_SKP : std_logic;".format(identifier),
    "",
    ]

    definitions = [
    "  --STREAM {0} Skip()".format(identifier),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_STB <= not STREAM_{0}_ACK;".format(identifier),
    "  end process;",
    '  STREAM_{0} <= "0";'.format(identifier),
    "  STREAM_{0}_BRK <= '0';".format(identifier),
    "  STREAM_{0}_SKP <= '1';".format(identifier),
    "",
    ]

    return ports, declarations, definitions
