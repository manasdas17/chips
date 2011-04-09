#!/usr/bin/env python
"""test file"""

from chips import *
import chips_cpp 

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

chip = Chip(Console(Printer(Repeater(1))))

p = chips_cpp.Plugin()
system.write_code(p)
good = p.test("test", stop_cycles=10)
