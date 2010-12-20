#!/usr/bin/env python

"""Example 5 PLot the positions of the 256 brightest stars as they would
appear when looking directly overhead. Plots the points on an avga monitor

Options are:

build - compile onto a xilinx FPGA"""

from math import asin, sin, cos, pi, radians
from datetime import datetime
from streams import *
import streams_VHDL
import sys

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
        for i in range(angle_scale/4+1):
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
           While(self.temp >= 512, self.temp.set(self.temp-512)),
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
           #bring angle into the range +/-255
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
    x = Variable(0)
    y = Variable(0)
    svga_stream = Output()
    count = Variable(0)
    us = Variable(0)
    ms = Variable(0)

    Process(20, #gives integer range -512 to 511

            #blank screen
            While(y<75,
               While(x<100,
                   svga_stream.write(x),
                   svga_stream.write(y),
                   svga_stream.write(0),
                   x.set(x+1),
               ),
               x.set(0),
               y.set(y+1),
            ),
            y.set(0),

            x.set(lst), y.set(0),
            While(x>=100, x.set(x-100), y.set(y+1)),
            svga_stream.write(0),
            svga_stream.write(0),
            svga_stream.write(0x30|y),

            y.set(0),
            While(x>=10, x.set(x-10), y.set(y+1)),
            svga_stream.write(1),
            svga_stream.write(0),
            svga_stream.write(0x30|y),

            y.set(0),
            While(x>=1, x.set(x-1), y.set(y+1)),
            svga_stream.write(2),
            svga_stream.write(0),
            svga_stream.write(0x30|y),

            #draw all stars
            count.set(0),
            While(count < 256,

               #read star coordinates in equitorial format
               ra_stream.read(ra),
               dec_stream.read(dec),

               #calculate ha based on LST
               ha.set(lst-ra),
               #While(ha < 0, ha.set(512+ha)),

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
               If(cos_az>255, cos_az.set(255)),
               If(cos_az<-255, cos_az.set(-255)),

               #find acos cos_az
               az.set(trig_tables.acos(cos_az)),
               If(sin_ha >= 0, az.set(512-az)),

               #Check if star is visible
               #If it is not, go to the next star
               If(alt<0, Continue()),

               #project points onto a plane
               x.set(trig_tables.sin(az)<<1),
               x.set(0-x),
               x.set((128-alt)*x),
               x.set(x>>8),

               y.set(trig_tables.cos(az)<<1),
               y.set((128-alt)*y),
               y.set(y>>8),

               x.set((512-(x+256))>>2),
               y.set((512-(y+256))>>2),

                If((x>=0)&(x<100)&(y>=0)&(y<75),
                   svga_stream.write(x),
                   svga_stream.write(y),
                   svga_stream.write(ord(".")),
                ),
               count.set(count+1),
            ),
    )

    return svga_stream

