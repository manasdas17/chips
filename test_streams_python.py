#!/usr/bin/env python

from streams import *
import streams_python
stop_on_fail = True

def sequence(*args):
    return Lookup(Counter(0, len(args)-1, 1), *args)

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
s=System(( Asserter(expected_response == z),))

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = simulation_plugin.python_test("integer + test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer - test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer * test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(int((1.0*i)/(1.0*j)))

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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer // test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer & test ", stop_cycles=1000)
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
s=System( ( Asserter(expected_response == z),))

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer | test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer ^ test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer << test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer >> test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer == test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer != test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer >= test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer <= test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer > test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("integer < test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("chain test ", stop_cycles=1000)
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
s=System(( Asserter(expected_response==stimulus_a+stimulus_b),))

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams + test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams - test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams * test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Binary //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(int((1.0*i)/(1.0*j)))

stimulus_a =        sequence(*a)
stimulus_b =        sequence(*b)
expected_response = sequence(*z)
s=System((Asserter(expected_response == stimulus_a // stimulus_b),))

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams // test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams & test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams | test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams ^ test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams << test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams >> test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams == test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams != test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams >= test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams <= test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams > test ", stop_cycles=1000)
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

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("streams < test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Formater
s=System((Asserter(Formater(Repeater(10))==sequence(49, 48)),))

simulation_plugin = streams_python.Plugin()
s.write_code(simulation_plugin)
good = good and simulation_plugin.python_test("formater test ", stop_cycles=2000)
if not good and stop_on_fail: exit()
print "All Tests PASS"
