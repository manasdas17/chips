"""VHDL generation of the Printer Primitive"""

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

    ports = [
    ]

    declarations = [
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --Printer({0})".format(identifier),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier),
    "    if STREAM_{0}_STB = '1' and STREAM_{0}_ACK = '0' then".format(identifier),
    "      PRINT(STREAM_{0});".format(identifier),
    "      STREAM_{0}_ACK <= '1';".format(identifier),
    "    end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
