#!/usr/bin/env python

from streams import *
import streams_VHDL


def string_stream(system, x):
    string_process = system.process(8)
    output_stream = string_process.outstream()
    variables = [string_process.variable(ord(i)) for i in x]
    string_process.procedure(
            *[output_stream.write(i) for i in variables]
    )
    return output_stream

system = System()
system.printer(string_stream(system, "hello world"))

print system

#ghdl simulation
simulation_plugin = streams_VHDL.Plugin()

system.write_code(simulation_plugin)
simulation_plugin.ghdl_sim(execute=True, stop_cycles=10000, generate_wave=True)

#xilinx synthesise
#synthesis_plugin = streams_VHDL.Plugin(internal_clock = False, internal_reset = False)

#system.write_code(synthesis_plugin)
#synthesis_plugin.xilinx_build(part="xc3s200-4-ft256")
