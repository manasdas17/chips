"""VHDL generation of the Switch Primitive"""

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
    sel_bits = stream.select.get_bits()
    identifier_sel = stream.select.get_identifier()


    ports = [
    ]

    declarations = [
"  signal STATE_{0}      : SWITCH_STATE_TYPE;".format(identifier),
"  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
"  signal STREAM_{0}_STB : std_logic;".format(identifier),
"  signal STREAM_{0}_ACK : std_logic;".format(identifier),
"  signal SEL_{0}        : std_logic_vector({1} downto 0);".format(identifier, sel_bits - 1),
"",
    ]

    definitions = [
"  --SWITCH {0} Switch({1}, ...)".format(identifier, identifier_sel,),
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(identifier),
"      when SWITCH_INPUT_SEL =>",
"        if STREAM_{0}_STB = '1' then".format(identifier_sel),
"          STREAM_{0}_ACK <= '1';".format(identifier_sel),
"          SEL_{0}   <= STREAM_{1};".format(identifier, identifier_sel),
"          STATE_{0} <= SWITCH_INPUT;".format(identifier),
"        end if;",
"      when SWITCH_INPUT =>",
"        STREAM_{0}_ACK <= '0';".format(identifier_sel),
"        case SEL_{0} is".format(identifier),
    ]

    for index, source in enumerate(stream.a):
        source_identifier = source.get_identifier()
        left = source.get_bits()-1
        definitions.extend([
"          when {0} =>".format(common.binary(index, sel_bits)),
"            if STREAM_{0}_STB = '1' then".format(source_identifier),
"              STREAM_{0} <= (others => STREAM_{1}({2}));".format(identifier, source_identifier, left),
"              STREAM_{0}({2} downto 0) <= STREAM_{1};".format(identifier, source_identifier, left),
"              STREAM_{0}_ACK <= '1';".format(source_identifier),
"              STREAM_{0}_STB <= '1';".format(identifier),
"              STATE_{0} <= SWITCH_OUTPUT;".format(identifier),
"            end if;"
        ])

    definitions.extend([
"          when Others =>".format(common.binary(index, sel_bits)),
"              STATE_{0} <= SWITCH_INPUT_SEL;".format(identifier),
"        end case;".format(identifier),
"      when SWITCH_OUTPUT =>",
    ])
    for source in stream.a:
        source_identifier = source.get_identifier()
        definitions.extend([
"        STREAM_{0}_ACK <= '0';".format(source_identifier),
        ])
    definitions.extend([
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"           STREAM_{0}_STB <= '0';".format(identifier),
"           STATE_{0} <= SWITCH_INPUT_SEL;".format(identifier),
"        end if;",
"     end case;",
"     if RST = '1' then",
    ])
    for source in stream.a:
        source_identifier = source.get_identifier()
        definitions.extend([
"       STREAM_{0}_ACK <= '0';".format(source_identifier),
        ])
    definitions.extend([
"       STREAM_{0}_ACK <= '0';".format(identifier_sel),
"       STREAM_{0}_STB <= '0';".format(identifier),
"       STATE_{0} <= SWITCH_INPUT_SEL;".format(identifier),
"     end if;",
"  end process;",
"",
    ])

    return ports, declarations, definitions
