#!/usr/bin/env python

"""

Streams are a fundamental component of the *Chips* library.

A stream is used to represent a flow of data. A stream can act as a:
    * An input to a *Chip* such as an *InPort* or a *SerialIn*.  
    * A source of data in its own right such as a *Repeater* or a *Counter*. 
    * A means of performing some operation on a stream of data to form 
      another stream such as a *Printer* or a *Lookup*.
    * A means of transfering data from one process to another, an *Output*.

Stream Expressions
------------------

A Stream Expression can be formed by combining Streams or Stream Expressions
with the following ooperators::

	+, -, *, \/, %, &, |, ^, <<, >>, ==, !=, <, <=, >, >=

Each data item in the resulting Stream Expression will be evaluated by removing
a data item from each of the operand streams, and applying the operator
function to these data items.

Generaly speaking a Stream Expression will have enough bits to contain any
possible result without any arithmetic overflow. The one exception to this is
the left shift operator where the result is always truncated to the size of the
left hand operand. Stream expressions may be explicitly truncated or sign
extended using the *Resizer*.

If one of the operands of a binary operator is not a Stream, Python Streams
will attempt to convert this operand into an integer. If the conversion is
successfull, a *Repeater* stream will be created using the integer value. The
repeater stream will be used in place of the non-stream operand. This allows
constructs such as ``a = 47+InPort(12, 8)`` to be used as a shorthand for ``a =
Repeater(47)+InPort("in", 8)`` or ``count = Counter(1, 10, 1)+3*2`` to be used as
a shorthand for ``count = Counter(1, 10, 1)+Repeater(5)``.  Of course ``a=1+1``
still yields the integer 2 rather than a stream.

The operators provided in the Python Streams library are summarised in the
table below. The bit width field specifies how many bits are used for the
result based on the number of bits in the left and right hand operands.

+----------+-----------------------------------+-----------------------+
| Operator | Function                          | Data Width (bits)     |
+==========+===================================+=======================+
|   \+     | Signed Add                        | max(left, right) \+ 1 |
+----------+-----------------------------------+-----------------------+
|   \-     | Signed Subtract                   | max(left, right) \+ 1 |
+----------+-----------------------------------+-----------------------+
|   \*     | Signed Multiply                   | left \+ right         |
+----------+-----------------------------------+-----------------------+
|   //     | Signed Floor Division             | max(left, right) \+ 1 |
+----------+-----------------------------------+-----------------------+
|   %      | Signed Modulo                     | max(left, right)      |
+----------+-----------------------------------+-----------------------+
|   &      | Bitwise AND                       | max(left, right)      |
+----------+-----------------------------------+-----------------------+
|   \|     | Bitwise OR                        | max(left, right)      |
+----------+-----------------------------------+-----------------------+
|   ^      | Bitwise XOR                       | max(left, right)      |
+----------+-----------------------------------+-----------------------+
|   <<     | Arithmetic Left Shift             | left                  |
+----------+-----------------------------------+-----------------------+
|   >>     | Arithmetic Right Shift            | left                  |
+----------+-----------------------------------+-----------------------+
|   ==     | Equality Comparison               | 1                     |
+----------+-----------------------------------+-----------------------+
|   !=     | Inequality Comparison             | 1                     |
+----------+-----------------------------------+-----------------------+
|   <      | Signed Less Than                  | 1                     |
|          | Comparison                        |                       |
+----------+-----------------------------------+-----------------------+
|   <=     | Signed Less Than or Equal         | 1                     |
|          | Comparison                        |                       |
+----------+-----------------------------------+-----------------------+
|   >      | Signed Greater Than               | 1                     |
|          | Comparison                        |                       |
+----------+-----------------------------------+-----------------------+
|   >=     | Signed Greater Than               | 1                     |
|          | Comparison                        |                       |
+----------+-----------------------------------+-----------------------+

Operator Precedence
-------------------

The operator precedence is inherited from the python language. The following
table summarizes the operator precedences, from lowest precedence (least
binding) to highest precedence (most binding). Operators in the same row have
the same precedence.

+----------------------+-------------------------------------+
|  Operator            | Description                         |
+======================+=====================================+
| ==, !=, <, <=, >, >= | Comparisons                         | 
+----------------------+-------------------------------------+
| |                    | Bitwise OR                          |
+----------------------+-------------------------------------+
| ^                    | Bitwise XOR                         | 
+----------------------+-------------------------------------+
| &                    | Bitwise AND                         | 
+----------------------+-------------------------------------+
| <<, >>               | Shifts                              |
+----------------------+-------------------------------------+
| +, -                 | Addition and subtraction            | 
+----------------------+-------------------------------------+
| *, //, %             | multiplication, division and modulo |
+----------------------+-------------------------------------+

"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintatiner__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from math import log
from inspect import currentframe, getsourcefile
from sys import stdout
from collections import deque

from process import Process
from common import how_many_bits, Unique, resize, c_style_modulo, c_style_division
from instruction import Write, Read
from exceptions import StreamsConstructionError, SimulationError

class Chip:
    """
    A Chip device containing streams, sinks and processes.

    Typically a Chip is used to describe a single device. You need to provide
    the Chip object with a list of all the sinks (devie outputs). You don't
    need to include any process, variables or streams. By analysing the sinks,
    the chip can work out which processes and streams need to be included in
    the device.
    
    Example::

        switches = InPort("SWITCHES", 8)
        serial_in = SerialIn("RX")
        leds = OutPort(switches, "LEDS")
        serial_out = SerialOut("TX", serial_in)

        #We need to tell the *Chip* that *leds* and *serial_out* are part of
        #the device. The *Chip* can work out for itself that *switches* and
        #*serial_in* are part of the device.

        s = Chip(
            leds,
            serial_out,
        )

        s.write_code(plugin)
        
    """

    def __init__(self, *args):
       """Create a streams Chip

       Arguments:
         sinks - A sequence object listing all data.receivers"""

       self.sinks = list(args)
       self.filename = getsourcefile(currentframe().f_back)
       self.lineno = currentframe().f_back.f_lineno

       #begin chip enumeration process
       self.streams = []
       self.processes = []
       self.executables = []
       for i in self.sinks:
           i.set_chip(self)

    def write_code(self, plugin):
        """Write source code for the streams chips using the specified plugin

        Arguments:
          plugin - A code generation plugin such as streams_vhdl.plugin()"""

        for i in self.streams:
            i.write_code(plugin)
        for i in self.processes:
            i.write_code(plugin)
        plugin.write_chip(self)

    def reset(self):
        """Reset the chip to its intial state.

        A chip must be reset before it can be executed."""

        for i in self.processes:
            i.reset()
        for i in self.streams:
            i.reset()

    def execute(self, steps=1):
        """Execute a native simulation

        Arguments:
          steps - specify the number of execution steps to run"""

        for i in range(steps):
            for i in self.processes:
                i.execute()
            for i in self.executables:
                i.execute()
            for i in self.sinks:
                i.execute()

    def test(self, name, stop_cycles=False):
        """Perform a test
       
        Resets, and executes the chip for specified number of cycles.

        Arguments:
          name        - a test name that will be reported
          stop_cycles - the number of cycles to execute for

        Returns:
          True  - if no assertions occur during execution
          False - if assertions occur"""

        self.reset()
        try:
            self.execute(stop_cycles)
        except AssertionError:
            print name,
            print "...Fail"
            return False

        print name,
        print "...Pass"
        return True


    def __repr__(self):
        return "Chip(sinks={0})".format(self.sinks)

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
    def get_type(self):
        return "integer"
    def read(self, variable, timout=0):
        return Read(self, variable)

    def set_chip(self, chip):
        if hasattr(self, "chip"):
            raise StreamsConstructionError("Stream is allready part of a chip", self.filename, self.lineno)
        self.chip = chip
        chip.streams.append(self)
        if hasattr(self, "a"): self.a.set_chip(chip)
        if hasattr(self, "b"): self.b.set_chip(chip)
        if hasattr(self, "c"): self.c.set_chip(chip)

#streams sources
################################################################################

class Repeater(Stream, Unique):
    """

    A stream which repeatedly yields the specified *value*.

    The *Repeater* stream is one of the most fundamental streams available. 

    The width of the stream in bits is calculated automatically. The smallest
    number of bits that can represent *value* in twos-complement format will be
    used.

    Examples::
        
        Repeater(5) #--> 5 5 5 5 \..
        #creates a 4 bit stream.

        Repeater(10) #--> 10 10 10 10 \..
        #creates a 5 bit stream.

        Repeater(5)*2 #--> 10 10 10 10 \..
        #This is shothand for: Repeater(5)*Repeater(2)

    """

    def __init__(self, value):
        """A Stream which repeatedly outputs a constant value.

        Arguments:
          value - a constant value to be output"""

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
    """
    
    A Stream which yields numbers from *start* to *stop* in *step* increments.

    A *Counter* is a versatile, and commonly used construct in device design,
    they can be used to number samples, index memories and so on.

    Example::

        Counter(0, 10, 2) # --> 0 2 4 6 8 10 0 \..

        Counter(10, 0, -2) # --> 10 8 7 6 4 2 0 10 \..
    
    
    """

    def __init__(self, start, stop, step):
        """A Stream which repeatedly outputs a constant value.

        Arguments:
          start - initial count value that will be output
          stop  - the last count value that will be output before wrapping
                  round to zero
          step  - the count step size"""

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
    """
    
    A Stream that allows a Python iterable to be used as a stream.
    
    A Simulus stream allows a transparent method to pass data from the Python
    envrinment into the simulation environment. The sequence object is set at
    run time using the set_simulation_data() method. The sequence object can be
    any iterable Python sequence such as a list, tuple, or even a generator.

    Example:: 

        import PIL

        picture = Stimulus()
        s = Chip(Console(Printer(picture)))

        im = PIL.open("test.bmp")
        image_data = list(im.getdata())
        picture.set_simulation_data(image_data)

        picture.reset()
        picture.execute(1000)
    
    """

    def __init__(self, bits):
        """A Stream that allows a sequence object to be used as simulation stimulus
        
        A source sequence should be set prior to simulation using the 
        Stimulus.set_simulation_data() method.

            arguments:
              bits - The resolution in bits of the stream"""

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
    """
    
    A device input port stream.

    An *InPort* allows a port pins of the target device to be used as a data
    stream.  There is no handshaking on the input port. The port pins are
    sampled at the point when data is transfered by the stream.  When
    implemented in VHDL, the *InPort* provides double registers on the port
    pins to synchronise data to the local clock domain.

    Since it is not possible to determine the width of the strean in bits
    automatically, this must be specified using the *bits* argument.

    The *name* parameter allows a string to be associated with the input port.
    In a VHDL implementation, *name* will be used as the port name in the
    top level entity.

    Example::

        dip_switches = Inport("dip_switches", 8) 
        s = Chip(SerialOut(Printer(dip_switches)))
    
    """

    def __init__(self, name, bits):
        """A Stream of data obtained from input port pins
        
        A source sequence should be set prior to simulation using the 
        Stimulus.set_simulation_data() method.

            arguments:
              name - A for the port.
                     The name will be prepended with OUT_in the component
                     entity.
              bits - The resolution in bits of the stream"""

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
    """
    
    A *SerialIn* yields 8-bit data from a serial uart input.
    

    
    """

    def __init__(self, name="RX", clock_rate=50000000, baud_rate=115200):
        """A Stream of data obtained from input port pins
        
        A source sequence should be set prior to simulation using the 
        Stimulus.set_simulation_data() method.

            arguments:
              name - A for the port.
                     The name will be prepended with OUT_in the component
                     entity.
              bits - The resolution in bits of the stream"""

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

    def set_chip(self, chip):
        if hasattr(self.process, "chip"):
            if self.process.chip is not chip:
                raise StreamsConstructionError("Process is allready part of another Chip", process.filename, process.lineno)
        self.process.set_chip(chip)
        Stream.set_chip(self, chip)

    def set_process(self, process):
        if hasattr(self, "process"):
            if self.process is not process:
                raise StreamsConstructionError("Output is allready part of a Process", self.filename, self.lineno)
        self.process = process

    def write(self, variable): 
        """write an expression to the process output"""
        return Write(self, variable)

    def get_bits(self):
        return self.process.get_bits()

    def write_code(self, plugin): 
        plugin.write_output(self)

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

class ExternalIPDefinition:
    def __init__(self, 
            name,
            dependencies,
            input_streams, 
            output_streams, 
            input_ports,
            output_ports):
        self.name = name
        self.dependencies = dependencies
        self.input_streams = input_streams
        self.output_streams = output_streams
        self.input_ports = input_ports
        self.output_ports = output_ports

class ExternalIPInstance(Unique):
    def __init__(self, input_streams, definition, inport_mapping, outport_mapping):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.input_streams = input_streams
        self.definition = definition
        self.output_streams = [ExternalIPStream(self, bits) for name, bits in self.definition.output_streams.iteritems()]
        self.inport_mapping = inport_mapping
        self.outport_mapping = outport_mapping

        for i in self.input_streams:
            if hasattr(i, "receiver"):
                raise StreamsConstructionError("stream allready has receiver", self.filename, self.lineno)
            else:
                i.receiver = self

        no_streams_expected = len(self.definition.input_streams)
        no_streams_actual = len(self.input_streams)
        if no_streams_expected != no_streams_actual:
            raise StreamsConstructionError("External IP expects: {0} input streams, actual: {1}".format(
                no_streams_expected, no_streams_actual), self.filename, self.lineno)

        expected_sizes = self.definition.input_streams.values()
        print expected_sizes
        for stream, expected_size in zip(self.input_streams, expected_sizes):
            if expected_size != stream.get_bits():
                raise StreamsConstructionError("incorrect bit width, expected: {0} actual: {1}".format(
                    expected_size, stream.get_bits()), self.filename, self.lineno)

        Unique.__init__(self)

    def set_system(self, system):
        #this should only get called if the IP is added to a system
        #ie. it is acting as a sink.
        if self.output_streams:
            raise StreamsConstructionError("only data sinks can be added to systems", self.filename, self.lineno)

        for i in self.input_streams:
            i.set_system(system)
        system.streams.append(self)

    def get_output_streams(self):
        return self.output_streams

    def write_code(self, plugin):
        plugin.write_external_ip(self)

    def write_input_code(self, output_stream, plugin):
        if output_stream is self.output_streams[0]:
            plugin.write_external_ip(self)

class ExternalIPStream(Stream, Unique):

    def __init__(self, instance, bits):
        """Do not call this manually, ExternalIPStream is
        automatically created by ExternalIPInstance"""
        self.instance = instance
        self.bits = bits
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)

    def set_chip(self, chip):

        if hasattr(self, "chip"):
            raise StreamsConstructionError("stream is allready part of a chip", self.filename, self.lineno)
        else:
            self.chip = chip
            chip.streams.append(self)

        if self is self.instance.output_streams[0]: 
            for i in self.instance.input_streams:
                i.set_chip(chip)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        self.instance.write_input_code(self, plugin)

    def reset(self):
        raise SimulationError("external ip cannot be natively simulated", self.filename, self.lineno)

    def get(self):
        raise SimulationError("external ip cannot be natively simulated", self.filename, self.lineno)

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
        'sl'  : lambda x, y : x,
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
        return resize(val, self.get_bits())

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
        if resize(val, self.a.get_bits()) > len(self.args)-1:
            print self.filename, 
            print self.lineno
            print val
            raise SimulationError("lookup index too large", self.filename, self.lineno)
        if resize(val, self.a.get_bits()) < 0:
            print self.filename, 
            print self.lineno
            raise SimulationError("negative lookup index", self.filename, self.lineno)
        return self.args[resize(val, self.a.get_bits())]

class Fifo(Stream, Unique):

    def __init__(self, data_in, depth):
        self.a = data_in
        self.depth = depth
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("address_in allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_chip(self, chip):
        Stream.set_chip(self, chip)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_fifo(self)

    def reset(self):
        self.a.reset()

    def get(self):
        return self.a.get()

class Array(Stream, Unique):

    def __init__(self, address_in, data_in, address_out, depth):
        self.a = address_in
        self.b = data_in
        self.c = address_out
        self.depth = depth
        self.memory = {}
        self.stored_a = None
        self.stored_b = None
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        Unique.__init__(self)
        if hasattr(self.a, "receiver"):
            raise StreamsConstructionError("address_in allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self
        if hasattr(self.b, "receiver"):
            raise StreamsConstructionError("data_in allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self
        if hasattr(self.c, "receiver"):
            raise StreamsConstructionError("address_out allready has receiver", self.filename, self.lineno)
        else:
            self.a.receiver = self

    def set_chip(self, chip): # a RAM behaves a a sink for data and address in
        chip.executables.append(self)
        Stream.set_chip(self, chip)

    def get_bits(self): 
        return self.b.get_bits()

    def write_code(self, plugin): 
        plugin.write_array(self)

    def reset(self):
        self.a.reset()
        self.b.reset()
        self.c.reset()

    def execute(self):
        if self.stored_a is None:
            self.stored_a = self.a.get()
        if self.stored_b is None:
            self.stored_b = self.b.get()
        if self.stored_a is None:
            return None
        if self.stored_b is None:
            return None
        self.memory[self.stored_a] = self.stored_b
        self.stored_a = None
        self.stored_b = None

    def get(self):
        address_out = self.c.get()
        if address_out is None:
            return None
        return self.memory[address_out]

class Decoupler(Stream, Unique):

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
        return self.a.get_bits()

    def write_code(self, plugin): 
        plugin.write_decoupler(self)

    def reset(self):
        self.a.reset()

    def get(self):
        return self.a.get()

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
        return resize(val, self.get_bits())

class Printer(Stream, Unique):

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
        plugin.write_printer(self)

    def reset(self):
        self.string = []

    def get(self):
        if self.string:
            return ord(self.string.popleft())
        else:
            val = self.a.get()
            if val is None: return None
            self.string = deque(str(val)+'\n')
            return ord(self.string.popleft())

class HexPrinter(Stream, Unique):

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
        maxval = 2**(self.a.get_bits()-1)
        digits = len(hex(maxval)[2:])
        return digits

    def write_code(self, plugin): 
        plugin.write_hex_printer(self)

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
