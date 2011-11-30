"""Generates VHDL for counter primitive"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(stream):

    identifier = stream.get_identifier()
    start, stop, step = stream.start, stream.stop, stream.step
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
    "  --STREAM {0} Counter({1}, {2}, {3}, {4})".format(identifier, start, stop, step, bits),
    "  process",
    "  begin",
    "    wait until rising_edge(CLK);",
    "    STREAM_{0}_STB <= '1';".format(identifier),
    "    if STREAM_{0}_ACK = '1' then".format(identifier),
    "      STREAM_{0}_STB <= '0';".format(identifier),
    "      STREAM_{0} <= STD_RESIZE(ADD(STREAM_{0}, {1}), {2});".format(identifier, common.binary(step, bits), bits),
    "      if STREAM_{0} = {1} then".format(identifier, common.binary(stop, bits)),
    "        STREAM_{0} <= {1};".format(identifier, common.binary(start, bits)),
    "      end if;",
    "    end if;",
    "    if RST = '1' then",
    "      STREAM_{0}_STB <= '0';".format(identifier),
    "      STREAM_{0} <= {1};".format(identifier, common.binary(start, bits)),
    "    end if;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
