#!/usr/bin/env python
import sys

from streams import * #use the streams library
from streams_visual import Plugin#import VHDL plugin 

a = Repeater(10)
b = Repeater(20)
c = Repeater(30)
z = a*b+c*Repeater(40)
var = Variable(0)
d = Output()
e = Output()
f = Output()
g = Output()

Process(8,
  z.read(var),
  d.write(var),
  e.write(var),
  f.write(var),
  g.read(var),
)

varb = Variable(0)
Process(8,
  f.read(varb),
  g.write(varb),
)

system = System(Console(d), SerialOut(e))
visual_plugin = Plugin()
system.write_code(visual_plugin)
visual_plugin.draw("test.svg")
