"""VHDL generation of an asynchronous input port"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(stream):

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
    "  --STREAM {0} STIMULUS({1})".format(identifier, bits),
    "  process",
    "    file INFILE : text open read_mode is \"stim_{0}.txt\";".format(identifier),
    "    variable INLINE : LINE;",
    "    variable VALUE : integer;",
    "  begin",
    "    if(not ENDFILE(INFILE)) then",
    "      readline(INFILE, INLINE);",
    "      read(INLINE, VALUE);",
    "      STREAM_{0} <= std_logic_vector(to_signed(VALUE, {1}));".format(identifier, bits),
    "      STREAM_{0}_STB <= '1';".format(identifier),
    "    end if;",
    "    while 1=1 loop",
    "      wait until rising_edge(CLK);",
    "      STREAM_{0}_STB <= '1';".format(identifier),
    "      if STREAM_{0}_ACK = '1' then".format(identifier),
    "        if(not ENDFILE(INFILE)) then",
    "          readline(INFILE, INLINE);",
    "          read(INLINE, VALUE);",
    "          STREAM_{0} <= std_logic_vector(to_signed(VALUE, {1}));".format(identifier, bits),
    "        end if;",
    "        STREAM_{0}_STB <= '0';".format(identifier),
    "      end if;",
    "    end loop;",
    "    wait;",
    "  end process;",
    "",
    ]

    return ports, declarations, definitions
