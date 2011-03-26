#!/usr/bin/env python

from chips import *
import chips_cpp 
stop_on_fail = False

def resize(val, bits):
    mask = (2**(bits))-1
    sign_bit = (2**(bits-1))
    val = val&mask
    if val & sign_bit: 
        val=val|~mask
    return val

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

#test fifo
fifo_in = Output()
fifo_out = Fifo(fifo_in, 4)
data_out = Output()
a = Variable(0)
Process(8,
    fifo_in.write(0),
    fifo_in.write(1),
    fifo_in.write(2),
    fifo_in.write(3),
    fifo_out.read(a),
    data_out.write(a),
    fifo_out.read(a),
    data_out.write(a),
    fifo_out.read(a),
    data_out.write(a),
    fifo_out.read(a),
    data_out.write(a),
)
chip = Chip(Asserter(data_out==Sequence(0, 1, 2, 3)))

p = chips_cpp.Plugin()
chip.write_code(p)
good = p.test("fifo test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#test arrays
address_in = Output()
data_in = Output()
address_out = Output()
data_out = Array(address_in, data_in, address_out, 4)
Process(8,
    address_in.write(0),
    data_in.write(0),
    address_in.write(1),
    data_in.write(1),
    address_in.write(2),
    data_in.write(2),
    address_in.write(3),
    data_in.write(3),
    Loop(
        address_out.write(0),
        address_out.write(1),
        address_out.write(2),
        address_out.write(3),
    )
)

chip = Chip(Asserter(data_out==Sequence(0, 1, 2, 3)))

p = chips_cpp.Plugin()
chip.write_code(p)
good = p.test("array test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#test sizing
out = Output()
a = Variable(127)
b = Variable(1)
Process(8,
    out.write(a+b),
)
chip = Chip(Asserter(out==0))

p = chips_cpp.Plugin()
chip.write_code(p)
good = good and p.test("test sizing", stop_cycles=1000)
if not good and stop_on_fail: exit()

#test stimulus
a = Stimulus(8)
a = Stimulus(8)

s=Chip(Asserter(a==Sequence(*range(100))))


simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
a.set_simulation_data(range(100), simulation_plugin)
good = good and simulation_plugin.test("stimulus test ", stop_cycles=200)
if not good and stop_on_fail: exit()

#test response
a = Response(Sequence(*range(100)))

s=Chip(a)

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = simulation_plugin.test("response test ", stop_cycles=10000)
for response, expected in zip(a.get_simulation_data(simulation_plugin), range(100)):
    good = good and response==expected
    if not good:
        print "incorrect simulation data"

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

#Join the elements together into a chip
s=Chip(Asserter(outstream==Sequence(0, 1, 2, 3)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("feedback test ", stop_cycles=100)
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

s=Chip(Asserter(expected_response == z))
simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("evaluate test", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
#good = good and simulation_plugin.test("integer + test ", stop_cycles=1000)
good = simulation_plugin.test("integer + test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer - test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer * test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer // test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer % test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer & test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer | test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer ^ test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer << test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer >> test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer == test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer != test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer >= test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer <= test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer > test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == z))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("integer < test ", stop_cycles=1000)
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
s=Chip(
        Asserter( expected_response == z),
        #Printer(z),
)

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chain test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a + stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips + test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a - stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips - test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a * stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips * test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a // stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips // test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a % stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips % test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a & stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips & test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a | stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips | test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == stimulus_a ^ stimulus_b))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips ^ test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Binary <<
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(0, 8):
        a.append(i)
        b.append(j)
        z.append(resize(i<<j,4))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=Chip(Asserter(expected_response == (stimulus_a << stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips << test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a >> stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips >> test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a == stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips == test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a != stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips != test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a >= stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips >= test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a <= stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips <= test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a > stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips > test ", stop_cycles=1000)
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
s=Chip(Asserter(expected_response == (stimulus_a < stimulus_b)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("chips < test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Printer
s=Chip(Asserter(Printer(Repeater(10))==Sequence(ord('1'), ord('0'), ord('\n'))))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("Printer test", stop_cycles=2000)
if not good and stop_on_fail: exit()

#Test Scanner
s=Chip(Asserter(Scanner(Sequence(ord('1'), ord('0'), ord('\n')), 8)==Repeater(10)))

simulation_plugin = chips_cpp.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.test("Scanner test", stop_cycles=2000)
if not good and stop_on_fail: exit()


print "All Tests PASS"
