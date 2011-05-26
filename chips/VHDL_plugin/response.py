"""VHDL generation of the asynchronous OutputPort"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


def write(stream):

    identifier = stream.a.get_identifier()
    bits = stream.get_bits()

    ports = [
    ]

    declarations = [
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --OutPort({0}, {1})".format(identifier, bits),
    "  process",
    "    file OUTFILE : text open write_mode is \"resp_{0}.txt\";".format(identifier),
    "    variable OUTLINE : LINE;",
    "    variable VALUE : integer;",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier),
    "    if STREAM_{0}_STB = '1' then".format(identifier),
    "      STREAM_{0}_ACK <= '1';".format(identifier),
    "    end if;"
    "    if STREAM_{0}_STB = '1' and STREAM_{0}_ACK = '1' then".format(identifier),
    "      VALUE := to_integer(signed(STREAM_{0}));".format(identifier),
    "      write(OUTLINE, VALUE);",
    "      writeline(OUTFILE, OUTLINE);",
    "    end if;"
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
