"""VHDL generation of the Stepper Primitive"""

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
    num_inputs = len(stream.a)


    ports = [
    ]

    declarations = [
"  signal STATE_{0}      : STEPPER_STATE_TYPE;".format(identifier),
"  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits-1),
"  signal STREAM_{0}_STB : std_logic;".format(identifier),
"  signal STREAM_{0}_ACK : std_logic;".format(identifier),
"  signal STREAM_{0}_BRK : std_logic;".format(identifier),
"  signal STREAM_{0}_SKP : std_logic;".format(identifier),
"  signal SEL_{0}        : integer range 0 to {1};".format(identifier, num_inputs-1),
"",
    ]

    definitions = [
"  --Stream {0} Stepper(...)".format(identifier),
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(identifier),
"      when STEPPER_INPUT =>",
"        case SEL_{0} is".format(identifier),
    ]

    for index, source in enumerate(stream.a):
        source_identifier = source.get_identifier()
        left = source.get_bits()-1
        definitions.extend([
"          when {0} =>".format(index),
"            if STREAM_{0}_STB = '1' then".format(source_identifier),
"              STREAM_{0}_ACK <= '1';".format(source_identifier),
"              STREAM_{0} <= (others => STREAM_{1}({2}));".format(identifier, source_identifier, left),
"              STREAM_{0}({2} downto 0) <= STREAM_{1};".format(identifier, source_identifier, left),
"              STREAM_{0}_SKP <= STREAM_{1}_SKP;".format(identifier, source_identifier, left),
"              if STREAM_{0}_BRK = '1' then".format(source_identifier),
"                if SEL_{0} = {1} then".format(identifier, num_inputs-1),
"                  SEL_{0} <= 0;".format(identifier),
"                else",
"                  SEL_{0} <= SEL_{0} + 1;".format(identifier),
"                end if;",
"                STATE_{0} <= STEPPER_ACK;".format(identifier),
"              else",
"                STREAM_{0}_STB <= '1';".format(identifier),
"                STATE_{0} <= STEPPER_OUTPUT;".format(identifier),
"              end if;",
"            end if;",
        ])

    definitions.extend([
"        end case;".format(identifier),
"      when STEPPER_ACK =>",
    ])
    for source in stream.a:
        source_identifier = source.get_identifier()
        definitions.extend([
"        STREAM_{0}_ACK <= '0';".format(source_identifier),
        ])
    definitions.extend([
"        STATE_{0} <= STEPPER_INPUT;".format(identifier),
"      when STEPPER_OUTPUT =>",
    ])
    for source in stream.a:
        source_identifier = source.get_identifier()
        definitions.extend([
"        STREAM_{0}_ACK <= '0';".format(source_identifier),
        ])
    definitions.extend([
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"           STREAM_{0}_STB <= '0';".format(identifier),
"           STATE_{0} <= STEPPER_INPUT;".format(identifier),
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
"       STREAM_{0}_STB <= '0';".format(identifier),
"       STATE_{0} <= STEPPER_INPUT;".format(identifier),
"       SEL_{0} <= 0;".format(identifier),
"     end if;",
"  end process;",
"  STREAM_{0}_BRK <= '0';".format(identifier),
"",
    ])

    return ports, declarations, definitions
