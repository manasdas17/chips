#!/usr/bin/env python

from streams import *
import streams_VHDL 
stop_on_fail = True

def sequence(system, *args):
    return Lookup(system.counter(0, len(args)-1, 1), *args)

#Test Process
system = System()

process = system.process(8)
outstream = process.outstream()
a = process.variable(15)
process.procedure(
    outstream.write(a)
)
system.asserter(outstream == system.repeater(15))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = plugin.ghdl_test("process test 1", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()

process = system.process(8)
instream = system.repeater(15)
outstream = process.outstream()
a = process.variable(20)
process.procedure(
    instream.read(a),
    outstream.write(a)
)
system.asserter(outstream == system.repeater(15))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()

process = system.process(8)
feedback = process.outstream()
count = process.outstream()
a = process.variable(0)
process.procedure(
    feedback.write(a),
    count.write(a),
    (feedback + system.repeater(1)).read(a),
)
system.asserter(count == system.counter(0, 10, 1))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 3", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()

process = system.process(8)
output = process.outstream()
count = system.counter(0, 10, 1)
a = process.variable(0)
b = process.variable(0)
process.procedure(
        count.read(a),
        b.set(a),
        output.write(b)
)
system.asserter(output == system.counter(0, 10, 1))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 4", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()
exit()

#Test Clone 
s = System()
x = Clone(sequence(s, *range(0, 128)))
s.asserter(x.spawn()==x.spawn())

plugin = streams_VHDL.Plugin()
s.write_code(plugin)

good = good and plugin.ghdl_test("clone test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Switch 
s = System()
s.asserter(sequence(s,0,1,2) == Switch(s.counter(0, 2, 1), s.repeater(0), s.repeater(1), s.repeater(2)))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("switch test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary +
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i+j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a + stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary + test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary -
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i-j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a - stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary - test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary *
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i*j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a * stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary * test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(int((1.0*i)/(1.0*j)))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a // stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary // test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary &
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i&j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a & stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary & test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary |
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i|j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a | stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary | test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary ^
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i^j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == stimulus_a ^ stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary ^ test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <<
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i<<j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a << stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary << test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >>
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i>>j)

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a >> stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary >> test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary ==
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i==j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a == stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary == test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary !=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i!=j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a != stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary != test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>=j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a >= stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary >= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<=j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a <= stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary <= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a > stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary > test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<j))

s = System()
stimulus_a =        sequence(s, *a)
stimulus_b =        sequence(s, *b)
expected_response = sequence(s, *z)
s.asserter(expected_response == (stimulus_a < stimulus_b))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary < test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formater
s = System()
s.asserter(Formater(s.repeater(10))==sequence(s, 49, 48))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("formater test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

