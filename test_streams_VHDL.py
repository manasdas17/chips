#!/usr/bin/env python

from streams import *
import streams_VHDL 
stop_on_fail = True

def sequence(*args):
    return Lookup(Counter(0, len(args)-1, 1), *args)

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

#test_feedback
lookup = Output()
lookedup = Lookup(lookup, 0, 1, 2, 3)

#create a process to calculate coordinates
RightAssensions = Sequence()
Declinations = Sequence()

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
            Asserter(outstream==sequence(0, 1, 2, 3)),
        )
)

#simulate in VHDL
import streams_VHDL
simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
simulation_plugin.ghdl_test("feedback test ", stop_cycles=10000, generate_wave=True)

#Test Evaluate
a = range(-8, 8)
z = [i>0 for i in a]
stimulus_a =        sequence(*a)
expected_response = sequence(*z)

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
good = simulation_plugin.ghdl_test("evaluate test", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Integer +
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-8, 8):
        a.append(i)
        b.append(j)
        z.append(i+j)

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)

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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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
expected_response = sequence(0, 1, 2, 3, 4, 5, 6)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
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

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
s=System((Asserter(expected_response == (stimulus_a < stimulus_b)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("streams < test ", stop_cycles=1000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(DecimalFormatter(Repeater(10))==sequence(49, 48)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 1", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

s=System((Asserter(DecimalFormatter(Repeater(100))==sequence(49, 48, 48)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

s=System((Asserter(DecimalFormatter(Repeater(-128))==sequence(45, 49, 50, 56)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("decimal formatter test 3", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(HexFormatter(Repeater(10))==sequence(48, 120, 97)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("hex formatter test 1", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

#Test Formatter
s=System((Asserter(HexFormatter(Repeater(-128))==sequence(45, 48, 120, 56, 48)),))

simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.ghdl_test("hex formatter test 2", stop_cycles=2000, generate_wave=True)
if not good and stop_on_fail: exit()

print "All Tests PASS"
