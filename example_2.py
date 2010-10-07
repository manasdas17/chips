#!/usr/bin/env python

"""Example, driving a 4 digit 7 segment display"""
from streams import *
import streams_VHDL

def seven_segment_driver(input_stream):
    number = Variable(0)
    digit_0 = Variable(0)
    digit_1 = Variable(0)
    digit_2 = Variable(0)
    digit_3 = Variable(0)
    cursor = Output()
    digit = Output()
    Process(16,
        Loop(
            input_stream.read(number),
            digit_0.set(1),
            digit_1.set(2),
            digit_2.set(3),
            digit_3.set(4),
            Loop(
                cursor.write(1),
                digit.write(digit_0),
                Wait(50000000*0.001),
                cursor.write(2),
                digit.write(digit_1),
                Wait(50000000*0.001),
                cursor.write(4),
                digit.write(digit_2),
                Wait(50000000*0.001),
                cursor.write(8),
                digit.write(digit_3),
            )
        )
    )
    return cursor, digit

cursor, digit = seven_segment_driver(Repeater(10))

system = System(
    sinks = (Printer(cursor),Printer(digit)),
)

#create a code generator plugin
vhdl_plugin = streams_VHDL.Plugin()

#write the system to the code generator plugin
system.write_code(vhdl_plugin)

#simulate using an external vhdl simulator
vhdl_plugin.ghdl_test("Example 2 : Seven Segment Display", stop_cycles=2000, generate_wave=True)
