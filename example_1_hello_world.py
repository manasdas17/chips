#!/usr/bin/env python
"""Example 1 Hello World .... in welsh!

options are:

simulate      - native python simulation
simulate_vhdl - simulate using ghdl cosimulation
build         - compile into a xilinx fpga
test          - check the results using the serial port"""

import sys

from streams import * #use the streams library
import streams_VHDL #import VHDL plugin 


################################################################################
##make a simulation model that prints to stdout

def make_system(string, output):
    return System(
            output(
                Sequence(*tuple((ord(i) for i in string))+(0,)),
            )
        )

if "simulate" in sys.argv:
    #write the system to the code generator plugin
    system=make_system("hello byd!\n", Console)
    system.test("Example 1: Hello World .... in welsh!", stop_cycles=100)

if "simulate_vhdl" in sys.argv:
    #simulate using an external vhdl simulator
    system=make_system("hello byd!\n", Console)
    vhdl_plugin = streams_VHDL.Plugin()
    system.write_code(vhdl_plugin)
    vhdl_plugin.ghdl_test("Example 1 : Hello world .... in welsh!", stop_cycles=2000)

if "build" in sys.argv:
    import os
    import shutil
    #compile into a xilinx device
    system=make_system("hello byd!\n", SerialOut)
    vhdl_plugin = streams_VHDL.Plugin(internal_reset=False, internal_clock=False)
    system.write_code(vhdl_plugin)
    from_file=os.path.join(".", "ucfs", "example_1.ucf")
    to_file=os.path.join(".", "project", "xilinx", "project.ucf")
    shutil.copy(from_file, to_file)
    vhdl_plugin.xilinx_build("xc3s200-4-ft256")

if "test" in sys.argv:
    #capture output from serial port
    from serial import Serial
    port = Serial('/dev/ttyS0', baudrate=115200, bytesize=8, parity="N", stopbits=1)
    response = port.readline()
    print response
    port.close()