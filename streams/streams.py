#!/usr/bin/env python

"""Primitive Operations for Streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from math import log

from process import Process
from common import Unique, Stream

class System:

    def __init__(self):
       self.sinks = []
       self.sources = []
       self.processes = []

    def repeater(self, value): 
        source =  Repeater(value)
        self.sources.append(source)
        return source

    def counter(self, first, last, step): 
        source =  Counter(first, last, step)
        self.sources.append(source)
        return source

    def in_port(self, name, bits=8): 
        source =  Counter(first, last, step)
        self.sources.append(source)
        return source

    def serial_in(self, name): 
        source =  SerialIn(name)
        self.sources.append(source)
        return source

    def process(self, bits):
        p = Process(bits)
        self.processes.append(p)
        return p

    def printer(self, stream):
        p = Printer(stream)
        self.sinks.append(p)

    def asserter(self, stream): 
        a = Asserter(stream)
        self.sinks.append(a)

    def out_port(self, stream, name):
        o = OutPort(stream, name)
        self.sinks.append(o)

    def serial_out(self, stream, name):
        s = SerialOut(stream, name)
        self.sinks.append(s)

    def write_code(self, plugin): 
        for i in self.sinks:
            i.write_code(plugin)
        for i in self.processes:
            i.write_code(plugin)
        plugin.write_system()

    def __repr__(self):
        return '\n'.join([
"SYSTEM",
"======",
"",
"sources",
"------",
'\n'.join((i.__repr__() for i in self.sources)),
"",
"sinks",
"------",
'\n'.join((i.__repr__() for i in self.sinks)),
"",
"processes",
"------",
'\n'.join((i.__repr__() for i in self.processes))
        ])

#streams sources
################################################################################

class Repeater(Stream, Unique):

    def __init__(self, value):
        self.value = value
        self.bits = how_many_bits(value)
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_repeater(self)

    def __repr__(self):
        return '\n'.join([
        "  repeater( value = ", 
        self.value, 
        ")"
        ])

class Counter(Stream, Unique):

    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop 
        self.step = step 
        self.bits = max((how_many_bits(start), how_many_bits(stop)))
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_counter(self)

    def __repr__(self):
        return '\n'.join([
        "  counter( start = ", 
        self.start, 
        "stop = ", 
        self.stop, 
        "step = ", 
        self.step, 
        ")"
        ])

class InPort(Stream, Unique):

    def __init__(self, name, bits):
        self.name, self.bits = name, bits
        Unique.__init__(self)

    def get_bits(self): return self.bits

    def write_code(self, plugin): 
        plugin.write_in_port(self)

    def __repr__(self):
        return '\n'.join([
        "  in_port( name = ", 
        self.name, 
        "bits = ", 
        self.bits, 
        ")"
        ])

class SerialIn(Stream, Unique):

    def __init__(self, name="RX", clock_rate=50000000, baud_rate=115200):
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        Unique.__init__(self)

    def get_bits(self): return 8

    def write_code(self, plugin): 
        plugin.write_serial_in(self)

    def __repr__(self):
        return '\n'.join([
        "  serial_in( name = ", 
        self.name, 
        "clock_rate = ", 
        self.clock_rate, 
        "baud_rate", 
        self.baud_rate, 
        ")"
        ])

#streams sinks
################################################################################
class OutPort(Unique):

    def __init__(self, a, name):
        self.name, self.a = name, a
        Unique.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_out_port(self)

    def __repr__(self):
        return '\n'.join([
        "  out_port( name = ", 
        self.name, 
        ")"
        ])

class Asserter(Unique):

    def __init__(self, a):
        self.a = a
        Unique.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_asserter(self)

    def __repr__(self):
        return '\n'.join([
        "  asserter()", 
        ])

class Printer(Unique):

    def __init__(self, a):
        self.a = a
        Unique.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_printer(self)

    def __repr__(self):
        return '\n'.join([
        "  printer()", 
        ])

class SerialOut(Unique):

    def __init__(self, a, name="TX", clock_rate=50000000, baud_rate=115200):
        self.a=a
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        assert a.get_bits()==8
        Unique.__init__(self)

    def get_bits(self): 
        return a

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_serial_out(self)

    def __repr__(self):
        return '\n'.join([
        "  serial_out( name = ", 
        self.name, 
        "clock_rate = ", 
        self.clock_rate, 
        "baud_rate", 
        self.baud_rate, 
        ")"
        ])

#streams combinators
################################################################################
class _Spawn(Stream, Unique):

    def __init__(self, clone):
        self.clone = clone
        Unique.__init__(self)

    def get_bits(self):
        return self.clone.a.get_bits()

    def write_code(self, plugin): 
        self.clone._write_code(self, plugin)

class Clone:

    def __init__(self, a):
        self.a = a
        self._spawn = []

    def spawn(self):
        _spawn = _Spawn(self)
        self._spawn.append(_spawn)
        return _spawn

    def _write_code(self, spawn, plugin):
        if spawn is self._spawn[0]:
            self.a.write_code(plugin)
            plugin.write_clone(self)

class Switch(Stream, Unique):

    def __init__(self, select, *args):
        self.select = select
        self.a = args
        Unique.__init__(self)

    def get_bits(self): 
        return max((i.get_bits() for i in self.a))

    def write_code(self, plugin): 
        for i in self.a:
            i.write_code(plugin)
        self.select.write_code(plugin)
        plugin.write_switch(self)

class Lookup(Stream, Unique):

    def __init__(self, source, *args):
        self.a = source
        self.args = args
        self.bits = max((how_many_bits(i) for i in args))
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_lookup(self)

class Resizer(Stream, Unique):

    def __init__(self, source, bits):
        self.a = source
        self.bits = bits
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_resizer(self)

class Formater(Stream, Unique):

    def __init__(self, source):
        self.a = source
        Unique.__init__(self)

    def get_bits(self): 
        return 8

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_formater(self)

def how_many_bits(num):
    if num > 0 :
        return int(log(num, 2)) + 2
    elif num < -1:
        return int(log(abs(num)-1, 2)) + 2
    else:
        return 1
