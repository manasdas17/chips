#!/usr/bin/env python

"""Example, output a count to a UART"""
from streams import *
import streams_VHDL
 
serial = Output()
count = Variable(0)
Process(16,
    Loop(
        serial.write(count),
    )
)

system = System(
    (
        SerialOut(Formater(serial)),
    ) 
)

#create a code generator plugin
vhdl_plugin = streams_VHDL.Plugin()

#write the system to the code generator plugin
system.write_code(vhdl_plugin)

#simulate using an external vhdl simulator
vhdl_plugin.ghdl_test("Example 4 : Output a numeric count to the serial port", stop_cycles=2000, generate_wave=True)
