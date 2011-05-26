#!/usr/bin/env python
"""A simple test of graphviz based visuaisation plugin"""

import sys

from chips import *
from chips.visual_plugin import Plugin

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.2"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

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

chip = Chip(Console(d), SerialOut(e))
visual_plugin = Plugin()
chip.write_code(visual_plugin)
visual_plugin.draw("test.svg")
