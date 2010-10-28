#!/usr/bin/env python
from streams import *
from streams_VHDL import Plugin


svga_stream = Output()
push_buttons=InPort(name="PB", bits=2)
pressed = Variable(0)
hours = Variable(0)
minutes = Variable(0)
seconds = Variable(0)
ms = Variable(0)
us = Variable(0)

Process(16,
    #reads the time from the serial port at power on
    Loop(
        While(hours < 24,
            While(minutes < 60,
                While(seconds < 60,
                    #every minute the time is updated
                    PrintDecimal(svga_stream, hours, 2),
                    svga_stream.write(ord(":")),
                    PrintDecimal(svga_stream, minutes, 2),
                    svga_stream.write(ord(":")),
                    PrintDecimal(svga_stream, seconds, 2),
                    svga_stream.write(ord("\r")),
                    push_buttons.read(pressed), 
                    If(pressed&1, minutes.set(minutes+1)),
                    If(pressed&2, hours.set(hours+1)),
                    While(ms < 1000,
                        While(us < 1000,
                            WaitUs(),
                            us.set(us + 1),
                        ),
                        us.set(0),
                        ms.set(ms + 1),
                    ),
                    ms.set(0),
                    seconds.set(seconds + 1),
                ),
                seconds.set(0),
                minutes.set(minutes + 1),
            ),
            minutes.set(0),
            hours.set(hours + 1),
        ),
        hours.set(0),
    ),
)

svga_out = Output()
char = Variable(0)
col = Variable(0)
row = Variable(0)
Process(8,
    Loop(
        While(row < 75,
            While(col < 100,
                svga_stream.read(char),
                If(char==ord("\r"), 
                    col.set(0), 
                ).ElsIf(char ==ord("\n"),
                    row.set(row+1),
                    If(row==75, row.set(0)),
                ).ElsIf(1,
                    svga_out.write(col),
                    svga_out.write(row),
                    svga_out.write(char),
                    col.set(col+1),
                ),
            ),
            col.set(0),
            row.set(row + 1),
        ),
        row.set(0),
    ),
)



#s = System(AsciiPrinter(serialout))
#s.reset()
#s.execute(1000)
s = System(SVGA(svga_out))
p = Plugin(internal_clock=False, internal_reset=False)
s.write_code(p)
p.xilinx_build(part="xc3s200-4-ft256")
#p = Plugin()
#s.write_code(p)
#p.ghdl_test("test svga", stop_cycles = 10000, generate_wave=True)
