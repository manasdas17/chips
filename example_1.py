#!/usr/bin/env python
"""Example 1 Hello World .... in welsh!"""

import sys

from streams import * #use the streams library
import streams_VHDL #import VHDL plugin 


################################################################################
##make a simulation model that prints to stdout

system = System(
        AsciiPrinter(
            Sequence(*tuple((ord(i) for i in "helo byd!\n"))+(0,)),
        )
    )

if "simulate" in sys.argv:
    #write the system to the code generator plugin
    system.test("Example 1: Hello World .... in welsh!", stop_cycles=100)

if "simulate_vhdl" in sys.argv:
    #simulate using an external vhdl simulator
    vhdl_plugin = streams_VHDL.Plugin()
    system.write_code(vhdl_plugin)
    vhdl_plugin.ghdl_test("Example 1 : Hello world .... in welsh!", stop_cycles=2000)
