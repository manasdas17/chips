"""
Sinks are a fundamental component of the *Chips* library.

A sink is used to terminate a stream. A sink may act as:
    * An output of a *Chip* such as an *OutPort* or *SerialOut*.  
    * A consumer of data in its own right such as an *Asserter*. 

"""

from math import log
from inspect import currentframe, getsourcefile
from sys import stdout
from collections import deque

from process import Process
from common import how_many_bits, Unique, resize, c_style_modulo,\
    c_style_division
from instruction import Write, Read
from exceptions import StreamsConstructionError, SimulationError

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

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
            raise StreamsConstructionError(
                "stream already has receiver", 
                self.filename,
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError(
                "stream is already part of a chip", 
                self.filename, 
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

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
            raise StreamsConstructionError(
                "stream already has receiver", 
                self.filename,
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError(
                "stream is already part of a chip", 
                self.filename, 
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

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
            raise StreamsConstructionError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError(
                "stream is already part of a chip", 
                self.filename, 
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

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

class Asserter(Unique):

    def __init__(self, a):
        self.a = a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self
    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError(
                "stream is already part of a chip", 
                self.filename, 
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_asserter(self)

    def reset(self):
        pass

    def execute(self):
        val = self.a.get()
        if val is not None:
            assert val,\
            "Python Streams Assertion failure file: {0} line: {1}".format(
                self.filename, 
                self.lineno
            )

    def __repr__(self):
        return '\n'.join([
        "  asserter()", 
        ])

class Console(Unique):

    def __init__(self, a):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.a = a
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError(
                "stream is already part of a chip", 
                self.filename,
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_console(self)

    def reset(self):
        self.string = []

    def execute(self):
        val = self.a.get()
        if val is not None:
            if chr(val&0xff)=='\n':
                stdout.write(''.join(self.string))
                stdout.write("\n")
                self.string = []
            else:
                self.string.append(chr(val&0xff))

    def __repr__(self):
        return "Console()"
