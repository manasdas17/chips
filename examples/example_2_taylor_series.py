#!/usr/bin/env python

"""Example 2 Sin Approximation using the taylor series

Options are:

simulate      - native python simulation
simulate_vhdl - simulate using ghdl cosimulation

Thing to try:

vary p        - the total number of bits in the approximation process
vary q        - the number of fraction bits in the fixed point representation
vary r        - the order of the power series, use odd values starting with 3"""

import sys
from math import pi
from chips import *

#fixed point routines
p = 26
q = 6
r = 9

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

    Process(p,
        Loop(
            angle.read(angle_var),
            approximation.set(angle_var),
            i.set(3),
            sign.set(-1),
            While( i <= r,

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
    from matplotlib import pyplot as pl

    x=n.linspace(to_fixed(0), to_fixed(pi), 100)
    response=Response(taylor(Sequence(*x)))
    chip = Chip(response)
    chip.reset()
    chip.execute(100000)
    sin_x=[from_fixed(i) for i in response.get_simulation_data()]
    pl.plot(sin_x[:100], 'b-', label="Taylor series approximation")
    pl.plot(n.sin(n.linspace(0,pi,100)), 'r-', label="sin(x)")
    pl.title("Sin Wave Approximation")
    pl.legend()
    pl.show()

elif "simulate_vhdl" in sys.argv:
    import numpy as n
    from matplotlib import pyplot as pl
    from chips.VHDL_plugin import Plugin
    x=n.linspace(to_fixed(0), to_fixed(pi), 100)
    response=Response(taylor(Sequence(*x)))
    chip = Chip(response)
    plugin = Plugin()
    chip.write_code(plugin)
    plugin.ghdl_test("test taylor series", stop_cycles=1000000)
    sin_x=[from_fixed(i) for i in response.get_simulation_data(plugin)]
    pl.plot(sin_x[:100], label="Taylor series approximation")
    pl.plot(n.sin(n.linspace(0,pi,100)), label="sin(x)")
    pl.title("Sin Wave Approximation")
    pl.legend()
    pl.show()

elif "simulate_cpp" in sys.argv:
    import numpy as n
    from matplotlib import pyplot as pl
    from chips.cpp_plugin import Plugin
    x=n.linspace(to_fixed(0), to_fixed(pi), 100)
    response=Response(taylor(Sequence(*x)))
    chip = Chip(response)
    plugin = Plugin()
    chip.write_code(plugin)
    plugin.test("test taylor series", stop_cycles=100000)
    sin_x=[from_fixed(i) for i in response.get_simulation_data(plugin)]
    pl.plot(sin_x[:100], label="Taylor series approximation")
    pl.plot(n.sin(n.linspace(0,pi,100)), label="sin(x)")
    pl.title("Sin Wave Approximation")
    pl.legend()
    pl.show()
