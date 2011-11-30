"""
Sinks are a fundamental component of the *Chips* library.

A sink is used to terminate a stream. A sink may act as:
    * An output of a *Chip* such as an *OutPort* or *SerialOut*.  
    * A consumer of data in its own right such as an *Asserter*. 

"""

from math import log
from inspect import currentframe, getsourcefile
import sys
from collections import deque

from process import Process
from common import how_many_bits, Unique, resize, c_style_modulo,\
    c_style_division
from instruction import Write, Read
from chips_exceptions import ChipsSyntaxError, ChipsSimulationError

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

class Response(Unique):
    """
   
    A *Response* sink allows data to be transfered into Python.

    As a simulation is run, the *Response* sink accumulates data. After a
    simulation is run, you can retrieve a python iterable using the
    get_simulation_data method. Using a *Response* sink allows you to
    seamlessly integrate your *Chips* simulation into a wider Python
    simulation. This works for simulations using an external simulator as well,
    in this case you also need to pass the code generation plugin to
    get_simulation_data. 

    A *Response* sink accepts a single stream argument as its source.

    Example::

        >>> from streams import *
        >>> import PIL.Image #You need the Python Imaging Library for this

        >>> def image_processor():
        ...    #black -> white
        ...    return Counter(0, 63, 1)*4

        >>> response = Response(image_processor())
        >>> chip = Chip(response)

        >>> chip.reset()
        >>> chip.execute(100000)

        >>> image_data = list(response.get_simulation_data())
        >>> image_data = image_data[:(64*64)-1]
        >>> im = PIL.Image.new("L", (64, 64))
        >>> im.putdata(image_data)
        >>> im.show()
    
    """

    def __init__(self, a):
        self.a = a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise ChipsSyntaxError(
                "stream already has receiver", 
                self.filename,
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise ChipsSyntaxError(
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
    """

    An *OutPort* sink outputs a stream of data to I/O port pins.

    No handshaking is performed on the output port, data will appear at the
    time when the source stream transfers data.

    An output port take two arguments, the source stream *a* and a string
    *name*. Name is used as the port name in generated VHDL.

    Example::

        >>> from chips import *
        >>> dip_switches = InPort("dip_switches", 8) 
        >>> led_array = OutPort(dip_switches, "led_array")
        >>> s = Chip(led_array)

    """

    def __init__(self, a, name):
        self.name, self.a = name, a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise ChipsSyntaxError(
                "stream already has receiver", 
                self.filename,
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise ChipsSyntaxError(
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
    """

    A *SerialOut* outputs data to a serial UART port.

    *SerialOut* outputs one character to the serial output port for each item
    of data in the source stream. At present only 8 data bits are supported, so
    the source stream must be 8 bits wide. The source stream could be truncated
    to 8 bits using a *Resizer*, but it is usually more convenient to use a
    *Printer* as the source stream. The will allow a stream of any width to be
    represented as a decimal string.

    A SerialOut accepts a source stream argument *a*. An optional *name*
    argument is used as the name for the serial TX line in generated VHDL. The
    clock rate of the target device in MHz can be specified using the
    *clock_rate* argument. The baud rate of the serial output can be specified
    using the *baud_rate* argument.

    Example::

        >>> from chips import *

        >>> #convert string into a sequence of characters
        >>> hello_world = map(ord, \"hello world\\n\")

        >>> my_chip = Chip(
        ...     SerialOut(
        ...         Sequence(*hello_world),
        ...     )
        ... )

    """

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
            raise ChipsSyntaxError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise ChipsSyntaxError(
                "stream is already part of a chip", 
                self.filename, 
                self.lineno
            )
        self.chip = chip
        chip.streams.append(self)
        self.a.set_chip(chip)

    def get_bits(self): 
        return 8

    def write_code(self, plugin): 
        plugin.write_serial_out(self)

    def reset(self):
        pass

    def execute(self):
        self.a.get()

    def __repr__(self):
        return '\n'.join([
            "  SerialOut( name = ", 
            self.name, 
            "clock_rate = ", 
            self.clock_rate, 
            "baud_rate", 
            self.baud_rate, 
            ")"
        ])

class Asserter(Unique):
    """

    An *Asserter* causes an exception if any data in the source stream is zero.

    An *Asserter* is particularly useful in automated tests, as it causes a
    simulation to fail is a condition is not met. In generated VHDL code, an
    asserter is represented by a VHDL assert statement. In practice this means
    that an *Asserter* will function correctly in a VHDL simulation, but will
    have no effect when synthesized.

    The *Asserter* sink accepts a source stream argument, *a*.

    Example::

        >>> from chips import *
        >>> a = Sequence(1, 2, 3, 4)
        >>> c = Chip(Asserter((a+1) == Sequence(2, 3, 4, 5)))

    Look at the Chips test suite for more examples of the Asserter being used
    for automated testing.

    """

    def __init__(self, a):
        self.a = a
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise ChipsSyntaxError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self
    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise ChipsSyntaxError(
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
        "  Asserter()", 
        ])

class Console(Unique):
    """

    A *Console* outputs data to the simulation console.

    *Console* stores characters for output to the console in a buffer. When an
    end of line character is seen, the buffer is written to the console.  A
    *Console* interprets a stream of numbers as ASCII characters. The source
    stream must be 8 bits wide. The source stream could be truncated to 8 bits
    using a *Resizer*, but it is usually more convenient to use a *Printer* as
    the source stream. The will allow a stream of any width to be represented
    as a decimal string.

    A *Console* accepts a source stream argument *a*.

    Example::

        >>> from chips import *

        >>> #convert string into a sequence of characters
        >>> hello_world = tuple((ord(i) for i in \"hello world\\n\"))

        >>> my_chip = Chip(
        ...     Console(
        ...         Sequence(*hello_world),
        ...     )
        ... )

    """

    def __init__(self, a):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.a = a
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise ChipsSyntaxError(
                "stream already has receiver", 
                self.filename, 
                self.lineno
            )
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise ChipsSyntaxError(
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
                sys.stdout.write(''.join(self.string))
                sys.stdout.write("\n")
                self.string = []
            else:
                self.string.append(chr(val&0xff))

    def __repr__(self):
        return "Console()"
