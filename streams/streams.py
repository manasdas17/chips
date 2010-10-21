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
from inspect import currentframe, getsourcefile
from collections import deque

from process import Process
from common import how_many_bits, Unique
from instruction import Write, Read
from exceptions import StreamsConstructionError

def resize(val, bits):
    mask_bits = (2**bits)-1
    return val | ~mask_bits if val < 0 else val & mask_bits

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

class System:
    """A Streams System

    A streams system is a container for data sources, data.receivers, and processes.
    Typically a System is used to describe a single device"""

    def __init__(self, sinks=(), processes=()):
       """Create a streams System

            Arguments:
              sinks              A sequence object listing all data.receivers"""

       self.sinks = sinks
       self.filename = getsourcefile(currentframe().f_back)
       self.lineno = currentframe().f_back.f_lineno

       #begin system enumeration process
       self.streams = []
       self.processes = []
       for i in self.sinks:
           i.set_system(self)

    def write_code(self, plugin):
        for i in self.streams:
            i.write_code(plugin)
        for i in self.processes:
            i.write_code(plugin)
        plugin.write_system(self)

    def reset(self):
        for i in self.processes:
            i.reset()
        for i in self.streams:
            i.reset()

    def execute(self, steps=1):
        for i in range(steps):
            for i in self.processes:
                i.execute()
            for i in self.sinks:
                i.execute()

    def test(self, name, stop_cycles=False):
        self.reset()
        try:
            self.execute(stop_cycles)
        except AssertionError:
            print name,
            print "...Fail"
            return True

        print name,
        print "...Pass"
        return True


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

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("Stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        if hasattr(self, "a"): self.a.set_system(system)
        if hasattr(self, "b"): self.b.set_system(system)

#streams sources
################################################################################

class Repeater(Stream, Unique):

    def __init__(self, value):
        self.value = value
        self.bits = how_many_bits(value)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_repeater(self)

    def __repr__(self):
        return "Repeater(value={0})".format(self.value) 

    def reset(self):
        pass

    def get(self):
        return self.value

class Counter(Stream, Unique):

    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop 
        self.step = step 
        self.bits = max((how_many_bits(start), how_many_bits(stop)))
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_counter(self)

    def reset(self):
        self.count = self.start

    def get(self):
        val = self.count
        if self.count == self.stop:
            self.count = self.start
        else:
            self.count += self.step
        return val

    def __repr__(self):
        return "Counter(start={0}, stop={1}, step={2})".format(self.start, self.stop, self.bits)

class Stimulus(Stream, Unique):

    def __init__(self, bits):
        self.bits = bits
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def get_bits(self): return self.bits

    def write_code(self, plugin): 
        plugin.write_stimulus(self)

    def reset(self):
        pass

    def get(self):
        return resize(self.queue.popleft(), self.bits)

    def set_simulation_data(self, iterator, plugin=None):
        if plugin is None:
            self.queue = deque(iterator)
        else:
            plugin.set_simulation_data(self, iterator)

    def __repr__(self):
        return "Stimulus({0})".format(self.name, self.bits)

class InPort(Stream, Unique):

    def __init__(self, name, bits):
        self.name, self.bits = name, bits
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def get_bits(self): return self.bits

    def write_code(self, plugin): 
        plugin.write_in_port(self)

    def reset(self):
        raise SimulationError("Inport ignored in native simulation")

    def get(self):
        raise SimulationError("Inport ignored in native simulation")

    def __repr__(self):
        return "InPort(name={0}, bits={1})".format(self.name, self.bits)

class SerialIn(Stream, Unique):

    def __init__(self, name="RX", clock_rate=50000000, baud_rate=115200):
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def get_bits(self): return 8

    def write_code(self, plugin): 
        plugin.write_serial_in(self)

    def reset(self):
        raise SimulationError("SerialIn ignored in native simulation")

    def get(self):
        raise SimulationError("SerialIn ignored in native simulation")

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


class Output(Stream, Unique):

    def __init__(self):
        """create a process output"""
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def set_system(self, system):
        Stream.set_system(self, system)
        if hasattr(self.process, "system"):
            if self.process.system is not system:
                raise StreamsConstructionError("process is allready part of another system", process.filename, process.lineno)
        self.process.set_system(system)

    def set_process(self, process):
        if hasattr(self, "process"):
            if self.process is not process:
                raise StreamsConstructionError("Output is allready part of a process", self.filename, self.lineno)
        self.process = process

    def write(self, variable): 
        """write an expression to the process output"""
        return Write(self, variable)

    def get_bits(self):
        return self.process.get_bits()

    def write_code(self, plugin): 
        pass
        #self.process.write_code(plugin)

    def reset(self):
        self.fifo=deque()

    def put(self, data):
        self.fifo.append(data)

    def get(self):
        try:
            return self.fifo.popleft()
        except IndexError:
            return None

    def __repr__(self):
        return "Output() at {0}".format(id(self))

#streams sinks
################################################################################

class Response(Unique):
    """A Response block allows data to be read from a stream in the python 
    design environment. A similar interface can be used in native python
    simulations and also co-simulations using external tools."""

    def __init__(self, a):
        self.a = a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_response(self)

    def reset(self):
        self.queue = deque()

    def execute(self):
        data = self.a.get()
        if data is not None:
            self.queue.append(data)

    def get_simulation_data(self, plugin=None):
        """Returns an iterator object representing the data output from this stream"""
        if plugin is None:
            return self.queue.__iter__()
        else:
            return plugin.get_simulation_data(self)

    def __repr__(self):
        return "Response({0}, self.sequence)".format(self.a)


class OutPort(Unique):

    def __init__(self, a, name):
        self.name, self.a = name, a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_out_port(self)

    def reset(self):
        pass

    def execute(self):
        self.a.get()

    def __repr__(self):
        return '\n'.join([
        "  out_port( name = ", 
        self.name, 
        ")"
        ])

class Asserter(Unique):

    def __init__(self, a):
        self.a = a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self
    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_asserter(self)

    def reset(self):
        pass

    def execute(self):
        val = self.a.get()
        if val is not None:
            assert val, "Python Streams Assertion failure file: {0} line: {1}".format(self.filename, self.lineno)

    def __repr__(self):
        return '\n'.join([
        "  asserter()", 
        ])

class DecimalPrinter(Unique):

    def __init__(self, a):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.a = a
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self
    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_decimal_printer(self)

    def reset(self):
        self.a.reset()

    def execute(self):
        val = self.a.get()
        if val is not None:
            print val

    def __repr__(self):
        return "DecimalPrinter"

class HexPrinter(Unique):

    def __init__(self, a):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.a = a
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_hex_printer(self)

    def reset(self):
        pass

    def execute(self):
        val = self.a.get()
        if val is not None:
            print hex(val)[2:]

    def __repr__(self):
        return "HexPrinter()"

class AsciiPrinter(Unique):

    def __init__(self, a):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.a = a
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_ascii_printer(self)

    def reset(self):
        self.string = []

    def execute(self):
        val = self.a.get()
        if val is not None:
            if val == 0:
                print ''.join(self.string)
                self.string = []
            else:
                self.string.append(chr(val&0xff))

    def __repr__(self):
        return "AsciiPrinter()"

class SerialOut(Unique):

    def __init__(self, a, name="TX", clock_rate=50000000, baud_rate=115200):
        self.a=a
        self.name = name
        self.clock_rate = clock_rate
        self.baud_rate = baud_rate
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        assert a.get_bits()==8
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_system(self, system):
        if hasattr(self, "system"):
            raise StreamsConstructionError("stream is allready part of a system", self.filename, self.lineno)
        self.system = system
        system.streams.append(self)
        self.a.set_system(system)

    def get_bits(self): 
        return a

    def write_code(self, plugin): 
        plugin.write_serial_out(self)

    def reset(self):
        pass

    def execute(self):
        self.a.get()

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


functions = {
    'add' : lambda a, b: a+b,
    'sub' : lambda a, b: a-b,
    'mul' : lambda a, b: a*b,
    'div' : lambda a, b: c_style_division(a, b),
    'mod' : lambda a, b: c_style_modulo(a, b),
    'and' : lambda a, b: a&b,
    'or'  : lambda a, b: a|b,
    'xor' : lambda a, b: a^b,
    'sl'  : lambda a, b: a<<b,
    'sr'  : lambda a, b: a>>b,
    'eq'  : lambda a, b: -int(a==b),
    'ne'  : lambda a, b: -int(a!=b),
    'lt'  : lambda a, b: -int(a<b),
    'le'  : lambda a, b: -int(a<=b),
    'gt'  : lambda a, b: -int(a>b),
    'ge'  : lambda a, b: -int(a>=b),
}
class  Binary(Stream, Unique):

    def __init__(self, a, b, function):
        self.a, self.b, self.function = a, b, function
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.function = function
        self.binary_function = functions[function]
        self.stored_a = None
        self.stored_b = None
        Unique.__init__(self)

        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

        if hasattr(self.b, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.b.receiver = self

    def get_bits(self):
        bit_function = {
        'add' : lambda x, y : max((x, y)) + 1,
        'sub' : lambda x, y : max((x, y)) + 1,
        'mul' : lambda x, y : x + y,
        'div' : lambda x, y : max((x, y)) + 1,
        'mod' : lambda x, y : max((x, y)),
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
        plugin.write_binary(self)

    def reset(self):
        pass

    def get(self):
        if self.stored_a is None:
            self.stored_a = self.a.get()
        if self.stored_b is None:
            self.stored_b = self.b.get()
        if self.stored_a is None:
            return None
        if self.stored_b is None:
            return None
        val = self.binary_function(self.stored_a, self.stored_b)
        self.stored_a = None
        self.stored_b = None
        return val

class Lookup(Stream, Unique):

    def __init__(self, source, *args):
        self.a = source
        self.args = [int(i) for i in args]
        self.bits = max((how_many_bits(i) for i in args))
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_lookup(self)

    def reset(self):
        self.a.reset()

    def get(self):
        val = self.a.get()
        if val is None: return None
        return self.args[resize(val, self.a.get_bits())]

class Resizer(Stream, Unique):

    def __init__(self, source, bits):
        self.a = source
        self.bits = bits
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_resizer(self)

    def reset(self):
        pass

    def get(self):
        val = self.a.get()
        if val is None: return None
        return resize(val, self.get_bits)

class DecimalFormatter(Stream, Unique):

    def __init__(self, source):
        self.a = source
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def get_bits(self): 
        return 8

    def get_num_digits(self):
        return len(str(2**(self.a.get_bits()-1)))

    def write_code(self, plugin): 
        plugin.write_decimal_formatter(self)

    def reset(self):
        self.string = []

    def get(self):
        if self.string:
            return ord(self.string.popleft())
        else:
            val = self.a.get()
            if val is None: return None
            self.string = deque(str(val))
            return ord(self.string.popleft())

class HexFormatter(Stream, Unique):

    def __init__(self, source):
        self.a = source
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def get_bits(self): 
        return 8

    def get_num_digits(self):
        return int((self.a.get_bits()-1)/4.0)

    def write_code(self, plugin): 
        plugin.write_hex_formatter(self)

    def reset(self):
        self.string = []

    def get(self):
        if self.string:
            return ord(self.string.popleft())
        else:
            val = self.a.get()
            if val is None: return None
            self.string = deque(hex(val)[2:])
            return ord(self.string.popleft())
