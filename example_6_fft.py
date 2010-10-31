#!/usr/bin/env python

from math import pi, sin, log, cos

from streams import *
from streams_VHDL import Plugin

#define a few fixed point routines
################################################################################

q=10 #define radix point

def to_fixed(x):
    return int(round(x * (2**q)))

def from_fixed(x):
    return x * (2**-q)

def mul(x, y):
    return (x * y) >> q

#define a fft component
################################################################################
def fft(input_stream, n):

    rex=VariableArray(n)
    imx=VariableArray(n)
    nm1=n-1
    nd2=n>>1
    m=int(log(n,2))

    #set up initial values for trig reccurence
    thetas = []
    for l in range(1, m+1):
        le=1<<l
        le2=le>>1
        thetas.append(pi/le2)

    sr_lut = Sequence(*[to_fixed(cos(i)) for i in thetas])
    si_lut = Sequence(*[to_fixed(-sin(i)) for i in thetas])

    i = Variable(0)
    ip = Variable(0)
    j = Variable(0)
    jm1 = Variable(0)
    l = Variable(0)
    k = Variable(0)
    le = Variable(0)
    le2 = Variable(0)
    tr = Variable(0)
    ti = Variable(0)
    xr = Variable(0)
    xi = Variable(0)
    ur = Variable(0)
    ui = Variable(0)
    sr = Variable(0)
    si = Variable(0)
    real = Output()
    imaginary = Output()

    Process(26,

        #read data into array
        i.set(0),
        While(i<n,
            input_stream.read(j),
            rex.write(i, j),
            input_stream.read(j),
            imx.write(i, j),
            i.set(i+1),
        ),

        #bitswap reordering

        j.set(nd2),
        i.set(1),
        While(i<=(n-2),
            If(i<j,
                tr.set(rex.read(j)),
                ti.set(imx.read(j)),
                rex.write(j, rex.read(i)),
                imx.write(j, imx.read(i)),
                rex.write(i, tr),
                imx.write(i, ti),
            ),
            k.set(nd2),
            While(k<=j,
               j.set(j-k),
               k.set(k>>1),
            ),
            j.set(j+k),
            i.set(i+1),
        ),

        #butterfly multiplies
        l.set(1),
        While(l<=m,
            le.set(1<<l),
            le2.set(le>>1),

            #initialize trigonometric reccurence

            ur.set(to_fixed(1.0)),
            ui.set(to_fixed(0.0)),

            sr_lut.read(sr),
            si_lut.read(si),

            j.set(1),
            While(j<=le2,
                jm1.set(j-1),
                i.set(jm1),
                While(i<=nm1,
                    ip.set(i+le2),

                    xr.set(rex.read(ip)),
                    xi.set(imx.read(ip)),

                    tr.set(((xr*ur)>>q)-((xi*ui)>>q)),
                    ti.set(((xr*ui)>>q)+((xi*ur)>>q)),

                    xr.set(rex.read(i)),
                    xi.set(imx.read(i)),

                    rex.write(ip, xr-tr),
                    imx.write(ip, xi-ti),
                    rex.write(i, xr+tr),
                    imx.write(i, xi+ti),

                    i.set(i+le),
                ),
                #trigonometric reccurence
                tr.set(ur),
                ur.set(((tr*sr)>>q)-((ui*si)>>q)),
                ui.set(((tr*si)>>q)+((ui*sr)>>q)),
                j.set(j+1),
            ),
            l.set(l+1),
        ),

        #write out data from array
        i.set(0),
        While(i<n,
            j.set(rex.read(i)),
            real.write(j),
            i.set(i+1),
        ),
        i.set(0),
        While(i<n,
            j.set(imx.read(i)),
            imaginary.write(j),
            i.set(i+1),
        ),
    )

    return real, imaginary


#test fft component
################################################################################
import numpy as n
import scipy as s
from matplotlib import pyplot as p
from math import pi, sqrt

#create a cosine to stimulate the fft
x = n.arange(64)
cos_x = n.zeros(128)
cos_x[0:64] = s.cos(2*pi*x/64)

#pack the stimulus into the correct format
complex_time = []
for i in cos_x:
    complex_time.append(to_fixed(i))
    complex_time.append(0.0)

#build a simulation model
real, imaginary = fft(Sequence(*complex_time), 128)
rer = Response(real)
imr = Response(imaginary)
system = System(rer, imr)

#run the simulation
system.reset()
system.execute(100000)

#unpack the frequency domain representation
real_frequency = list(rer.get_simulation_data())
imaginary_frequency = list(imr.get_simulation_data())

frequency_magnitude = []
for i in xrange(0, 128):
    mag = sqrt(real_frequency[i]**2+imaginary_frequency[i]**2)
    frequency_magnitude.append(from_fixed(mag))

p.plot(abs(s.fft(cos_x)))
p.plot(frequency_magnitude)
p.show()

