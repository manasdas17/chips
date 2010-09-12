"""VHDL generation of the Binary Division operator"""

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
    identifier_b = stream.b.get_identifier()
    bits_a = stream.a.get_bits()
    bits_b = stream.b.get_bits()

    ports = [
    ]

    declarations = [
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "  signal STATE_{0}      : DIVIDER_STATE_TYPE;".format(identifier),
    "  signal A_{0}          : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal B_{0}          : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal QUOTIENT_{0}   : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal SHIFTER_{0}    : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal REMAINDER_{0}  : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal COUNT_{0}      : integer range 0 to {1};".format(identifier, bits),
    "  signal SIGN_{0}       : std_logic;".format(identifier),
    "",
    ]

    definitions = [
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"      case STATE_{0} is".format(identifier),
"",
"        when READ_A_B =>",
"          if STREAM_{0}_STB = '1' and STREAM_{0}_STB = '1' then".format(identifier_a, identifier_b),
"            A_{0} <= std_logic_vector(abs(resize(signed(STREAM_{1}), {2})));".format(identifier, identifier_a, bits),
"            B_{0} <= std_logic_vector(abs(resize(signed(STREAM_{1}), {2})));".format(identifier, identifier_b, bits),
"            SIGN_{0} <= STREAM_{1}({3}) xor STREAM_{2}({4});".format(identifier, identifier_a, identifier_b, bits_a-1, bits_b-1),
"            STREAM_{0}_ACK <= '1';".format(identifier_a),
"            STREAM_{0}_ACK <= '1';".format(identifier_b),
"            STATE_{0} <= DIVIDE_1;".format(identifier),
"          end if;",
"",
"        when DIVIDE_1 =>",
"          STREAM_{0}_ACK <= '0';".format(identifier_a),
"          STREAM_{0}_ACK <= '0';".format(identifier_b),
"          QUOTIENT_{0} <= (others => '0');".format(identifier),
"          SHIFTER_{0} <= (others => '0');".format(identifier),
"          SHIFTER_{0}(0) <= A_{0}({1});".format(identifier, bits-1),
"          A_{0} <= A_{0}({1} downto 0) & '0';".format(identifier, bits-2),
"          COUNT_{0} <= {1};".format(identifier, bits-1),
"          STATE_{0} <= DIVIDE_2;".format(identifier),
"",
"        when DIVIDE_2 => --subtract",
"         --if SHIFTER - B is positive or zero",
"         if REMAINDER_{0}({1}) = '0' then".format(identifier, bits-1),
"           SHIFTER_{0}({1} downto 1) <= REMAINDER_{0}({2} downto 0);".format(identifier, bits-1, bits-2),
"         else",
"           SHIFTER_{0}({1} downto 1) <= SHIFTER_{0}({2} downto 0);".format(identifier, bits-1, bits-2),
"         end if;",
"         SHIFTER_{0}(0) <= A_{0}({1});".format(identifier, bits-1),
"         A_{0} <= A_{0}({1} downto 0) & '0';".format(identifier, bits-2),
"         QUOTIENT_{0} <= QUOTIENT_{0}({2} downto 0) & not(REMAINDER_{0}({1}));".format(identifier, bits-1, bits-2),
"         if COUNT_{0} = 0 then".format(identifier),
"           STATE_{0} <= WRITE_Z;".format(identifier),
"         else",
"           COUNT_{0} <= COUNT_{0} - 1;".format(identifier),
"         end if;",
"",
"      when WRITE_Z =>",
"        if SIGN_{0} = '1' then --if negative".format(identifier),
"          STREAM_{0} <= std_logic_vector(not(signed(QUOTIENT_{0}))+1);".format(identifier),
"        else",
"          STREAM_{0} <= QUOTIENT_{0};".format(identifier),
"        end if;",
"        STREAM_{0}_STB <= '1';".format(identifier),
"        if STREAM_{0}_ACK = '1' then".format(identifier),
"          STREAM_{0}_STB <= '0';".format(identifier),
"          STATE_{0} <= READ_A_B;".format(identifier),
"        end if;",
"",
"    end case;",
"    if RST = '1' then",
"      STATE_{0} <= READ_A_B;".format(identifier),
"      STREAM_{0}_ACK <= '0';".format(identifier_a),
"      STREAM_{0}_ACK <= '0';".format(identifier_b),
"      STREAM_{0}_STB <= '0';".format(identifier),
"    end if;",
"  end process;",
"",
"  --subtractor",
"  REMAINDER_{0} <= std_logic_vector(unsigned(SHIFTER_{0}) - resize(unsigned(B_{0}), {1}));".format(identifier, bits),
"",
    ]

    return ports, declarations, definitions
