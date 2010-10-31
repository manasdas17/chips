#!/usr/bin/env python

from math import pi, sin

from streams import *
from streams_VHDL import Plugin

#define a few fixed point routines
################################################################################

q=8 #define radix point

def to_fixed(x):
    return int(round(x * (2**q)))

def from_fixed(x):
    return x * (2**-q)

def mul(x, y):
    return (x * y) >> q

#define a fft component
################################################################################
def fft(input_stream, points):

    data=VariableArray(points*2)#use alternate locations for real and imaginay
    nn = points
    n = nn << 1

    #set up initial values for trig reccurence
    thetas = [(2.0*pi)*(2.0**-i) for i in range(1, n)]
    wpr_lut = Sequence(*[to_fixed(-2.0*sin(0.5*i)*sin(0.5*i)) for i in thetas])
    wpi_lut = Sequence(*[to_fixed(sin(i)) for i in thetas])

    print [to_fixed(-2.0*sin(0.5*i)*sin(0.5*i)) for i in thetas]

    i = Variable(0)
    j = Variable(0)
    mmax = Variable(0)
    m = Variable(0)
    istep = Variable(0)
    swap_0 = Variable(0)
    swap_1 = Variable(0)
    tempr = Variable(0)
    tempi = Variable(0)
    xr = Variable(0)
    xi = Variable(0)
    wr = Variable(0)
    wi = Variable(0)
    wpr = Variable(0)
    wpi = Variable(0)
    output_stream = Output()

    Process(100,

        #read data into array
        i.set(0),
        While(i<n,
            input_stream.read(j),
            data.write(i, j),
            i.set(i+1),
        ),

        #bitswap reordering
        j.set(1),
        i.set(1),
        While(i<n,
            If(j>i,
                swap_0.set(data.read(j-1)),
                swap_1.set(data.read(i-1)),
                data.write(j-1, swap_1),
                data.write(i-1, swap_0),
                swap_0.set(data.read(j)),
                swap_1.set(data.read(i)),
                data.write(j, swap_1),
                data.write(i, swap_0),
            ),
            m.set(nn),
            While((m>=2)&(j>m),
                j.set(j-m),
                m.set(m>>1),
            ),
            j.set(j+m),
            i.set(i+2),
        ),

        #butterfly multiplies
        mmax.set(2),
        While(n>mmax,
            istep.set(mmax<<1),

            #initialize trigonometric reccurence
            wpr_lut.read(wpr),
            wpi_lut.read(wpi),
            wr.set(to_fixed(1.0)),
            wi.set(to_fixed(0.0)),
            m.set(1),
            While(m<mmax,
                i.set(m),
                While(i<=n,
                    j.set(i+mmax),

                    xr.set(data.read(j-1)),
                    xi.set(data.read(j)),

                    tempr.set(((wr*xr)>>q)-((wi*xi)>>q)),
                    tempi.set(((wr*xi)>>q)+((wi*xr)>>q)),

                    xr.set(data.read(i-1)),
                    xi.set(data.read(i)),

                    data.write(j-1, xr-tempr),
                    data.write(j  , xi-tempi),
                    data.write(i-1, xr+tempr),
                    data.write(i  , xi+tempi),

                    i.set(i+istep),
                ),
                #trigonometric reccurence
                swap_0.set(wr),
                wr.set(((wr*wpr)>>q)-((wi*wpi    )>>q)+wr),
                wi.set(((wi*wpr)>>q)-((swap_0*wpi)>>q)+wi),
                m.set(m+2),
            ),
            mmax.set(istep),
        ),

        #write out data from array
        i.set(0),
        While(i<n,
            j.set(data.read(i)),
            output_stream.write(j),
            i.set(i+1),
        ),
    )

    return output_stream


#test fft component
################################################################################
import numpy as n
import scipy as s
from matplotlib import pyplot as p
from math import pi, sqrt

#create a cosine to stimulate the fft
x = n.arange(128)
cos_x = s.cos(2*pi*x/128)

#pack the stimulus into the correct format
complex_time = []
for i in cos_x:
    complex_time.append(to_fixed(i))
    complex_time.append(0)#set immaginary part to zero

#build a simulation model
response = Response(fft(Sequence(*complex_time), 128))
system = System(response)

#run the simulation
system.reset()
system.execute(100000)

#unpack the frequency domain representation
complex_frequency = list(response.get_simulation_data())

frequency_magnitude = []
for i in xrange(0, 254, 2):
    mag = sqrt(complex_frequency[i]**2.0 + complex_frequency[i+1]**2.0)
    frequency_magnitude.append(from_fixed(mag))

p.plot(abs(s.fft(cos_x)))
p.plot(frequency_magnitude)
p.show()

