#!/usr/bin/env python

from chips import *
import chips_cpp 

chip = Chip(Console(Printer(Repeater(1))))

p = chips_cpp.Plugin()
system.write_code(p)
good = p.test("test", stop_cycles=10)