#Create simulation Model
################################################################################
#create a lookup table of azimuths
ra_degrees = [101.29, 95.99, 213.92, 219.90, 279.23, 79.17, 78.63, 114.83,
24.43, 88.79, 210.96, 297.70, 68.98, 247.35, 201.30, 116.33, 344.41, 191.93,
310.36, 186.65, 152.09, 104.66, 187.79, 263.40, 81.28, 81.57, 138.3, 84.05,
332.06, 193.51, 122.38, 51.08, 165.93, 107.10, 276.04, 125.63, 206.89,
264.33, 89.88, 99.43, 306.41, 95.68, 141.90, 113.65, 31.79, 239.88, 37.95,
283.82, 10.90, 85.19, 17.43, 211.67, 86.94, 2.10, 263.73, 222.68, 47.04,
177.27, 305.56, 137.00, 83.00, 10.13, 233.67, 269.15, 139.27, 120.90, 30.98,
200.98, 2.29, 240.08, 165.46, 326.05, 6.57, 345.94, 257.59, 319.65, 178.46,
111.02, 311.55, 346.19, 45.57, 168.53, 83.18, 183.95, 285.65, 229.25,
154.99, 241.36, 84.91, 28.66, 188.60, 236.07, 21.45, 208.67, 262.69, 74.25,
221.25, 275.25, 296.57, 243.59, 222.72, 265.87, 83.86, 247.56, 76.96,
262.61, 276.99, 3.31, 195.54, 82.06, 29.69, 326.76, 56.87, 95.74, 245.30,
287.44, 111.79, 194.01, 322.89, 340.75, 59.51, 187.47, 331.45, 100.98,
146.46, 271.45, 286.35, 75.49, 182.53, 95.08, 218.02, 34.84, 230.18, 155.58,
288.14, 292.68, 305.25, 87.74, 258.76, 134.80, 257.20, 76.63, 354.84,
322.17, 44.57, 284.74, 244.58, 343.66, 93.72, 226.02, 231.23, 183.86,
168.56, 117.32, 101.32, 127.57, 203.67, 28.60, 193.90, 46.29, 340.37, 28.27,
12.28, 154.17, 154.27, 282.52, 17.15, 40.83, 169.62, 258.66, 225.49, 124.13,
145.29, 67.15, 332.55, 110.03, 83.78, 55.81, 4.86, 304.51, 177.67, 130.07,
57.29, 309.39, 211.10, 64.95, 190.42, 325.02, 231.96, 56.22, 298.83, 176.51,
27.87, 75.62, 268.38, 65.73, 42.67, 309.91, 311.92, 106.03, 111.43, 247.73,
68.89, 56.08, 297.04, 163.33, 172.85, 335.41, 48.02, 56.46, 69.55, 220.77,
148.19, 44.11, 184.98, 233.88, 318.96, 131.17, 290.97, 93.71, 290.66,
243.00, 201.31, 284.91, 182.10, 308.30, 62.97, 59.74, 216.30, 325.88,
214.00, 164.94, 287.37, 105.94, 91.03, 334.21, 56.58, 304.41, 125.71,
134.62, 26.35, 188.44, 330.95, 290.81, 56.30, 142.93, 231.12, 17.78, 30.51,
47.91, 263.05, 295.02, 288.44, 262.68, 169.55, 63.82]
#
dec_degrees = [262.37, 102.43, 102.97, 66.78, 157.17, 92.81, 330.65, 243.91,
112.62, 294.25, 340.30, 65.27, 197.19, 349.67, 231.24, 354.95, 29.51, 76.95,
353.81, 278.20, 100.32, 100.03, 43.30, 97.55, 209.54, 348.10, 59.22, 130.52,
15.67, 74.50, 265.56, 55.97, 334.72, 277.27, 91.72, 82.17, 235.19, 85.93,
39.71, 67.95, 149.81, 301.73, 143.65, 257.79, 170.71, 96.41, 164.17, 329.93,
94.66, 179.51, 277.87, 318.93, 134.56, 4.34, 236.05, 44.60, 98.60, 171.48,
307.93, 272.45, 42.33, 60.71, 150.63, 340.62, 179.31, 301.52, 16.14, 215.56,
175.03, 195.66, 284.01, 221.96, 3.15, 70.58, 230.05, 195.41, 136.03, 13.08,
98.42, 357.65, 255.95, 312.35, 26.61, 300.24, 96.69, 152.94, 353.01, 305.54,
160.15, 332.93, 278.91, 107.35, 320.36, 266.35, 245.04, 298.02, 318.88,
275.73, 97.74, 294.05, 104.64, 278.99, 264.61, 178.29, 346.06, 99.54,
151.91, 214.84, 124.73, 85.86, 296.31, 254.16, 69.82, 347.60, 218.71,
200.85, 122.10, 354.14, 210.16, 80.62, 35.14, 270.15, 255.25, 106.11,
359.07, 86.52, 323.58, 146.77, 311.42, 26.02, 253.46, 248.92, 236.35, 93.86,
282.84, 46.80, 284.41, 104.97, 186.77, 219.44, 137.04, 256.87, 297.02,
197.94, 87.88, 315.59, 310.37, 357.75, 13.04, 64.28, 80.28, 54.04, 337.93,
153.00, 347.70, 135.31, 201.24, 153.33, 169.33, 27.43, 27.33, 259.08,
164.46, 140.78, 11.98, 282.94, 316.12, 57.47, 36.32, 114.45, 209.05,
71.57, 97.82, 125.79, 176.75, 237.09, 3.93, 51.53, 124.31, 232.22, 330.51,
116.65, 351.19, 216.58, 309.65, 125.38, 242.77, 5.09, 153.74, 105.98,
273.22, 115.87, 138.93, 231.69, 229.68, 75.58, 70.17, 293.87, 112.72,
125.52, 244.56, 18.27, 8.75, 206.19, 133.58, 125.15, 112.06, 320.84, 33.41,
137.50, 356.63, 307.72, 222.65, 50.43, 250.63, 87.89, 250.94, 298.60,
340.30, 256.70, 359.50, 233.30, 118.64, 121.86, 325.30, 215.73, 327.60,
16.66, 254.23, 75.66, 90.57, 207.39, 125.02, 237.19, 55.89, 46.98, 155.25,
353.17, 210.66, 250.80, 125.30, 38.67, 310.48, 163.83, 151.09, 133.70,
278.55, 246.58, 253.16, 278.92, 12.06, 117.78, 249.43, 51.91, 40.44, 66.90]

ra_stream = Sequence(*tuple((i/360.0*512.0 for i in ra_degrees)))
dec_stream = Sequence(*tuple((i/360.0*512.0 for i in dec_degrees)))

#Create synthesis Model
################################################################################

if "build" in sys.argv:
    import streams_VHDL
    import os
    import shutil
    svga_stream = translate_coordinates(ra_stream, dec_stream)
    system=System(SVGA(Resizer(svga_stream, 8)))
    plugin = streams_VHDL.Plugin(internal_clock=False, internal_reset=False)
    system.write_code(plugin)
    from_file=os.path.join(".", "ucfs", "example_5.ucf")
    to_file=os.path.join(".", "project", "xilinx", "project.ucf")
    shutil.copy(from_file, to_file)
    plugin.xilinx_build("xc3s200-4-ft256")
