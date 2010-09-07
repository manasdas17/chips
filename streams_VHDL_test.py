#!/usr/bin/env python

from streams import *
import streams_VHDL 


#Test Binary +
a, b, z = [], [], []
for i in range(0, 16):
    for j in range(0, 16):
        a.append(i)
        b.append(j)
        z.append((i+j)%32)
print a
print b
print z

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(5, *z)
model = Asserter(expected_response == stimulus_a + stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_sim(execute=True, stop_cycles=1000, generate_wave=True)
