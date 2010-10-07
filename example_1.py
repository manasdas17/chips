#!/usr/bin/env python

#the streams library provides the streams design constructs
#when using the streams library it is best to use from streams import *
from streams import *

#the streams_VHDL library provides the VHDL code generation plugin
import streams_VHDL

#Example 1 outputing a stream of numbers

#create a system
out=Output()

Process(8,
    Loop(
        out.write(2),
        out.write(3),
        Break(),
    )
)

system = System(
    sinks = (Printer(out),),
)

#create a code generator plugin
vhdl_plugin = streams_VHDL.Plugin()

#write the system to the code generator plugin
system.write_code(vhdl_plugin)

#simulate using an external vhdl simulator
vhdl_plugin.ghdl_test("Example 1 : Hello world ... part I", stop_cycles=2000, generate_wave=True)
