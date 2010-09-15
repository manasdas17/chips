#!/usr/bin/env python

from streams import *
import streams_VHDL 
stop_on_fail = True

#Test Clone 
x = Clone(Sequence(9, *range(0, 256)))
model = Asserter(x.spawn()==x.spawn())

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = simulation_plugin.ghdl_test("clone test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Switch 
model = Asserter(Sequence(8,0,1,2) == Switch(Counter(0, 2, 1), Repeater(0), Repeater(1), Repeater(2)))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("switch test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Spinner
model = Asserter(Sequence(8,0,1,2) == Spinner(Repeater(0), Repeater(1), Repeater(2)))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("spinner test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Stepper
model = Asserter(Repeater(8) == Stepper(Repeater(8), Repeater(9), Repeater(1)))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("stepper test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Flow Control 1
#Check that Step() propogates through Spinner()
#Check that Step() increments Stepper()
flow = Stepper(
        Spinner(
            Repeater(0),
            Repeater(1),
            Step(),
        ),
        Spinner(
            Repeater(2),
            Repeater(3),
            Step(),
        )
)

model = Asserter(Sequence(8, 0, 1, 2, 3) == flow)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("flow control 1 ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Flow Control 2
#Check that Step() does not propogate through Stepper()
flow = Stepper(
            Stepper(Step(), Repeater(5)),
            Repeater(10),
)

model = Asserter(Repeater(5) == flow)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("flow control 2 ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Flow Control 3
#Check that Step() does not propogate through Stepper()
flow = Spinner(
            Spinner(Skip(), Skip(), Skip(), Repeater(5)),
            Spinner(Skip(), Skip(), Skip(), Repeater(10)),
)

model = Asserter(Sequence(8, 5, 10) == flow)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("flow control 3 ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Flow Control 4
#Check that a step_if function can be constructed from primitives
def step_if(predicate):
    return Switch(predicate, Skip(), Step())

flow = Stepper(
            Spinner(Repeater(5), step_if(Counter(1, 5, 1) == Repeater(5))),
            Spinner(Repeater(1), Step()),
)

model = Asserter(Sequence(8, 5, 5, 5, 5, 5, 1) == flow)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("flow control 4 ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary + test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary - test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary *
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append((i*j)%256)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(4, *b)
expected_response = Sequence(8, *z)
model = Asserter(expected_response == stimulus_a * stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary * test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(int((1.0*i)/(1.0*j))%32)

stimulus_a =        Sequence(4, *a)
stimulus_b =        Sequence(5, *b)
expected_response = Sequence(5, *z)
model = Asserter(expected_response == stimulus_a // stimulus_b)

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("binary // test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary & test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary | test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary ^ test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary << test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary >> test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary == test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary != test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary >= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary <= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary > test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

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
good = good and simulation_plugin.ghdl_test("binary < test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formater
model = Asserter(Formater(Repeater(10))==Sequence(8, 49, 48))

simulation_plugin = streams_VHDL.Plugin()
model.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("formater test ", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

