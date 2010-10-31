#!/usr/bin/env python
from streams import *
from streams_VHDL import Plugin

hours = Variable(0)
minutes = Variable(0)
seconds = Variable(0)
ms = Variable(0)
us = Variable(0)

serialin = SerialIn()
serialout = Output()

def StringPrint(stream, string):
    return Block(tuple((stream.write(ord(i)) for i in string)))

Process(16,
    StringPrint(serialout, "Enter time hours:\r\n"),
    Scan(serialin, hours),
    StringPrint(serialout, "Enter time minutes:\r\n"),
    Scan(serialin, minutes),
    #reads the time from the serial port at power on
    Loop(
        While(hours < 24,
            While(minutes < 60,
                While(seconds < 60,
                    #every minute the time is updated
                    Print(serialout, hours, 2),
                    serialout.write(ord(":")),
                    Print(serialout, minutes, 2),
                    serialout.write(ord(":")),
                    Print(serialout, seconds, 2),
                    serialout.write(ord("\r")),
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

#s = System(AsciiPrinter(serialout))
#s.reset()
#s.execute(1000)
s = System(SerialOut(Resizer(serialout, 8)))
p = Plugin(internal_clock=False, internal_reset=False)
s.write_code(p)
p.xilinx_build(part="xc3s200-4-ft256")
