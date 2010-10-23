#!/usr/bin/env python

from math import asin, sin, cos, pi, radians
from datetime import datetime

#enter location details
latitude = 51 #London
longitude = -3.3 #London

local_time = datetime.now()
local_time_degrees = (local_time.hour + (local_time.minute/60.0) + (local_time.second/3600.0))*15
J2000 = datetime(2000, 01, 01, 12, 00)
delta_J2000 = (local_time - J2000)
delta_J2000_days = delta_J2000.days + (delta_J2000.seconds/86400.0)

lst = 100.46 + (0.985647 * delta_J2000_days) + local_time_degrees + longitude
lst = lst%360.0
lst = lst*512.0/360.0

def to_radians(x): return (x/256.0)*pi
def from_radians(x): return (x/pi)*256.0
def scale(x): return x*255
def unscale(x): return (x/255.0)

#scale degrees so that 0=0 and 512=360 256=180 128=90
#scale sin tables so that 1 = 255 and -1 = -255
sin_values = []
for i in range(512):
    sin_values.append(scale(sin(to_radians(i))))

asin_values = []
for i in range(256):
    asin_values.append(from_radians(asin(unscale(i))))


#create a lookup table to lookup the sine of an angle

sin_in = Output()
sin_out = Lookup(angle, *sin_values)

def fsin(x)
    return Evaluate(
       #find sin dec
       If(x < 0,
           sin_in.write(0-x),
           sin_out.read(temp),
           temp.set(0-temp)
       ).ElsIf(1,
           sin.write(x),
           temp.read(temp),
       ),
       Value(temp),
    )

def fcos(x)
    return Evaluate(
       #find sin dec
       If(x < 0,
           sin_in.write((0-x)+128),
           sin_out.read(temp),
           temp.set(0-temp)
       ).ElsIf(1,
           sin.write(x+128),
           temp.read(temp),
       ),
       Value(temp),
    )

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

sin_lat = int(round(sin(radians(latitude))*255))
cos_lat = int(round(cos(radians(latitude))*255))


ha = Variable(0)

sin_dec = Variable(0)
cos_dec = Variable(0)
sin_ha  = Variable(0)
cos_ha  = Variable(0)
sin_alt  = Variable(0)
cos_alt  = Variable(0)
cos_az  = Variable(0)

alt_stream = Output()
az_stream = Output()

Process(20, #gives integer range -512 to 511
    Loop(

       #read star coordinates in equitorial format
       right_assensions.read(ra),
       declinations.read(dec),

       #calculate ha based on LST
       ha.set(lst-ra),
       While(ha < 0, ha.set(512+ha)),

       #find sin dec
       sin_dec.set(fsin(dec)),
       cos_dec.set(fcos(dec)),
       sin_ha.set(fsin(ha)),
       cos_ha.set(fcos(ha)),


       sin_alt.set(((sin_dec*sin_lat)>>8) + ((((cos_dec*cos_lat)>>8)*cos_ha)>>8)),
       #sin_alt.set((sin_dec*sin_lat)>>8),

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

       cos_az.set(((sin_dec-((sin_alt*sin_lat)>>8))<<8) // ((cos_alt*cos_lat)>>8)),

       #find acos cos_az
       If(cos_az < 0,
           asin_angle.write(0-cos_az),
           aangle.read(az),
           az.set(az-128),
           If(az <= 0, az.set(512+az)),
       ).ElsIf(1,
           asin_angle.write(cos_az),
           aangle.read(az),
           az.set(az-128),
           If(az < 0, az.set(512+az)),
       ),

       alt_stream.write(alt),
       az_stream.write(cos_az),
    )
)

alt_response = Response(alt_stream)
az_response = Response(az_stream)

#Join the elements together into a system
s=System(
        sinks=(alt_response, az_response)
)

s.test("fixed test ", stop_cycles=1000)
for i, j in zip(alt_response.get_simulation_data(), az_response.get_simulation_data()):
    print i/512.0*360.0,
    print j/255.0


#simulate in VHDL
import streams_VHDL
simulation_plugin = streams_VHDL.Plugin()
s.write_code(simulation_plugin)
simulation_plugin.ghdl_test("fixed test ", stop_cycles=10000, generate_wave=True)

