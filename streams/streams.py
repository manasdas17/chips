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
from common import how_many_bits, Unique
from instruction import Write, Read

class System:
    """A Streams System

    A streams system is a container for data sources, data sinks, and processes.
    Typically a System is used to describe a single device"""

    def __init__(self, sinks=(), processes=()):
       """Create a streams System

            Arguments:
              sinks              A sequence object listing all data sinks"""

       self.sinks = sinks

    def write_code(self, plugin):
        for i in self.sinks:
            i.write_code(plugin)

    def __repr__(self):
        return "System(sinks={0})".format(self.sinks)

# Stream Classes
################################################################################

class Stream:

    def __add__(self, other): return Binary(self, repeaterize(other), 'add')
    def __sub__(self, other): return Binary(self, repeaterize(other), 'sub')
    def __mul__(self, other): return Binary(self, repeaterize(other), 'mul')
    def __mod__(self, other): return Binary(self, repeaterize(other), 'mod')
    def __floordiv__(self, other): return Binary(self, repeaterize(other), 'div')
    def __and__(self, other): return Binary(self, repeaterize(other), 'and')
    def __or__(self, other): return Binary(self, repeaterize(other), 'or')
    def __xor__(self, other): return Binary(self, repeaterize(other), 'xor')
    def __rshift__(self, other): return Binary(self, repeaterize(other), 'sr')
    def __lshift__(self, other): return Binary(self, repeaterize(other), 'sl')
    def __eq__(self, other): return Binary(self, repeaterize(other), 'eq')
    def __ne__(self, other): return Binary(self, repeaterize(other), 'ne')
    def __gt__(self, other): return Binary(self, repeaterize(other), 'gt')
    def __ge__(self, other): return Binary(self, repeaterize(other), 'ge')
    def __lt__(self, other): return Binary(self, repeaterize(other), 'lt')
    def __le__(self, other): return Binary(self, repeaterize(other), 'le')
    def __radd__(other, self): return Binary(self, repeaterize(other), 'add')
    def __rsub__(other, self): return Binary(self, repeaterize(other), 'sub')
    def __rmul__(other, self): return Binary(self, repeaterize(other), 'mul')
    def __rmod__(other, self): return Binary(self, repeaterize(other), 'mod')
    def __rfloordiv__(other, self): return Binary(self, repeaterize(other), 'div')
    def __rand__(other, self): return Binary(self, repeaterize(other), 'and')
    def __ror__(other, self): return Binary(self, repeaterize(other), 'or')
    def __rxor__(other, self): return Binary(self, repeaterize(other), 'xor')
    def __rrshift__(other, self): return Binary(self, repeaterize(other), 'sr')
    def __rlshift__(other, self): return Binary(self, repeaterize(other), 'sl')
    def __req__(other, self): return Binary(self, repeaterize(other), 'eq')
    def __rne__(other, self): return Binary(self, repeaterize(other), 'ne')
    def __rgt__(other, self): return Binary(self, repeaterize(other), 'gt')
    def __rge__(other, self): return Binary(self, repeaterize(other), 'ge')
    def __rlt__(other, self): return Binary(self, repeaterize(other), 'lt')
    def __rle__(other, self): return Binary(self, repeaterize(other), 'le')
    def read(self, variable):
        return Read(self, variable)

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
        return "Repeater(value={0})".format(self.value) 

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
        return "Counter(start={0}, stop={1}, step={2})".format(self.start, self.stop, self.bits)

class InPort(Stream, Unique):

    def __init__(self, name, bits):
        self.name, self.bits = name, bits
        Unique.__init__(self)

    def get_bits(self): return self.bits

    def write_code(self, plugin): 
        plugin.write_in_port(self)

    def __repr__(self):
        return "InPort(name={0}, bits={1})".format(self.name, self.bits)

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

class Output(Stream, Unique):

    def __init__(self):
        """create a process output"""
        Unique.__init__(self)

    def write(self, variable): 
        """write an expression to the process output"""
        return Write(self, variable)

    def get_bits(self):
        return self.process.get_bits()

    def set_process(self, process):
        self.process = process

    def write_code(self, plugin): 
        self.process.write_code(plugin)

    def __repr__(self):
        return "Output() at {0}".format(id(self))

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

def repeaterize(potential_repeater):
    if hasattr(potential_repeater, "write_code"):
        return potential_repeater
    else:
        return Repeater(int(potential_repeater))



class  Binary(Stream, Unique):

    def __init__(self, a, b, function):
        self.a, self.b, self.function = a, b, function
        Unique.__init__(self)

    def get_bits(self):
        bit_function = {
        'add' : lambda x, y : max((x, y)) + 1,
        'sub' : lambda x, y : max((x, y)) + 1,
        'mul' : lambda x, y : x + y,
        'div' : lambda x, y : max((x, y)) + 1,
        'and' : lambda x, y : max((x, y)),
        'or'  : lambda x, y : max((x, y)),
        'xor' : lambda x, y : max((x, y)),
        'sl'  : lambda x, y : x+((2**(y-1))-1),
        'sr'  : lambda x, y : x,
        'eq'  : lambda x, y : 1,
        'ne'  : lambda x, y : 1,
        'lt'  : lambda x, y : 1,
        'le'  : lambda x, y : 1,
        'gt'  : lambda x, y : 1,
        'ge'  : lambda x, y : 1,
        }
        return bit_function[self.function](self.a.get_bits(), self.b.get_bits())

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        self.b.write_code(plugin)
        plugin.write_binary(self)
class _Spawn(Stream, Unique):

    def __init__(self, clone):
        self.clone = clone
        Unique.__init__(self)

    def get_bits(self):
        return self.clone.a.get_bits()

    def write_code(self, plugin): 
        self.clone._write_code(self, plugin)

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
