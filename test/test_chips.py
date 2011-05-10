#!/usr/bin/env python
"""Test suite for native chips simulation."""

from chips import *
import chips.common
stop_on_fail = True

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

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

system = Chip(Asserter(data_out==Sequence(0, 1, 2, 3)))

good = system.test("fifo test 1", 100)
if not good and stop_on_fail: exit()

#test arrays
myarray = VariableArray(4)
data_out = Output()
Process(8,
    myarray.write(0, 0),
    myarray.write(1, 1),
    myarray.write(2, 2),
    myarray.write(3, 3),
    Loop(
        data_out.write(myarray.read(0)),
        data_out.write(myarray.read(1)),
        data_out.write(myarray.read(2)),
        data_out.write(myarray.read(3)),
    ),
)

system = Chip(Asserter(data_out==Sequence(0, 1, 2, 3)))

good = system.test("array test 1", 100)
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

system = Chip(Asserter(data_out==Sequence(0, 1, 2, 3)))

good = system.test("array test 2", 100)
if not good and stop_on_fail: exit()

#test sizing
out = Output()
a = Variable(127)
b = Variable(1)
Process(8,
    out.write(a+b),
)

system = Chip(Asserter(out==-128))
good = good and system.test("test sizing", 100)
if not good and stop_on_fail: exit()

#test process to process
stream = Output()
Process(8,
    stream.write(1),
    stream.write(2),
    stream.write(3),
)
result = Output()
temp = Variable(0)
Process(8,
    stream.read(temp),
    If(temp == 1,
        result.write(-1),
    ).Else(
        result.write(0),
    ),
    stream.read(temp),
    If(temp == 2,
        result.write(-1),
    ).Else(
        result.write(0),
    ),
    stream.read(temp),
    If(temp == 3,
        result.write(-1),
    ).Else(
        result.write(0),
    )
)

system = Chip(Asserter(result))
good = good and system.test("test process to process", 100)
if not good and stop_on_fail: exit()

#test available
stream = Output()
Process(8,
    stream.write(1),
    stream.write(1),
)
result = Output()
temp = Variable(0)
Process(8,
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    If(stream.available(),
        result.write(-1),
    ).Else(
        result.write(0),
    ),
    stream.read(temp),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    temp.set(stream.available()),
    If(stream.available(),
        result.write(-1),
    ).Else(
        result.write(0),
    ),
    stream.read(temp),
    If(stream.available(),
        result.write(0),
    ).Else(
        result.write(-1),
    )
)

system = Chip(Asserter(result))
good = good and system.test("test available", 100)
if not good and stop_on_fail: exit()

#test stimulus
a = Stimulus(8)
a = Stimulus(8)

s=Chip(Asserter(a==Sequence(*range(100))))

a.set_simulation_data(range(100))

good = good and s.test("stimulus test ", stop_cycles=100)
if not good and stop_on_fail: exit()

#test response
a = Response(Sequence(*range(100)))

s=Chip(a)

s.test("response test ", stop_cycles=100)
for response, expected in zip(a.get_simulation_data(), range(100)):
    good = response==expected
    if not good:
        print "Failed to retrieve simulation data"

if not good and stop_on_fail: exit()


#test_feedback
lookup = Output()
lookedup = Lookup(lookup, 0, 1, 2, 3)

#create a process to calculate coordinates
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
s=Chip(Asserter(outstream==Sequence(0, 1, 2, 3)))

#simulate in python
good = s.test("feedback test ", stop_cycles=1000)
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
                ).Elif(1,
                    Value(0),
                )
            )
        )
    )
)
s=Chip( Asserter(expected_response == z))

#simulate in python
good = good and s.test("evaluate test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer abs
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(abs(i), 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(abs(a))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer abs test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer Not
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(int(not i))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.Not())
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer Not test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer ~
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(~i)

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(~a)
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer ~ test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_left(1)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i<<1, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_left(1))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_left(1) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_left(2)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i<<2, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_left(2))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_left(2) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_left(4)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i<<4, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_left(4))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_left(4) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_left(8)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i<<8, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_left(8))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_left(8) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_right(1)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i>>1, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_right(1))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_right(1) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_right(2)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i>>2, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_right(2))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_right(2) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_right(4)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i>>4, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_right(4))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_right(4) test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Integer shift_right(8)
a, b, z = [], [], []
for i in range(-8, 8):
        a.append(i)
        z.append(resize(i>>8, 8))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)

