#!/usr/bin/env python

from streams import *
import streams_VHDL 


#Test Binary +
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i+j)%32)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(5, *z)
model = Asserter(expected_response == stimulus_a + stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary + test ", stop_cycles=1000, generate_wave=True)

#Test Binary -
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i-j)%32)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(5, *z)
model = Asserter(expected_response == stimulus_a - stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary - test ", stop_cycles=1000, generate_wave=True)

#Test Binary &
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i&j)%16)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(4, *z)
model = Asserter(expected_response == stimulus_a & stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary & test ", stop_cycles=1000, generate_wave=True)

#Test Binary |
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i|j)%16)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(4, *z)
model = Asserter(expected_response == stimulus_a | stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary | test ", stop_cycles=1000, generate_wave=True)

#Test Binary ^
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i^j)%16)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(4, *z)
model = Asserter(expected_response == stimulus_a ^ stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary ^ test ", stop_cycles=1000, generate_wave=True)

#Test Binary <<
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append((i<<j)%16)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(4, *z)
model = Asserter(expected_response == (stimulus_a << stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary << test ", stop_cycles=1000, generate_wave=True)

#Test Binary >>
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append((i>>j)%16)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(4, *z)
model = Asserter(expected_response == (stimulus_a >> stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary >> test ", stop_cycles=1000, generate_wave=True)

#Test Binary ==
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i==j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a == stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary == test ", stop_cycles=1000, generate_wave=True)

#Test Binary !=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i!=j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a != stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary != test ", stop_cycles=1000, generate_wave=True)

#Test Binary >=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i>=j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a >= stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary >= test ", stop_cycles=1000, generate_wave=True)

#Test Binary <=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i<=j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a <= stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary <= test ", stop_cycles=1000, generate_wave=True)

#Test Binary >
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i>j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a > stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary > test ", stop_cycles=1000, generate_wave=True)

#Test Binary <
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(int(i<j))

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(1, *z)
model = Asserter(expected_response == (stimulus_a < stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("binary < test ", stop_cycles=1000, generate_wave=True)

#Test Clone 
x = Clone(Sequence(9, *range(0, 256)))
model = Asserter(x.spawn()==x.spawn())

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("clone test ", stop_cycles=2000, generate_wave=True)

#Test Switch 
model = Asserter(Sequence(8,0,1,2) == Switch(Counter(0, 2, 1), Repeater(0), Repeater(1), Repeater(2)))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("switch test ", stop_cycles=2000, generate_wave=True)
