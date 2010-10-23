#!/usr/bin/env python

from streams import *
import streams_VHDL 
stop_on_fail = True

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

#test sizing
out = Output()
a = Variable(127)
b = Variable(1)
Process(8,
    out.write(a+b),
)
system = System((Asserter(out==0),))

p = streams_VHDL.Plugin()
system.write_code(p)
good = p.ghdl_test("test sizing", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#test stimulus
a = Stimulus(8)
a = Stimulus(8)

s=System(
        sinks=(
            Asserter(a==Sequence(*range(100))),
        )
)


simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
a.set_simulation_data(range(100), simulation_plugin)
good = good and simulation_plugin.ghdl_test("stimulus test ", stop_cycles=200, generate_wave=True)
if not good and stop_on_fail: exit()

#test response
a = Response(Sequence(*range(100)))

s=System(
        sinks=(
           a,
        )
)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = simulation_plugin.ghdl_test("response test ", stop_cycles=10000, generate_wave=True)
for response, expected in zip(a.get_simulation_data(simulation_plugin), range(100)):
    good = good and response==expected
    if not good:
        print "Failed to retireve simulation data"

if not good and stop_on_fail: exit()

#test_feedback
lookup = Output()
lookedup = Lookup(lookup, 0, 1, 2, 3)
x = Variable(0)
outstream = Output()

Process(10, #gives integer range -512 to 512
    Loop(
       lookup.write(0),
       lookedup.read(x),
       outstream.write(x),
       lookup.write(1),
       lookedup.read(x),
       outstream.write(x),
       lookup.write(2),
       lookedup.read(x),
       outstream.write(x),
       lookup.write(3),
       lookedup.read(x),
       outstream.write(x),
    )
)

#Join the elements together into a system
s=System(
        sinks=(
            Asserter(outstream==Sequence(0, 1, 2, 3)),
        )
)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("feedback test ", stop_cycles=10000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Evaluate
a = range(-8, 8)
z = [i>0 for i in a]
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, 
    Loop(
        stimulus_a.read(a),
        z.write(
            Evaluate(
                If(a>0, 
                    Value(1),
                ).ElsIf(1,
                    Value(0),
                )
            )
        )
    )
)

s=System(( Asserter(expected_response == z),))
simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("evaluate test", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer +
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i+j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a+b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer + test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer -
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i-j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a-b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer - test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer *
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i*j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a*b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer * test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_division(i, j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a//b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer // test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer %
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_modulo(i, j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a%b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer % test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer &
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i&j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a&b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer & test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer |
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i|j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a|b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer | test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer ^
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i^j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a^b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer ^ test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer <<
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i<<j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(16, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a<<b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer << test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer >>
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i>>j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a>>b)
))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer >> test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer ==
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i==j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a==b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer == test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer !=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i!=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a!=b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer != test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer >=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a>=b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer >= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer <=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)

a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a<=b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer <= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer >
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a>b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer > test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer <
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
a = Variable(0)
b = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    stimulus_b.read(b),
    z.write(a<b)
    ))
s=System((Asserter(expected_response == z),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("integer < test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Chain
expected_response = Sequence(0, 1, 2, 3, 4, 5, 6)
z = Output()
Process(8, 
    Loop(
        z.write(0),
        z.write(1),
        z.write(2),
        z.write(3),
        z.write(4),
        z.write(5),
        z.write(6),
    )
)
s=System(
    (
        Asserter( expected_response == z),
        #Printer(z),
    )
)

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("chain test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary +
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i+j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a + stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = simulation_plugin.ghdl_test("streams + test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary -
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i-j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a - stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams - test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary *
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i*j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a * stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams * test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_division(i, j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a // stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams // test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary %
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_modulo(i, j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a % stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams % test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary &
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i&j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a & stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams & test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary |
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i|j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a | stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams | test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary ^
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i^j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == stimulus_a ^ stimulus_b),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams ^ test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <<
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i<<j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a << stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams << test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >>
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(i>>j)

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a >> stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams >> test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary ==
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i==j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a == stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams == test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary !=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i!=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a != stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams != test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a >= stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams >= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <=
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<=j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a <= stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams <= test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary >
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i>j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a > stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams > test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Binary <
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(-int(i<j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=System((Asserter(expected_response == (stimulus_a < stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams < test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(DecimalFormatter(Repeater(10))==Sequence(ord('1'), ord('0'))),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 1", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

s=System((Asserter(DecimalFormatter(Repeater(100))==Sequence(49, 48, 48)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

s=System((Asserter(DecimalFormatter(Repeater(-128))==Sequence(45, 49, 50, 56)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 3", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(HexFormatter(Repeater(10))==Sequence(48, 120, 97)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("hex formatter test 1", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(HexFormatter(Repeater(-128))==Sequence(45, 48, 120, 56, 48)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("hex formatter test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

print "All Tests PASS"
