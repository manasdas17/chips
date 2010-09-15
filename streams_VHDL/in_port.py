"""VHDL generation of an asynchronous input port"""

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
    name = stream.name
    bits = stream.get_bits()

    ports = [
    "    IN_{0} : in std_logic_vector({1} downto 0)".format(name, bits - 1),
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal STREAM_{0}_BRK : std_logic;".format(identifier),
    "  signal STREAM_{0}_SKP : std_logic;".format(identifier),
    "  signal IN_{0}_DEL     : std_logic_vector({1} downto 0);".format(name, bits - 1),
    "  signal IN_{0}_DEL_DEL : std_logic_vector({1} downto 0);".format(name, bits - 1),
    "",
    ]

    definitions = [
    "  --STREAM {0} InPort({1}, {2})".format(identifier, name, bits),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    IN_{0}_DEL <= IN_{0};".format(name),
    "    IN_{0}_DEL_DEL <= IN_{0}_DEL;".format(name),
    "    STREAM_{0} <= IN_{1}_DEL_DEL;".format(identifier,  name),
    "  end process;",
    "  STREAM_{0}_STB <= '1';".format(identifier),
    "  STREAM_{0}_BRK <= '0';".format(identifier),
    "  STREAM_{0}_SKP <= '0';".format(identifier),
    "",
    ]

    return ports, declarations, definitions