a = Variable(0)
z = Output()
Process(8, Loop(
    stimulus_a.read(a),
    z.write(a.shift_right(8))
))
s=Chip(Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer shift_right(8) test ", stop_cycles=1000)
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
s=Chip( Asserter(expected_response == z))

#simulate in python
good = good and s.test("integer + test ", stop_cycles=1000)
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

#simulate in python
good = good and s.test("integer - test ", stop_cycles=1000)
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

good = good and s.test("integer * test ", stop_cycles=1000)
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

good = good and s.test("integer // test ", stop_cycles=1000)
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

good = good and s.test("integer % test ", stop_cycles=1000)
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

good = good and s.test("integer & test ", stop_cycles=1000)
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

good = good and s.test("integer | test ", stop_cycles=1000)
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

good = good and s.test("integer ^ test ", stop_cycles=1000)
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

good = good and s.test("integer << test ", stop_cycles=1000)
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

good = good and s.test("integer >> test ", stop_cycles=1000)
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

good = good and s.test("integer == test ", stop_cycles=1000)
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

good = good and s.test("integer != test ", stop_cycles=1000)
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

good = good and s.test("integer >= test ", stop_cycles=1000)
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

good = good and s.test("integer <= test ", stop_cycles=1000)
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

good = good and s.test("integer > test ", stop_cycles=1000)
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

good = good and s.test("integer < test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

for a in range(-8, 8):

    #Test reverse Integer +
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a+j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a+b)
    ))
    s=Chip( Asserter(expected_response == z))

    #simulate in python
    good = good and s.test("reverse integer + test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()


    #Test reverse Integer -
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a-j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a-b)
    ))
    s=Chip(Asserter(expected_response == z))

    #simulate in python
    good = good and s.test("reverse integer - test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer *
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a*j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a*b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer * test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer //
    b, z = [], []
    for j in range(-16, 0)+range(1, 16):
        b.append(j)
        z.append(c_style_division(a, j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a//b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer // test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer %
    b, z = [], []
    for j in range(-16, 0)+range(1, 16):
        b.append(j)
        z.append(c_style_modulo(a, j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a%b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer % test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer &
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a&j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a&b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer & test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer |
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a|j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a|b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer | test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer ^
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a^j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a^b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer ^ test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer <<
    b, z = [], []
    for j in range(0, 8):
        b.append(j)
        z.append(a<<j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(16, Loop(
        stimulus_b.read(b),
        z.write(a<<b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer << test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer >>
    b, z = [], []
    for j in range(0, 8):
        b.append(j)
        z.append(a>>j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a>>b)
    ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer >> test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer ==
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a!=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a!=b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer != test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer ==
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a==j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a==b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer == test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer >=
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a>=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a>=b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer >= test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer <=
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a<=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)

    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a<=b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer <= test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer >
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a>j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a>b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer > test_{0} ".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test reverse Integer <
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a<j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    b = Variable(0)
    z = Output()
    Process(8, Loop(
        stimulus_b.read(b),
        z.write(a<b)
        ))
    s=Chip(Asserter(expected_response == z))

    good = good and s.test("reverse integer < test_{0} ".format(a), stop_cycles=100)
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

good = good and s.test("chain test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary Abs
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(abs(i), 4))

stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response == (abs(stimulus_a))))

good = good and s.test("chips abs test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary Not
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(-int(not i))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.Not()))

good = good and s.test("chips not test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary ~
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(~i)
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==(~stimulus_a)))

good = good and s.test("chips ~ test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_left(1)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i<<1, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_left(1)))

good = good and s.test("chips shift_left(1) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_left(2)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i<<2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_left(2)))

good = good and s.test("chips shift_left(2) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_left(4)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i<<2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_left(2)))

good = good and s.test("chips shift_left(4) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_left(8)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i<<2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_left(2)))

good = good and s.test("chips shift_left(8) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_right(1)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i>>1, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_right(1)))

good = good and s.test("chips shift_right(1) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_right(2)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i>>2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_right(2)))

good = good and s.test("chips shift_right(2) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_right(4)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i>>2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_right(2)))

good = good and s.test("chips shift_right(4) test", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Unary shift_right(8)
a, z = [], []
for i in range(-8, 8):
    a.append(i)
    z.append(resize(i>>2, 4))
stimulus_a =        Sequence(*a)
expected_response = Sequence(*z)
s=Chip( Asserter(expected_response==stimulus_a.shift_right(2)))

good = good and s.test("chips shift_right(8) test", stop_cycles=1000)
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
s=Chip( Asserter(expected_response==stimulus_a+stimulus_b))

good = good and s.test("chips + test ", stop_cycles=1000)
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

good = good and s.test("chips - test ", stop_cycles=1000)
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

good = good and s.test("chips * test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Binary //
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_division(i,j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=Chip(Asserter(expected_response == stimulus_a // stimulus_b))

good = good and s.test("chips // test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

#Test Binary %
a, b, z = [], [], []
for i in range(-8, 8):
    for j in range(-16, 0)+range(1, 16):
        a.append(i)
        b.append(j)
        z.append(c_style_modulo(i,j))

stimulus_a =        Sequence(*a)
stimulus_b =        Sequence(*b)
expected_response = Sequence(*z)
s=Chip(Asserter(expected_response == stimulus_a % stimulus_b))

good = good and s.test("chips % test ", stop_cycles=1000)
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

good = good and s.test("chips & test ", stop_cycles=1000)
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

good = good and s.test("chips | test ", stop_cycles=1000)
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

good = good and s.test("chips ^ test ", stop_cycles=1000)
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

good = good and s.test("chips << test ", stop_cycles=1000)
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

good = good and s.test("chips >> test ", stop_cycles=1000)
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

good = good and s.test("chips == test ", stop_cycles=1000)
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

good = good and s.test("chips != test ", stop_cycles=1000)
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

good = good and s.test("chips >= test ", stop_cycles=1000)
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

good = good and s.test("chips <= test ", stop_cycles=1000)
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

good = good and s.test("chips > test ", stop_cycles=1000)
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

good = good and s.test("chips < test ", stop_cycles=1000)
if not good and stop_on_fail: exit()

for a in range(-8, 8):
    #Test Binary +
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a+j)
    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip( Asserter(expected_response==a+stimulus_b))

    good = good and s.test("chips reverse + test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary -
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a-j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a - stimulus_b))

    good = good and s.test("chips reverse - test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary *
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a*j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a * stimulus_b))

    good = good and s.test("chips reverse * test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary //
    b, z = [], []
    for j in range(-16, 0)+range(1, 16):
        b.append(j)
        z.append(c_style_division(a,j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a // stimulus_b))

    good = good and s.test("chips reverse // test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary %
    b, z = [], []
    for j in range(-16, 0)+range(1, 16):
        b.append(j)
        z.append(c_style_modulo(a,j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a % stimulus_b))

    good = good and s.test("chips reverse % test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary &
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a&j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a & stimulus_b))

    good = good and s.test("chips reverse & test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary |
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a|j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a | stimulus_b))

    good = good and s.test("chips reverse | test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary ^
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(a^j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == a ^ stimulus_b))

    good = good and s.test("chips reverse ^ test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary <<
    b, z = [], []
    for j in range(0, 8):
        b.append(j)
        z.append(resize(a<<j, chips.common.how_many_bits(a)))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a << stimulus_b)))

    good = good and s.test("chips reverse << test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary >>
    b, z = [], []
    for j in range(0, 8):
        b.append(j)
        z.append(resize(a, chips.common.how_many_bits(a))>>j)

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a >> stimulus_b)))

    good = good and s.test("chips reverse >> test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary ==
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a==j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a == stimulus_b)))

    good = good and s.test("chips reverse == test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary !=
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a!=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a != stimulus_b)))

    good = good and s.test("chips reverse != test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary >=
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a>=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a >= stimulus_b)))

    good = good and s.test("chips reverse >= test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary <=
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a<=j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a <= stimulus_b)))

    good = good and s.test("chips reverse <= test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary >
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a>j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a > stimulus_b)))

    good = good and s.test("chips reverse > test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

    #Test Binary <
    b, z = [], []
    for j in range(-8, 8):
        b.append(j)
        z.append(-int(a<j))

    stimulus_b =        Sequence(*b)
    expected_response = Sequence(*z)
    s=Chip(Asserter(expected_response == (a < stimulus_b)))

    good = good and s.test("chips reverse < test {0}".format(a), stop_cycles=100)
    if not good and stop_on_fail: exit()

#Test Printer
s=Chip(Asserter(Printer(Repeater(10))==Sequence(ord('1'), ord('0'), ord('\n'))))

good = good and s.test("Printer test ", stop_cycles=2000)
if not good and stop_on_fail: exit()

#Test Scanner
s=Chip(Asserter(Scanner(Sequence(ord('1'), ord('0'), ord('\n')), 8)==Repeater(10)))

good = good and s.test("Scanner test ", stop_cycles=2000)
if not good and stop_on_fail: exit()

print "All Tests PASS"
