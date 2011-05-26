from __future__ import division

"""VHDL generation of the SerialOut Primitive"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(stream):

    identifier = stream.get_identifier()
    identifier_a = stream.a.get_identifier()
    name = stream.name
    clock_divider = stream.clock_rate/stream.baud_rate

    ports = [
"    {0} : out std_logic".format(name),
    ]

    declarations = [
"  signal STATE_{0}           : SERIAL_OUT_STATE_TYPE;".format(identifier),
"  constant CLOCK_DIVIDER_{0} : Unsigned(11 downto 0) := To_unsigned({1}, 12);".format(identifier, int(round(clock_divider))-1),
"  signal BAUD_COUNT_{0}      : Unsigned(11 downto 0);".format(identifier),
"  signal DATA_{0}            : std_logic_vector(7 downto 0);".format(identifier),
"  signal X16CLK_EN_{0}       : std_logic;".format(identifier),

    ]


    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --serial output port baud rate generator",
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    if BAUD_COUNT_{0} = CLOCK_DIVIDER_{0} then".format(identifier),
"      BAUD_COUNT_{0} <= (others => '0');".format(identifier),
"      X16CLK_EN_{0}  <= '1';".format(identifier),
"    else",
"      BAUD_COUNT_{0} <= BAUD_COUNT_{0} + 1;".format(identifier),
"      X16CLK_EN_{0}  <= '0';".format(identifier),
"    end if;",
"    if RST = '1' then",
"      BAUD_COUNT_{0} <= (others => '0');".format(identifier),
"      X16CLK_EN_{0}  <= '0';".format(identifier),
"    end if;",
"  end process;",
"",            
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(identifier),
"      when IDLE =>",
"        if STREAM_{0}_STB = '1'  then".format(identifier_a),
"          STREAM_{0}_ACK <= '1';".format(identifier_a),
"          DATA_{0} <= STREAM_{1};".format(identifier, identifier_a),
"          STATE_{0}     <= WAIT_EN;".format(identifier),
"        end if;",
"      when WAIT_EN =>",
"        STREAM_{0}_ACK <= '0';".format(identifier_a),
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= START;".format(identifier),
"        end if;",
"      when START =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX0;".format(identifier),
"        end if;",
"        {0} <= '0'; ".format(name),
"      when TX0 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX1;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(0);".format(identifier, name),
"      when TX1 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX2;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(1);".format(identifier, name),
"      when TX2 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX3;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(2);".format(identifier, name),
"      when TX3 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX4;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(3);".format(identifier, name),
"      when TX4 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX5;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(4);".format(identifier, name),
"      when TX5 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX6;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(5);".format(identifier, name),
"      when TX6 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= TX7;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(6);".format(identifier, name),
"      when TX7 =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= STOP;".format(identifier),
"        end if;",
"        {1} <= DATA_{0}(7);".format(identifier, name),
"      when STOP =>",
"        if X16CLK_EN_{0} = '1' then".format(identifier),
"          STATE_{0} <= IDLE;".format(identifier),
"        end if;",
"        {0} <= '1';".format(name),
"      when others =>",
"        STATE_{0} <= IDLE;".format(identifier),
"      end case;",
"    if RST = '1' then",
"      STREAM_{0}_ACK <= '0';".format(identifier_a),
"      STATE_{0} <= IDLE;".format(identifier),
"    end if; ",
"  end process;",
    ]

    return ports, declarations, definitions
