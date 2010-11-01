#!/usr/bin/env python
import sys
from math import pi
from streams import *

#fixed point routines
q = 8

def to_fixed(x):
    return int(round(x*(2**q)))

def from_fixed(x):
    return x*(2**-q)

#create taylor series
def taylor(angle):

    sin_out = Output()
    approximation = Variable(0)
    i = Variable(0)
    power = Variable(0)
    fact = Variable(0)
    count = Variable(0)
    angle_var = Variable(0)
    sign = Variable(0)

    Process(32,
        Loop(
            angle.read(angle_var),
            approximation.set(angle_var),
            i.set(3),
            sign.set(-1),
            While( i <= 9,

                #calculate x**i
                count.set(0),
                power.set(to_fixed(1.0)),
                While(count<i, power.set((power*angle_var)>>q), count.set(count+1)),

                #calculate x!
                count.set(1),
                fact.set(1),
                While(count<=i, fact.set(fact*count), count.set(count+1)),

                #calculate x**i/i!
                approximation.set(approximation + (sign*(power//fact))),
                sign.set(0-sign),


                i.set(i+2),
            ),
            sin_out.write(approximation),
        )
    )
    return sin_out

if "simulate" in sys.argv:
    import numpy as n
    from matplotlib import pyplot as p

    x=n.linspace(to_fixed(0), to_fixed(pi), 100)
    response=Response(taylor(Sequence(*x)))
    system = System(response)
    system.reset()
    system.execute(100000)
    sin_x=[from_fixed(i) for i in response.get_simulation_data()]
    p.plot(sin_x[:100])
    p.plot(n.sin(n.linspace(0,pi,100)))
    p.show()

elif "simulate_vhdl" in sys.argv:
    import numpy as n
    from matplotlib import pyplot as p
    import streams_VHDL
    x=n.linspace(to_fixed(0), to_fixed(pi), 100)
    response=Response(taylor(Sequence(*x)))
    system = System(response)
    plugin = streams_VHDL.Plugin()
    system.write_code(plugin)
    plugin.ghdl_test("test taylor series", stop_cycles=10000, generate_wave=True)
    sin_x=[from_fixed(i) for i in response.get_simulation_data(plugin)]
    p.plot(sin_x[:100])
    p.plot(n.sin(n.linspace(0,pi,100)))
    p.show()
