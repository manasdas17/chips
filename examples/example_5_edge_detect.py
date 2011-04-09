#!/usr/bin/env python

"""Example 7 apply an edge detection filter to a greyscale image

Options are:

simulate      - native python simulation
simulate_vhdl - simulate using ghdl cosimulation
build         - compile onto a Xilinx FPGA
test          - hardware-in-loop test using serial port """


from math import pi, sin
import sys

from PIL import Image

from chips import *
from chips_VHDL import Plugin

#define a few fixed point routines
################################################################################
im = Image.open("test.bmp")
image_data = list(im.getdata())
width, height = im.size
                
#chips version of edge detection routine
################################################################################

def edge_detector(image):
    new_image = Output()
    im = VariableArray(width*3)

    def get_x_y(x,y):
        return Evaluate(
            If(x<0, Value(0)),
            If(x>=width, Value(0)),
            Value(im.read(x+(y*width)))
        )

    i = Variable(0)
    j = Variable(0)
    p = Variable(0)

    p = Process(13,

        #read image into memory
        i.set(0),#above
        While(i < width,
            im.write((width*2)+i, 0),
            i.set(i+1),
        ),

        i.set(0),#this
        While(i < width,
            image.read(p),
            im.write((width*1)+i, p),
            i.set(i+1),
        ),

        i.set(0),#below
        While(i < width,
            image.read(p),
            im.write(i, p),
            i.set(i+1),
        ),

        #filter image
        j.set(0),
        While(j < height,

            i.set(0),
            While(i < width,
                p.set(get_x_y(i, 1)),
                p.set(p-(get_x_y(i-1, 2)>>3)),
                p.set(p-(get_x_y(i-1, 1)>>3)),
                p.set(p-(get_x_y(i-1, 0)>>3)),
                p.set(p-(get_x_y(i,   2)>>3)),
                p.set(p-(get_x_y(i,   0)>>3)),
                p.set(p-(get_x_y(i+1, 2)>>3)),
                p.set(p-(get_x_y(i+1, 1)>>3)),
                p.set(p-(get_x_y(i+1, 0)>>3)),
                new_image.write(p),
                i.set(i+1),
            ),

            i.set(0),
            While(i < width,#above
                im.write((width*2)+i, im.read(width+i)),
                i.set(i+1),
            ),

            i.set(0),#this
            While(i < width,
                im.write(width+i, im.read(i)),
                i.set(i+1),
            ),

            i.set(0),#below
            While(i < width,
                If(j < (height-1),
                    image.read(p),
                ).ElsIf(-1,
                    p.set(0),
                ),
                im.write(i, p),
                i.set(i+1),
            ),

            j.set(j+1),
        ),
    )
    return new_image

if "python" in sys.argv:
    new_image = []

    def get_x_y(x, y):
        if x < 0: return 0
        if x >= width : return 0
        if y < 0: return 0
        if y >= height : return 0
        return image_data[x + y*width]

    for j in range(height):
        for i in range(width):
            pixel = get_x_y(i,j)*1
            pixel = pixel - get_x_y(i-1,j-1)//8
            pixel = pixel - get_x_y(i-1,j)//8
            pixel = pixel - get_x_y(i-1,j+1)//8
            pixel = pixel - get_x_y(i,j-1)//8
            pixel = pixel - get_x_y(i,j+1)//8
            pixel = pixel - get_x_y(i+1,j-1)//8
            pixel = pixel - get_x_y(i+1,j)//8
            pixel = pixel - get_x_y(i+1,j+1)//8
            new_image.append(pixel)

    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show()
        
if "simulate" in sys.argv:
    response = Response(edge_detector(Sequence(*image_data)))
    chip = Chip(response)
    chip.reset()
    chip.execute(10000000)
    new_image = list(response.get_simulation_data())
    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show()

if "simulate_vhdl" in sys.argv:
    from chips.VHDL_plugin import Plugin
    response = Response(edge_detector(Sequence(*image_data)))
    chip = Chip(response)
    plugin = Plugin()
    chip.write_code(plugin)
    plugin.ghdl_test("edge_detect", stop_cycles=10000000)
    new_image = list(response.get_simulation_data(plugin))
    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show()

if "simulate_cpp" in sys.argv:
    from chips.cpp_plugin import Plugin
    response = Response(edge_detector(Sequence(*image_data)))
    chip = Chip(response)
    plugin = Plugin()
    chip.write_code(plugin)
    plugin.test("edge_detect", stop_cycles=10000000)
    new_image = list(response.get_simulation_data(plugin))
    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show()

if "build" in sys.argv:
    from chips.VHDL_plugin import Plugin
    import os
    import shutil
    response = SerialOut(Printer(edge_detector(Scanner(SerialIn(baud_rate=460800), 9))), baud_rate=460800)
    chip = Chip(response)
    plugin = Plugin(internal_clock=False, internal_reset=False)
    chip.write_code(plugin)
    from_file=os.path.join(".", "ucfs", "example_7.ucf")
    to_file=os.path.join(".", "project", "xilinx", "project.ucf")
    shutil.copy(from_file, to_file)
    plugin.xilinx_build("xc3s200-4-ft256")

if "test" in sys.argv:
    from serial import Serial
    from collections import deque
    image_data = deque(image_data)
    new_image = []

    port = Serial("/dev/ttyUSB0", 460800)
    port.open()

    for i in range(width):
        port.write("{0}\n".format(image_data.popleft()))

    for i in range(width):
        port.write("{0}\n".format(image_data.popleft()))

    for j in range(height-2):
        for i in range(width):
            new_image.append(int(port.readline())),
        for i in range(width):
            port.write("{0}\n".format(image_data.popleft()))
        sys.stdout.write("{0}%\r".format(100*j//height))
        sys.stdout.flush()

    for j in range(1):
        for i in range(width):
            new_image.append(int(port.readline())),
        sys.stdout.write("100%\r")
        sys.stdout.flush()

    new_im = Image.new(im.mode, (width, height))
    new_im.putdata(new_image)
    im.show()
    new_im.show()
