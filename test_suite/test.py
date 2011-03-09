#!/usr/bin/env python

from streams import *
import streams_cpp 

system = System(Console(Printer(Repeater(1))))

p = streams_cpp.Plugin()
system.write_code(p)
good = p.test("test", stop_cycles=10)
