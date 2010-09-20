#!/usr/bin/env python
"""VHDL generation of processes"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import common

def write_process(process, plugin):

    plugin.definitions.extend([
"  process",
"  begin",
"    wait until rising_edge(CLK);",
"    case STATE_{0} is".format(process.get_identifier()),
    ])

    ideclarations = []
    for i in process.instructions:
        idec, idef = i.write_code(plugin)
        plugin.definitions.extend(idef)
        ideclarations.extend(idec)

    plugin.definitions.extend([
"    end case;",
"    if RST = '1' then",
"      STATE_{0} <= INSTRUCTION_{1};".format(process.get_identifier(), process.instructions[0].get_identifier()),
    ])
    for i in process.outstreams:
        plugin.definitions.extend([
"      STREAM_{0}_STB <= '0';".format(i.get_identifier()),
        ])
    for i in process.instructions:
        if hasattr(i, 'instream'):
            plugin.definitions.extend([
"      STREAM_{0}_ACK <= '0';".format(i.instream.get_identifier()),
            ])
    for i in process.variables:
        plugin.definitions.extend([
"      VARIABLE_{0} <= {1};".format(i.get_identifier(), common.binary(i.initial, i.get_bits())),
        ])
    plugin.definitions.extend([
"    end if;",
"  end process;",
    ])

    plugin.declarations.extend([
"  TYPE PROCESS_{0}_STATE_TYPE is ({1});".format(process.get_identifier(), ', '.join(ideclarations)),
"  signal STATE_{0} : PROCESS_{0}_STATE_TYPE;".format(process.get_identifier())
    ])
    for i in process.outstreams:
        plugin.declarations.extend([
"  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(i.get_identifier(), i.get_bits()-1),
"  signal STREAM_{0}_STB : std_logic;".format(i.get_identifier()),
"  signal STREAM_{0}_ACK : std_logic;".format(i.get_identifier()),
        ])
    for i in process.variables:
        plugin.declarations.extend([
"  signal VARIABLE_{0}   : std_logic_vector({1} downto 0);".format(i.get_identifier(), i.get_bits()-1),
        ])


