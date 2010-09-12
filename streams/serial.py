#!/usr/bin/env python

"""Provides Serial Sources and Sinks for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from primitives import Stream

class SerialIn(Stream):

    def __init__(self, name="RX", clock_rate=50000000, baud_rate=115200):
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        Stream.__init__(self)

    def get_bits(self): return 8

    def write_code(self, plugin): 
        plugin.write_serial_in(self)

    def generator(self): 
        raise Exception()

#streams sinks
################################################################################
class SerialOut(Stream):

    def __init__(self, a, name="TX", clock_rate=50000000, baud_rate=115200):
        self.a=a
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        assert a.get_bits()==8
        Stream.__init__(self)

    def get_bits(self): 
        return a

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_serial_out(self)

    def generator(self): 
        raise Exception()
