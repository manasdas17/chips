from __future__ import division

"""VHDL generation of the SerialIn primitive"""

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
    name = stream.name
    bits = stream.get_bits()
    clock_divider = stream.clock_rate/(stream.baud_rate * 16)

    ports = [
"    {0} : in std_logic".format(name),
    ]

    declarations = [
"  signal STATE_{0}           : SERIAL_IN_STATE_TYPE;".format(identifier),
"  signal STREAM_{0}          : std_logic_vector(7 downto 0);".format(identifier),
"  signal STREAM_{0}_STB      : std_logic;".format(identifier),
"  signal STREAM_{0}_ACK      : std_logic;".format(identifier),
"  signal COUNT_{0}           : integer Range 0 to 3;".format(identifier),
"  signal BIT_SPACING_{0}     : integer Range 0 to 15;".format(identifier),
"  signal INT_SERIAL_{0}      : std_logic;".format(identifier),
"  signal SERIAL_DEGLITCH_{0} : std_logic_Vector(1 downto 0);".format(identifier),
"  constant CLOCK_DIVIDER_{0} : unsigned(11 downto 0) := To_unsigned({1}, 12);".format(identifier, int(round(clock_divider-1))),
"  signal BAUD_COUNT_{0}      : unsigned(11 downto 0);".format(identifier),
"  signal X16CLK_EN_{0}       : std_logic;".format(identifier),

    ]


    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --serial input port baud rate generator",
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
"  --synchronise and filter",
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    SERIAL_DEGLITCH_{0} <= SERIAL_DEGLITCH_{0}(0) & {1};".format(identifier, name),
"    if X16CLK_EN_{0} = '1' then".format(identifier),
"      if SERIAL_DEGLITCH_{0}(1) = '1' then".format(identifier),
"        if COUNT_{0} = 3 then".format(identifier),
"          INT_SERIAL_{0} <= '1';".format(identifier),
"        else ",
"          COUNT_{0} <= COUNT_{0} + 1;".format(identifier),
"        end if;",
"      else",
"        if COUNT_{0} = 0 then".format(identifier),
"          INT_SERIAL_{0} <= '0';".format(identifier),
"        else",
"          COUNT_{0} <= COUNT_{0} - 1;".format(identifier),
"        end if;",
"      end if;",
"    end if;",
"  end process;",
"",  
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"	 if X16CLK_EN_{0} = '1' then ".format(identifier),
"      if BIT_SPACING_{0} = 15 then".format(identifier),
"        BIT_SPACING_{0} <= 0;".format(identifier),
"      else",
"        BIT_SPACING_{0} <= BIT_SPACING_{0} + 1;".format(identifier),
"      end if;",
"    end if;",
"    case STATE_{0} is".format(identifier),
"      when IDLE =>",
"        BIT_SPACING_{0} <= 0;".format(identifier),
"        if X16CLK_EN_{0} = '1' and INT_SERIAL_{0} = '0' then".format(identifier),
"          STATE_{0} <= START;".format(identifier),
"        end if;",
"      when START =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 7 then".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX0;".format(identifier),
"        end if; ",
"      when RX0 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(0) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX1;".format(identifier),
"        end if;",
"      when RX1 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(1) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX2;".format(identifier),
"        end if;",
"      when RX2 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(2) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX3;".format(identifier),
"        end if;",
"      when RX3 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(3) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX4;".format(identifier),
"        end if;",
"      when RX4 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(4) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX5;".format(identifier),
"        end if;",
"      when RX5 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(5) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX6;".format(identifier),
"        end if;",
"      when RX6 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(6) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= RX7;".format(identifier),
"        end if;",
"      when RX7 =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"          STREAM_{0}(7) <= INT_SERIAL_{0};".format(identifier),
"          BIT_SPACING_{0} <= 0;".format(identifier),
"          STATE_{0} <= STOP;".format(identifier),
"        end if;",
"      when STOP =>",
"        if X16CLK_EN_{0} = '1' and BIT_SPACING_{0} = 15 then".format(identifier),
"            BIT_SPACING_{0} <= 0;".format(identifier),
"            STATE_{0} <= OUTPUT_DATA;".format(identifier),
"        end if;",
"      when OUTPUT_DATA =>",
"          STREAM_{0}_STB <= '1';".format(identifier),
"          if STREAM_{0}_ACK = '1' then".format(identifier),
"            STREAM_{0}_STB <= '0';".format(identifier),
"            STATE_{0} <= IDLE;".format(identifier),
"          end if;",
"      when others =>",
"        STATE_{0} <= IDLE;".format(identifier),
"    end case;",
"    if RST = '1' then",
"      STATE_{0} <= IDLE;".format(identifier),
"      STREAM_{0}_STB <= '0';".format(identifier),
"    end if; ",
"  end process;",
"",
    ]

    return ports, declarations, definitions
