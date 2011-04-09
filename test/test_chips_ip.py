#!/usr/bin/env python
"""Test that ip can be generated and compiled without error."""

from chips import *
from chips.VHDL_plugin import Plugin
import chips.ip

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


s = Chip(Console(chips.ip.PS2Keyboard()))
p = Plugin()
s.write_code(p)
p.ghdl_test("test keyboard", stop_cycles=100)

