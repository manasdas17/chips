#!/usr/bin/env python

from math import asin, sin, cos, pi, radians
from datetime import datetime
from streams import *
import streams_VHDL

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

#def local_time_to_lst(year, month, day, hour, minutes):
    #return Evaluate(
        #If(year==1998, J2000_days.set(-731.5 * (2**8)),
        #If(year==1999, J2000_days.set(-366.5 * (2**8)),
        #If(year==1900, J2000_days.set(-1.5   * (2**8)),
        #If(year==2001, J2000_days.set(-364.5 * (2**8)),
        #If(year==2002, J2000_days.set(-729.5 * (2**8)),
        #If(year==2003, J2000_days.set(-1094.5* (2**8)),
        #If(year==2004, J2000_days.set(-1459.5* (2**8)),
        #If(year==2005, J2000_days.set(-1825.5* (2**8)),
        #If(year==2006, J2000_days.set(-2190.5* (2**8)),
        #If(year==2007, J2000_days.set(-2555.5* (2**8)),
        #If(year==2008, J2000_days.set(-2920.5* (2**8)),
        #If(year==2009, J2000_days.set(-3286.5* (2**8)),
        #If(year==2010, J2000_days.set(-3651.5* (2**8)),
        #If(year==2011, J2000_days.set(-4016.5* (2**8)),
        #If(year==2012, J2000_days.set(-4381.5* (2**8)),
        #If(year==2013, J2000_days.set(-4747.5* (2**8)),
        #If(year==2014, J2000_days.set(-5112.5* (2**8)),
        #If(year==2015, J2000_days.set(-5477.5* (2**8)),
        #If(year==2016, J2000_days.set(-5842.5* (2**8)),
        #If(year==2017, J2000_days.set(-6208.5* (2**8)),
        #If(year==2018, J2000_days.set(-6573.5* (2**8)),
        #If(year==2019, J2000_days.set(-6938.5* (2**8)),
        #If(year==2020, J2000_days.set(-7303.5* (2**8)),
        #If(year==2021, J2000_days.set(-7669.5* (2**8)),
        #If(month==1,  J2000_days.set(J2000_days + 0 * (2**8))),
        #If(month==2,  J2000_days.set(J2000_days + 31 * (2**8))),
        #If(month==3,  J2000_days.set(J2000_days + 59 * (2**8))),
        #If(month==4,  J2000_days.set(J2000_days + 90 * (2**8))),
        #If(month==5,  J2000_days.set(J2000_days + 120 * (2**8))),
        #If(month==6,  J2000_days.set(J2000_days + 151 * (2**8))),
        #If(month==7,  J2000_days.set(J2000_days + 181 * (2**8))),
        #If(month==8,  J2000_days.set(J2000_days + 212 * (2**8))),
        #If(month==9,  J2000_days.set(J2000_days + 243 * (2**8))),
        #If(month==10, J2000_days.set(J2000_days + 273 * (2**8))),
        #If(month==11, J2000_days.set(J2000_days + 304 * (2**8))),
        #If(month==12, J2000_days.set(J2000_days + 334 * (2**8))),
        #If(Year%4==0,
            #J2000_days.set(J2000_days + 1 * (2**8)),
            #If(Year%100==0,
                #J2000_days.set(J2000_days - 1 * (2**8)),
                #If(year%400==0, J2000_days.set(J2000_days+1 * (2**8)),)
            #)
        #)



#create sin and cosine function using lookup tables
################################################################################

