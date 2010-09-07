#!/usr/bin/env python

from streams import *
import streams_VHDL

a = Rotate(Repeater(1), Repeater(2))

simulation_model = Printer(a)
synthesis_model = OutPort("my_output", a)

simulation_plugin = streams_VHDL.Plugin()
simulation_model.write_code(simulation_plugin)
simulation_plugin.ghdl_sim(execute=True, stop_cycles=1000, generate_wave=True)

#synthesis_plugin = streams_VHDL.Plugin(internal_clock = False, internal_reset = False)
#synthesis_model.write_code(synthesis_plugin)
#synthesis_plugin.xilinx_build()


#plugin.ghdl_sim(execute=True, stop_cycles=10000)
#plugin.ghdl_sim()
