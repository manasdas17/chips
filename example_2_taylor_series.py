#!/usr/bin/env python
from math import pi
from streams import *

angle = Repeater(int(pi/4.0*(2**8)))
sin_out = Output()
sin = Response(sin_out)

approximation = Variable(0)
i = Variable(0)
power = Variable(0)
fact = Variable(0)
count = Variable(0)
angle_var = Variable(0)
sign = Variable(0)

Process(32,
        angle.read(angle_var),
        sin_out.write(10),
        i.set(3),
        sign.set(-1),
        While( i <= 7,

            #calculate x**i
            count.set(i),
            power.set(1<<8),
            While(count > 0, power.set((power*angle_var)>>8), count.set(count-1)),

            #calculate x!
            count.set(1),
            fact.set(1),
            While(count<=i, fact.set(fact*count), count.set(count+1)),

            #calculate x**i/x!
            approximation.set(approximation + (sign*(power//fact))),
            sign.set(0-sign),

            sin_out.write(approximation),

            i.set(i+2),

        )
)

system = System((sin,))
system.reset()
system.execute(10000)
print list(sin.get_simulation_data())
for i in sin.get_simulation_data():
    print i*(2**-8)

import streams_VHDL
p = streams_VHDL.Plugin()
system.write_code(p)
p.ghdl_test("test taylor series", stop_cycles=100000, generate_wave=True)
print sin.get_simulation_data(p)
for i in sin.get_simulation_data(p):
    print i*(2**-8)