class TrigTables:
    def __init__(self, angle_scale=512, ratio_scale=255):

        def to_radians(x): return (x/float(angle_scale))*2*pi
        def from_radians(x): return (x/(2*pi))*angle_scale
        def scale(x): return x*ratio_scale
        def unscale(x): return (x/float(ratio_scale))

        #generate table to cover 1 quadrant only
        sin_values = []
        for i in range(angle_scale/4):
            sin_values.append(scale(sin(to_radians(i))))
        self.sin_in = Output()
        self.sin_out = Lookup(self.sin_in, *sin_values)
        self.temp = Variable(0)

        #generate table to cover 1 quadrant only
        asin_values = []
        for i in range(ratio_scale + 1):
            asin_values.append(from_radians(asin(unscale(i))))
        self.asin_in = Output()
        self.asin_out = Lookup(self.asin_in, *asin_values)

    def sin(self,x):
        return Evaluate(
           self.temp.set(x),
           #bring angle into the range 0-512
           While(self.temp < 0, self.temp.set(self.temp+512)),
           #sin 256-512 is a negative version of 0-128
           If(self.temp >= 256, 
               self.temp.set(self.temp-256),
               #sin 128-256 is a reflection about 128 of 0-128
               If(self.temp >= 128, self.temp.set(128-(self.temp-128))),
               self.sin_in.write(self.temp),
               self.sin_out.read(self.temp),
               self.temp.set(0-self.temp)
           ).ElsIf(1,
               #sin 128-256 is a reflection about 128 of 0-128
               If(self.temp >= 128, self.temp.set(128-(self.temp-128))),
               self.sin_in.write(self.temp),
               self.sin_out.read(self.temp),
           ),
           Value(self.temp),
        )

    def cos(self, x):
        return Evaluate(
           self.temp.set(x+128),
           Value(self.sin(self.temp)),
        )

    def asin(self, x):
        return Evaluate(
           If(x < 0,
               self.asin_in.write(0-x),
               self.asin_out.read(self.temp),
               self.temp.set(0-self.temp),
           ).ElsIf(1,
               self.asin_in.write(x),
               self.asin_out.read(self.temp),
           ),
           Value(self.temp)
        )

    def acos(self, x):
        return Evaluate(
           self.temp.set(self.asin(x)-128),
           If(self.temp < 0, self.temp.set(0-self.temp)),
           Value(self.temp)
        )

#create a coordinate translator
################################################################################

def translate_coordinates(ra_stream, dec_stream):

    trig_tables = TrigTables()

    sin_lat = int(round(sin(radians(latitude))*255))
    cos_lat = int(round(cos(radians(latitude))*255))

    #create a process to calculate coordinates
    ra = Variable(0)
    dec = Variable(0)
    alt = Variable(0)
    az = Variable(0)
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

    Process(32, #gives integer range -512 to 511
        Loop(

           #read star coordinates in equitorial format
           ra_stream.read(ra),
           dec_stream.read(dec),

           #calculate ha based on LST
           ha.set(lst-ra),
           While(ha < 0, ha.set(512+ha)),

           #find sin dec
           sin_dec.set(trig_tables.sin(dec)),
           cos_dec.set(trig_tables.cos(dec)),
           sin_ha.set(trig_tables.sin(ha)),
           cos_ha.set(trig_tables.cos(ha)),

           sin_alt.set(((sin_dec*sin_lat)>>8) + ((((cos_dec*cos_lat)>>8)*cos_ha)>>8)),

           #find asin sin_alt
           alt.set(trig_tables.asin(sin_alt)),

           #find cos_alt
           cos_alt.set(trig_tables.cos(alt)),
           cos_az.set(((sin_dec-((sin_alt*sin_lat)>>8))<<8) // ((cos_alt*cos_lat)>>8)),

           #find acos cos_az
           az.set(trig_tables.acos(cos_az)),
           If(sin_ha >= 0, az.set(512-az)),

           alt_stream.write(alt),
           az_stream.write(az),
        )
    )

    return alt_stream, az_stream

#Create simulation Model
################################################################################

#create a lookup table of azimuths
ra_stream = Sequence(144, 137)
dec_stream = Sequence(-22, -73)
alt_stream, az_stream = translate_coordinates(ra_stream, dec_stream)
alt_response = Response(alt_stream)
az_response = Response(az_stream)

#Join the elements together into a system
simulation_model=System(
        sinks=(alt_response, az_response)
)

simulation_model.test("fixed test ", stop_cycles=10000)
for i, j in zip(alt_response.get_simulation_data(), az_response.get_simulation_data()):
    print i/512.0*360,
    print j/512.0*360

simulation_plugin = streams_VHDL.Plugin()
simulation_model.write_code(simulation_plugin)
simulation_plugin.ghdl_test("fixed test", stop_cycles = 1000000)
for i, j in zip(alt_response.get_simulation_data(simulation_plugin), az_response.get_simulation_data()):
    print i/512.0*360.0,
    print j/512.0*360.0

#Create synthesis Model
################################################################################

#create a lookup table of azimuths
ra_stream = Sequence(144, 137)
dec_stream = Sequence(-22, -73)
alt_stream, az_stream = translate_coordinates(ra_stream, dec_stream)
alt_response = OutPort(alt_stream, "ALT")
az_response = OutPort(az_stream, "AZ")

#Join the elements together into a system
synthesis_model=System(
        sinks=(alt_response, az_response)
)
simulation_plugin = streams_VHDL.Plugin(internal_reset=False, internal_clock=False)
synthesis_model.write_code(simulation_plugin)
#simulation_plugin.xilinx_build()

