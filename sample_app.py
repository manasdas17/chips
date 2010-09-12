#!/usr/bin/env python

from streams import *
import streams_VHDL

def stringify(x):
    return Sequence(8, *[ord(i) for i in x])

model = SerialOut(SerialIn())

#ghdl simulation
simulation_plugin = streams_VHDL.Plugin()

model.write_code(simulation_plugin)
simulation_plugin.ghdl_sim(execute=True, stop_cycles=10000, generate_wave=True)

#xilinx synthesise
synthesis_plugin = streams_VHDL.Plugin(internal_clock = False, internal_reset = False)

model.write_code(synthesis_plugin)
synthesis_plugin.xilinx_build(part="xc3s200-4-ft256")
