#!/usr/bin/env python


from math import asin, sin, cos, pi

#enter location details
lst=0
latitude = 51 #London
lonitude = 0 #London

#scale degrees so that 0=0 and 512=360 256=180 128=90
sin_values = []
for i in range(512):
    sin_values.append(round(sin((i/512.0)*2*pi)*255))

asin_values = []
for i in range(256):
    asin_values.append(round(asin(i/255.0)*(256.0/pi)))

#plot the sin values
#import matplotlib.pyplot as plt
#plt.plot(sin_values, 'bo')
#plt.ylabel('some numbers')
#plt.show()

#start of hardware design
from streams import *

#create a lookup table to lookup the sine of an angle
angle = Output()
sin_angle = Lookup(angle, *sin_values)

#create a lookup table to lookup the angle of arcsine
asin_angle = Output()
aangle = Lookup(asin_angle, *asin_values)

#create a lookup table of azimuths
right_assensions = Sequence(144, 137)
declinations = Sequence(-22, -73)

#create a process to calculate coordinates
ra = Variable(0)
dec = Variable(0)

alt = Variable(0)
az = Variable(0)

sin_lat = int(round(sin((512*51)/360)))
cos_lat = int(round(cos((512*51)/360)))


ha = Variable(0)

sin_dec = Variable(0)
cos_dec = Variable(0)
sin_ha  = Variable(0)
cos_ha  = Variable(0)
sin_alt  = Variable(0)
cos_alt  = Variable(0)
cos_az  = Variable(0)

display = Output()

Process(20, #gives integer range -512 to 511
    Loop(

       #read star coordinates in equitorial format
       right_assensions.read(ra),
       declinations.read(dec),

       #calculate ha based on LST
       ha.set(ra-lst),
       If(ha < 0, ha.set(512-ha)),

       #find sin dec
       If(dec < 0,
           angle.write(0-dec),
           sin_angle.read(sin_dec),
           sin_dec.set(0-sin_dec)
       ).ElsIf(1,
           angle.write(dec),
           sin_angle.read(sin_dec),
       ),

       #find cos dec 
       If(dec < 0,
           angle.write((0-dec)+128),
           sin_angle.read(cos_dec),
       ).ElsIf(1,
           angle.write(dec+128),
           sin_angle.read(cos_dec),
       ),

       #find sin ha
       If(ha < 0,
           angle.write(0-ha),
           sin_angle.read(sin_ha),
           sin_ha.set(0-sin_ha)
       ).ElsIf(1,
           angle.write(ha),
           sin_angle.read(sin_ha),
       ),

       #find cos ha 
       If(ha < 0,
           angle.write((0-ha)+128),
           sin_angle.read(cos_ha),
       ).ElsIf(1,
           angle.write(ha+128),
           sin_angle.read(cos_ha),
       ),

       #display.write(sin_ha),
       #display.write(cos_ha),
       #display.write(sin_dec),
       #display.write(cos_dec),

       sin_alt.set((sin_dec*sin_lat)>>9 + (((cos_dec*cos_lat)>>9)*cos_ha)>>9),

       #find asin sin_alt
       If(sin_alt < 0,
           asin_angle.write(0-sin_alt),
           aangle.read(alt),
           alt.set(0-alt),
       ).ElsIf(1,
           asin_angle.write(sin_alt),
           aangle.read(alt),
       ),

       #find cos_alt
       If(alt < 0,
           angle.write((0-alt)+128),
           sin_angle.read(cos_alt),
       ).ElsIf(1,
           angle.write(alt+128),
           sin_angle.read(cos_alt),
       ),

       cos_az.set(((sin_dec-((sin_alt*sin_lat)>>9)) // ((cos_alt*cos_lat)>>9))<<9),


       #find acos cos_az
       If(cos_az < 0,
           asin_angle.write(0-cos_az),
           aangle.read(az),
           az.set(az-128),
           If(az <= 0, az.set(512-az)),
       ).ElsIf(1,
           asin_angle.write(cos_az),
           aangle.read(az),
           az.set(az-128),
           If(az < 0, az.set(512-az)),
       ),

       display.write(alt),
       display.write(az),
    )
)

#Join the elements together into a system
s=System(
        sinks=(
            DecimalPrinter(display),
        )
)

#simulate in python
#import streams_python
#simulation_plugin = streams_python.Plugin()
#s.write_code(simulation_plugin)
#simulation_plugin.python_test("fixed test ", stop_cycles=1000)

#simulate in VHDL
import streams_VHDL
simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
simulation_plugin.ghdl_test("fixed test ", stop_cycles=10000, generate_wave=True)

