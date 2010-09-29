#!/usr/bin/env python

from streams import *
import streams_VHDL 
stop_on_fail = True

def sequence(system, *args):
    return Lookup(system.counter(0, len(args)-1, 1), *args)

#Test Process
system = System()

a = Variable(15)
outstream = Output()

process = system.process(
    outputs = (outstream,),
    variables = (a,),
    instructions = (
        Instruction("OP_IMM", 10, immediate=10),
        Instruction("OP_WRITE_1", 10),
        Instruction("OP_JMP", immediate = 0),
        Instruction("OP_JMP", immediate = 2),
    )
)

system.printer(outstream)

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = plugin.ghdl_test("process_test", stop_cycles=2000, generate_wave=True)
exit()

#Test Process
system = System()

instream = system.repeater(15)
outstream = Output()
a = Variable(20)

process = system.process(
    inputs = (instream,),
    outputs = (outstream,),
    variables = (a,),
    instructions = (
        instream.read(a),
        outstream.write(a)
    )
)
system.asserter(outstream == system.repeater(15))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()

feedback = Output()
count = Output()
a = Variable(0)
i = (feedback + system.repeater(1))
process = system.process(
    inputs = (i,),
    outputs = (count, feedback),
    variables = (a,),
    instructions = (
        feedback.write(a),
        count.write(a),
        i.read(a),
    )
)
system.asserter(count == system.counter(0, 10, 1))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 3", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()
count = system.counter(0, 10, 1)

output = Output()
a = Variable(0)
b = Variable(0)

process = system.process(
    bits = 8,
    inputs = (count,),
    outputs = (output,),
    variables = (
        a,
        b
    ),
    instructions = (
        Loop(
            count.read(a),
            b.set(a),
            output.write(b)
        ),
    )
)
system.asserter(output == system.counter(0, 10, 1))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 4", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Process
system = System()
count = system.counter(0, 10, 1)

output = Output()
a = Variable(0)
b = Variable(0)

process = system.process(
    bits = 8,

    inputs = (count,),

    outputs = (output,),

    variables = (
        a,
        b
    ),

    instructions = (
        Loop(
            count.read(a),
            b.set(a),
            output.write(b),
            Break(),
        ),
        Loop(
            count.read(a),
            b.set(a),
            output.write(b)
        ),
    )
)
system.asserter(output == system.counter(0, 10, 1))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("process test 5", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test If 1
system = System()
output = Output()
a = Variable(0)
b = Variable(0)

process = system.process(
    bits = 8,

    outputs = (output,),

    variables = (
        a,
        b,
    ),

    instructions = (
        Loop(
            If( (Constant(0),),
                output.write(a),
            ),
        ),
    ),
)
system.asserter(output == system.repeater(0))

plugin = streams_VHDL.Plugin()
system.write_code(plugin)
good = good and plugin.ghdl_test("if test 1", stop_cycles=2000, generate_wave=True)
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

