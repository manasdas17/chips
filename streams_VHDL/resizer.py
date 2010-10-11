"""VHDL generation of the Resizer Primitive"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

def write(stream):

    identifier = stream.get_identifier()
    bits = stream.get_bits()
    identifier_a = stream.a.get_identifier()
    bits_a = stream.a.get_bits()

    if bits_a < bits :
        expression = "  STREAM_{0} <= resize(signed(STREAM_{1}), {2});".format(identifier, identifier_a, bits)
    elif bits_a == bits:
        expression = "  STREAM_{0} <= STREAM_{1};".format(identifier, identifier_a)
    else:
        expression = "  STREAM_{0} <= STREAM_{1}({2} downto 0);".format(identifier, identifier_a, bits-1)

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
    "  --stream {0} Resizer({1}, {2})".format(identifier, identifier_a, bits),
    "  STREAM_{1}_ACK <= STREAM_{0}_ACK;".format(identifier, identifier_a),
    "  STREAM_{0}_STB <= STREAM_{1}_STB;".format(identifier, identifier_a),
    expression,
    "",
    ]

    return ports, declarations, definitions
