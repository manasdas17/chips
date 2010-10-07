#!/usr/bin/env python

"""Example, echo charaters with a uart"""
from streams import *
import streams_VHDL

system = System(
    (
        SerialOut(SerialIn()),
    ) 
)

#create a code generator plugin
vhdl_plugin = streams_VHDL.Plugin()

#write the system to the code generator plugin
system.write_code(vhdl_plugin)

#simulate using an external vhdl simulator
vhdl_plugin.ghdl_test("Example 3 : Serial UART echo", stop_cycles=2000, generate_wave=True)
