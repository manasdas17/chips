"""VHDL generation of the Array Primitive"""

import common

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


def write(plugin, stream):

    identifier = stream.get_identifier()
    bits = stream.get_bits()
    depth = stream.depth
    identifier_a = stream.a.get_identifier()
    if hasattr(plugin, "has_fifo"):
        one_offs = False
    else:
        plugin.has_fifo=True
        one_offs = True

    dependencies = [
"--  ****************************************************************************",
"--  Filename         :fifo.vhd",
"--  Project          :library",
"--  Version          :0.1",
"--  Author           :Jonathan P Dawson",
"--  Created Date     :2007-06-20",
"--  ****************************************************************************",
"--  Description      :Generic FIFO",
"--  ****************************************************************************",
"--  Dependencies     :Standard Libraries",
"--  ****************************************************************************",
"--  Revision History :",
"--",
"--  Date :2007-06-20",
"--  Author :Jonathan P Dawson",
"--  Modification: Created File",
"--",
"--  ****************************************************************************",
"--  Copyright (C) Jonathan P Dawson 2007",
"--  ****************************************************************************",
"library ieee;",
"use ieee.std_logic_1164.all;",
"use ieee.numeric_std.all;",
"",
"entity FIFO is",
"    generic(",
"        DEPTH : integer;",
"        WIDTH : integer",
"    );",
"    port(",
"        CLK        : in std_logic;",
"        RST        : in std_logic;",
"        DATA_I     : in std_logic_vector(WIDTH - 1 downto 0);",
"        DATA_I_STB : in std_logic;",
"        DATA_I_ACK : out std_logic;",
"        DATA_O     : out std_logic_vector(WIDTH - 1 downto 0);",
"        DATA_O_STB : out std_logic;",
"        DATA_O_ACK : in std_logic",
"    );",
"end entity FIFO;",
"",
"architecture RTL of FIFO is",
"",
"    type MEMORY_TYPE is array (0 to DEPTH - 1) of std_logic_vector(WIDTH - 1 downto 0);",
"    signal MEMORY : MEMORY_TYPE;",
"",
"    signal FILL : integer range 0 to DEPTH;",
"    signal INPOINTER, OUTPOINTER : integer range 0 to DEPTH -1;",
"    signal FULL, EMPTY : std_logic;",
"    signal WRITE, READ : std_logic;",
"",
"begin",
"",
"  EMPTY <= '1' when",
"    FILL = 0 else",
"      '0';",
"",
"  FULL <= '1' when",
"    FILL = DEPTH else",
"      '0';",
"",
"  WRITE <= '1' when",
"    DATA_I_STB = '1' and FULL = '0' else",
"     '0';",
"",
"  READ <= '1' when ",
"    DATA_O_ACK = '1' else",
"     '0';",
"",
"",
"  ACCESS_MEMORY : process(CLK)",
"  begin",
"    if rising_edge(CLK) then",
"      if WRITE = '1' then",
"        MEMORY(INPOINTER) <= DATA_I;",
"      end if;",
"      DATA_O <= MEMORY(OUTPOINTER);",
"    end if;",
"  end process ACCESS_MEMORY;",
"",
"  FIFO_CONTROL : process",
"  begin",
"",
"    wait until rising_edge(CLK);",
"",
"    DATA_I_ACK <= '0';",
"    if WRITE = '1' then",
"      if INPOINTER = DEPTH - 1 then",
"        INPOINTER <= 0;",
"      else",
"        INPOINTER <= INPOINTER + 1;",
"      end if;",
"      DATA_I_ACK <= '1';",
"    end if;",
"",
"    if EMPTY = '0' then",
"      DATA_O_STB <= '1';",
"    end if;",
"",
"    if READ = '1' then",
"      if OUTPOINTER = DEPTH - 1 then",
"        OUTPOINTER <= 0;",
"      else",
"        OUTPOINTER <= OUTPOINTER + 1;",
"      end if;",
"      --The memory will take a clock cycle to read the new data",
"      --so disable the strobe for now.",
"      DATA_O_STB <= '0';",
"    end if;",
"",
"    if WRITE = '1' and READ = '0' then",
"      FILL <= FILL + 1;",
"    elsif READ = '1' and WRITE = '0' then",
"      FILL <= FILL - 1;",
"    end if;",
"",
"    if RST = '1' then",
"      INPOINTER <= 0;",
"      OUTPOINTER <= 0;",
"      FILL <= 0;",
"      DATA_O_STB <= '0';",
"    end if;",
"  end process FIFO_CONTROL;",
"",
"end architecture RTL;",
"",
    ]
    if not one_offs: dependencies = []

    ports = []

    if one_offs:
        declarations = [
"  component FIFO is",
"    generic (",
"      width      : integer := 8;",
"      depth      : integer := 16",
"    );",
"    port (",
"      RST        : in  Std_logic;",
"      CLK        : in  Std_logic;",
"      DATA_I     : in  Std_logic_vector(width - 1 downto 0);",
"      DATA_I_STB : in  Std_logic;",
"      DATA_I_ACK : out Std_logic;",
"      DATA_O     : out Std_logic_vector(width - 1 downto 0);",
"      DATA_O_STB : out Std_logic;",
"      DATA_O_ACK : in  Std_logic",
"    );",
"  end component FIFO;",
"",
"  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
"  signal STREAM_{0}_STB : std_logic;".format(identifier),
"  signal STREAM_{0}_ACK : std_logic;".format(identifier),
"",
        ]
    else:
        declarations = [
"  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
"  signal STREAM_{0}_STB : std_logic;".format(identifier),
"  signal STREAM_{0}_ACK : std_logic;".format(identifier),
"",
        ]


    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --STREAM {0} Array()".format(identifier),
"  FIFO_{0} : FIFO generic map(".format(identifier),
"      DEPTH => {0},".format(depth),
"      WIDTH => {0}".format(bits),
"  )",
"  port map(",
"      CLK           => CLK,",
"      RST           => RST,",
"      DATA_I        => STREAM_{0},".format(identifier_a),
"      DATA_I_STB    => STREAM_{0}_STB,".format(identifier_a),
"      DATA_I_ACK    => STREAM_{0}_ACK,".format(identifier_a),
"      DATA_O        => STREAM_{0},".format(identifier),
"      DATA_O_STB    => STREAM_{0}_STB,".format(identifier),
"      DATA_O_ACK    => STREAM_{0}_ACK".format(identifier),
"    );",
"",
    ]

    return dependencies, ports, declarations, definitions
