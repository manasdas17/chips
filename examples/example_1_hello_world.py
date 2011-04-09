#!/usr/bin/env python
"""Example 1 Hello World .... in welsh!

options are:

simulate      - native python simulation
simulate_vhdl - simulate using ghdl cosimulation
build         - compile into a xilinx fpga
test          - check the results using the serial port"""

import sys

from chips import * #use the chips library


################################################################################
##make a simulation model that prints to stdout

def make_chip(string, output):
    return Chip(
            output(
                Sequence(*tuple((ord(i) for i in string))+(0,)),
            )
        )

if "simulate" in sys.argv:
    #write the chip to the code generator plugin
    chip=make_chip("helo byd!\n", Console)
    chip.test("Example 1: Hello World .... in welsh!", stop_cycles=100)

if "simulate_vhdl" in sys.argv:
    import chips_VHDL #import VHDL plugin 
    #simulate using an external vhdl simulator
    chip=make_chip("helo byd!\n", Console)
    vhdl_plugin = chips_VHDL.Plugin()
    chip.write_code(vhdl_plugin)
    vhdl_plugin.ghdl_test("Example 1 : Hello world .... in welsh!", stop_cycles=2000)

if "simulate_cpp" in sys.argv:
    import chips_cpp #import C++ plugin 
    #simulate using an external vhdl simulator
    chip=make_chip("helo byd!\n", Console)
    cpp_plugin = chips_cpp.Plugin()
    chip.write_code(cpp_plugin)
    cpp_plugin.test("Example 1 : Hello world .... in welsh!", stop_cycles=2000)

if "visualize" in sys.argv:
    import chips_visual
    #simulate using an external vhdl simulator
    chip=make_chip("helo byd!\n", Console)
    visual_plugin = chips_visual.Plugin("Example 1 : Hello world .... in welsh!")
    chip.write_code(visual_plugin)
    visual_plugin.draw("example_1.svg")

if "build" in sys.argv:
    import os
    import shutil
    #compile into a xilinx device
    chip=make_chip("helo byd!\n", SerialOut)
    vhdl_plugin = chips_VHDL.Plugin(internal_reset=False, internal_clock=False)
    chip.write_code(vhdl_plugin)
    from_file=os.path.join(".", "ucfs", "example_1.ucf")
    to_file=os.path.join(".", "project", "xilinx", "project.ucf")
    shutil.copy(from_file, to_file)
    vhdl_plugin.xilinx_build("xc3s200-4-ft256")

if "test" in sys.argv:
    #capture output from serial port
    from serial import Serial
    port = Serial("/dev/ttyUSB0", baudrate=115200, bytesize=8, parity="N", stopbits=1)
    response = port.readline()
    response = port.readline()
    print response
    port.close()
