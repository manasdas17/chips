"""VHDL generation of the Console Primitive"""

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

    ports = [
    ]

    declarations = [
    ]

    definitions = [
    "  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
    "  --Console({0})".format(identifier),
    "  process",
    "    variable OUTPUT_LINE : line;",
    "    variable INT  : integer;",
    "    variable CHAR : character;",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_ACK <= '0';".format(identifier),
    "    if STREAM_{0}_STB = '1' and STREAM_{0}_ACK = '0' then".format(identifier),
    "      INT := (to_integer(unsigned(STREAM_{0})));".format(identifier),
    "      CHAR := character'val (INT);",
    "      if INT = 10 then",
    "        writeline(output, OUTPUT_LINE);",
    "      else",
    "        write(OUTPUT_LINE, CHAR);",
    "      end if;",
    "      STREAM_{0}_ACK <= '1';".format(identifier),
    "    end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
