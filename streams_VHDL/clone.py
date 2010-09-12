"""VHDL generation of the Clone Primitive"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

class Tee:
    ident = 0
    def __init__(self, y, z):
        self.identifier = 'TEE_' + str(Tee.ident)
        Tee.ident += 1
        self.y = y
        self.z = z

    def get_identifier(self): return self.identifier

    def get_declarations(self, bits):
        identifier_y = self.y.get_identifier()
        identifier_z = self.z.get_identifier()
        identifier = self.get_identifier()
        declarations = [
        "  signal STATE_{0}      : TEE_STATE_TYPE;".format(identifier),
        "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
        "  signal STREAM_{0}_STB : std_logic;".format(identifier),
        "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
        "",
        ]
        if hasattr(self.y, 'get_definitions'):
            declarations.extend(self.y.get_declarations(bits))
        else:
            declarations.extend([
        "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(self.y.get_identifier(), bits - 1),
        "  signal STREAM_{0}_STB : std_logic;".format(self.y.get_identifier()),
        "  signal STREAM_{0}_ACK : std_logic;".format(self.y.get_identifier()),
        "",
            ])
        if hasattr(self.z, 'get_definitions'):
            declarations.extend(self.z.get_declarations(bits))
        else:
            declarations.extend([
        "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(self.z.get_identifier(), bits - 1),
        "  signal STREAM_{0}_STB : std_logic;".format(self.z.get_identifier()),
        "  signal STREAM_{0}_ACK : std_logic;".format(self.z.get_identifier()),
        "",
            ])
        return declarations

    def get_definitions(self):
        identifier_y = self.y.get_identifier()
        identifier_z = self.z.get_identifier()
        identifier = self.get_identifier()
        definitions = [
        "  process",
        "  begin",
        "    wait until rising_edge(CLK);",
        "    STREAM_{0} <= STREAM_{1};".format(identifier_y, identifier),
        "    STREAM_{0} <= STREAM_{1};".format(identifier_z, identifier),
        "    case STATE_{0} is".format(identifier),
        "      when TEE_INPUT_A =>",
        "        if STREAM_{0}_STB = '1' then".format(identifier),
        "          STREAM_{0}_STB <= '1'; STREAM_{1}_STB <= '1';".format(identifier_y, identifier_z),
        "          STREAM_{0}_ACK <= '1';".format(identifier),
        "          STATE_{0} <= TEE_WAIT_YZ;".format(identifier),
        "        end if;",
        "",
        "      when TEE_WAIT_YZ =>",
        "        STREAM_{0}_ACK <= '0';".format(identifier),
        "        if STREAM_{0}_ACK = '1' and STREAM_{1}_ACK = '1' then".format(identifier_y, identifier_z),
        "          STREAM_{0}_STB <= '0'; STREAM_{1}_STB <= '0';".format(identifier_y, identifier_z),
        "          STATE_{0} <= TEE_INPUT_A;".format(identifier),
        "        elsif STREAM_{0}_ACK = '1' then".format(identifier_y),
        "          STREAM_{0}_STB <= '0';".format(identifier_y),
        "          STATE_{0} <= TEE_WAIT_Z;".format(identifier),
        "        elsif STREAM_{0}_ACK = '1' then".format(identifier_z),
        "          STREAM_{0}_STB <= '0';".format(identifier_z),
        "          STATE_{0} <= TEE_WAIT_Y;".format(identifier),
        "        end if;",
        "  ",
        "      when TEE_WAIT_Y =>",
        "        if STREAM_{0}_ACK = '1' then".format(identifier_y),
        "          STREAM_{0}_STB <= '0';".format(identifier_y),
        "          STATE_{0} <= TEE_INPUT_A;".format(identifier),
        "        end if;",
        "",
        "      when TEE_WAIT_Z =>",
        "        if STREAM_{0}_ACK = '1' then".format(identifier_z),
        "          STREAM_{0}_STB <= '0';".format(identifier_z),
        "          STATE_{0} <= TEE_INPUT_A;".format(identifier),
        "        end if;",
        "",
        "    end case;",
        "    if RST = '1' then",
        "      STREAM_{0}_STB <= '0';".format(identifier_y),
        "      STREAM_{0}_STB <= '0';".format(identifier_z),
        "      STREAM_{0}_ACK <= '0';".format(identifier),
        "      STATE_{0} <= TEE_INPUT_A;".format(identifier),
        "    end if;",
        "  end process;",
        "",
        ]
        if hasattr(self.y, 'get_definitions'):
            definitions.extend(self.y.get_definitions())
        if hasattr(self.z, 'get_definitions'):
            definitions.extend(self.z.get_definitions())
        return definitions

def balance_reduce(sequence, function):
    length = len(sequence)
    if length <= 1: return sequence[0]
    a, b = sequence[:length//2], sequence[length//2:]
    return function(balance_reduce(a, function), balance_reduce(b, function))
     

def write(stream):
    source_identifier = stream.a.get_identifier()
    bits = stream.a.get_bits()
    spawn = stream._spawn
    tee = balance_reduce(spawn, Tee)
    identifier = tee.get_identifier()

    ports = []

    declarations = []
    declarations.extend(tee.get_declarations(bits))

    definitions = [
    "  STREAM_{0} <= STREAM_{1};".format(identifier, source_identifier),
    "  STREAM_{0}_STB <= STREAM_{1}_STB;".format(identifier, source_identifier),
    "  STREAM_{1}_ACK <= STREAM_{0}_ACK;".format(identifier, source_identifier),
    "",
    ]
    definitions.extend(tee.get_definitions())

    return ports, declarations, definitions
