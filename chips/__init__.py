"""*Chips* is a python library for designing digital ICs."""

import streams, sinks, process, instruction

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


Chip = streams.Chip
Process = process.Process

#COMBINATORS
Lookup = streams.Lookup
Array = streams.Array
Fifo = streams.Fifo
Decoupler = streams.Decoupler
Resizer = streams.Resizer
Printer = streams.Printer
HexPrinter = streams.HexPrinter

#SOURCES
InPort = streams.InPort
SerialIn = streams.SerialIn
Counter = streams.Counter
Repeater = streams.Repeater
Stimulus = streams.Stimulus

#SINKS
Response = sinks.Response
OutPort = sinks.OutPort
SerialOut = sinks.SerialOut
Console = sinks.Console
Asserter = sinks.Asserter

#PROCESS INSTRUCTIONS
Output = streams.Output #also a source
Loop = instruction.Loop
Variable = instruction.Variable
Constant = instruction.Constant
Break = instruction.Break
Continue = instruction.Continue
If = instruction.If
Block = instruction.Block
WaitUs = instruction.WaitUs
Evaluate = instruction.Evaluate
Value = instruction.Value

#EXTERNAL IP INTERFACE
ExternalIPDefinition = streams.ExternalIPDefinition
ExternalIPInstance = streams.ExternalIPInstance

#synthesised streams
def Sequence(*args):
    """A *Sequence* stream yields each of its arguments in turn repeatedly.

    A *Sequence* accepts any number of arguments. The bit width of a sequence
    is determined automatically, using the number of bits necessary to
    represent the argument with the largest magnitude. A *Sequence* allows
    Python sequences to be used within a Chips simulation using the
    ``Sequence(*python_sequence)`` syntax.
    
    Example::

        >>> print "blah"
        
        >>> from chips import *

        >>> c = Chip(
        ...     Console(
        ...         Sequence(*map(ord, "hello world\\n")),
        ...     )
        ... )

        >>> c.reset()
        >>> c.execute(50)
        hello world
        hello world
        hello world
        hello world
    
    """
    return Lookup(Counter(0, len(args)-1, 1), *args)

#synthesised instructions
def While(condition, *instructions):
#    """A loop in which one iteration will be executed each time the condition
#    is true. The condition is tested before each loop iteration.
#    
#    Equivalent to::
#
#        Loop( 
#            If(Not(condition), Break()),
#            instructions,
#        ) 
#    
#    """
    loop_instructions = (If(Not(condition), Break()),)+instructions
    return Loop(*loop_instructions)

def DoWhile(condition, *instructions):
#    """A loop in which one iteration will be executed each time the condition
#    is true. The condition is tested after each loop iteration.
#    
#    Equivalent to::
#
#        Loop( 
#            instructions,
#            If(Not(condition), Break()),
#        ) 
#    
#    """
    loop_instructions = instructions+(If(Not(condition), Break()),)
    return Loop(*loop_instructions)

def Until(condition, *instructions):
#    """A loop in which one iteration will be executed each time the condition
#    is false. The condition is tested before each loop iteration.
#    
#    Equivalent to::
#
#        Loop( 
#            If(condition, Break()),
#            instructions,
#        ) 
#    
#    """
    loop_instructions = (If(condition, Break()),)+instructions
    return Loop(*loop_instructions)

def DoUntil(condition, *instructions):
#    """A loop in which one iteration will be executed each time the condition
#    is false. The condition is tested after each loop iteration.
#    
#    Equivalent to::
#
#        Loop( 
#            instructions,
#            If(condition, Break()),
#        ) 
#    
#    """
    loop_instructions = instructions+(If(condition, Break()),)
    return Loop(*loop_instructions)

def Not(thing):
#    """Not(thing) is a nicer way of saying thing.Not()"""
    return thing.Not()

class Print(instruction.UserDefinedStatement):
#    """The *Print* instruction write an integer to a stream in decimal ASCII
#    format.
#
#    Print will not add any white space or line ends (in contrast to the
#    *Printer*) The *Print* instruction accepts two arguments, the destination
#    *stream*, which must be an *Output* stream, and a numeric expression,
#    *exp*. An optional third argument specifies the minimum number of digits to
#    print (leading 0 characters are added).
#
#    Example:: 
#    
#        >>> #multiply by 2 and echo
#        >>> temp = Variable(0)
#        >>> inp = Sequence(*map(ord, "1 2 3 "))
#        >>> out_stream = Output()
#        >>> p=Process(8,
#        ...     Loop(
#        ...         Scan(inp, temp),
#        ...         out_stream.write(temp*2),
#        ...     )
#        ... )
#
#        >>> c = Chip(Console(Printer(out_stream)))
#        >>> c.reset()
#        >>> c.execute(1000)
#        
#    """

    variables={}

    def __init__(self, stream, exp, minimum_number_of_digits=None):
        self.stream = stream
        self.exp = exp

        self.minimum_number_of_digits = minimum_number_of_digits

    def on_execute(self):

        #Need to reference different variables in different processes
        if id(self.process) in Print.variables:
            leading, decade, digit, count, sign = Print.variables[id(self.process)]
        else:
            decade = Variable(0)
            digit = Variable(0)
            sign = Variable(0)
            count = Variable(0)
            leading = Variable(0)
            Print.variables[id(self.process)] = leading, decade, digit, count, sign

        #calculate number of digits
        bits = self.process.bits
        num_digits = len(str(2**(bits-1)))
        initial_decade = 10**(num_digits-1)

        #decade of minimum number of digits
        if self.minimum_number_of_digits is not None:
            minimum_decade = 10**(self.minimum_number_of_digits-1)
        else:
            minimum_decade = 0
            
        return (
            If(self.exp < 0,
                self.stream.write(ord("-")),
                count.set(0-self.exp),
            ).Elif(1,
                count.set(self.exp),
            ),
            decade.set(initial_decade),
            leading.set(0),
            While(decade,
                digit.set(0),
                While(count >= decade,
                    count.set(count-decade),
                    digit.set(digit+1),
                ),
                If((digit!=0) | (decade==minimum_decade), leading.set(-1)),
                If(leading, self.stream.write(0x30|digit)),
                decade.set(decade//10),
            ),
            self.stream.write(0x0),
        )

class Scan(instruction.UserDefinedStatement):
#    """The *Scan* instruction reads an integer value from a stream of decimal
#    ASCII characters.
#
#    Numeric characters separated by non-numeric characters are interpreted as
#    numbers. If *Scan* encounters a number that is too large to represent in a
#    process, the result is undefined.
#    
#    The *Scan* accepts two arguments, the source stream and a destination variable.
#
#    Example:: 
#
#        >>> from chips import *
#
#        >>> #multiply by 2 and echo
#        >>> temp = Variable(0)
#        >>> inp = Sequence(*map(ord, "1 2 3 "))
#        >>> out = Output()
#        >>> p=Process(8,
#        ...     Loop(
#        ...         Scan(inp, temp),
#        ...         out.write(temp*2),
#        ...     )
#        ... )
#
#        >>> c = Chip(Console(Printer(out)))
#        >>> c.reset()
#        >>> c.execute(1000) # doctest: +ELLIPSIS
#        2
#        4
#        6
#        ...
#        
#    """

    variables={}

    def __init__(self, stream, variable):
        self.stream = stream
        self.variable = variable

    def on_execute(self):

        #Need to reference different variables in different processes
        if id(self.process) in Scan.variables:
            digit, count = Scan.variables[id(self.process)]
        else:
            digit = Variable(0)
            count = Variable(0)
            Scan.variables[id(self.process)] = digit, count

        return (
            #read first digit
            self.stream.read(digit),
            While((digit < 0x30) | (digit > 0x39),
                self.stream.read(digit),
            ),
            count.set(digit & 0xf),
            #read other digits
            Loop(
                self.stream.read(digit),
                If((digit >= 0x30) & (digit <= 0x39),
                    count.set(count*10),
                    count.set(count+(digit & 0xf)),
                ).Elif(1, 
                    Break(),
                ),
            ),
            self.variable.set(count),
        )

def Scanner(stream, bits):
#    """A *Scanner* converts a stream of decimal ASCII into their integer value.
#
#    Numeric characters separated by non-numeric characters are interpreted as
#    numbers.  As it is not possible to determine the maximum value of a
#    *Scanner* stream at compile time, the width of the stream must be specified
#    using the bits parameter.
#    
#    The *Scanner* stream accepts two inputs, the source stream and the number
#    of bits.
#
#    Example:: 
#    
#        >>> from chips import *
#
#        >>> #multiply by two and echo
#        >>> c = Chip(
#        ...     Console(
#        ...         Printer(
#        ...             Scanner(Sequence(*map(ord, "10 20 30 ")), 8)*2,
#        ...         ),
#        ...     ),
#        ... )
#
#        >>> c.reset()
#        >>> c.execute(1000) # doctest: +ELLIPSIS
#        20
#        40
#        60
#        20
#        ...
#        
#    """

    i=Variable(0)
    out=Output()
    Process(bits,
        Loop(
            Scan(stream, i),
            out.write(i),
        )
    )

    return out

class VariableArray:
#    """A *VariableArray* is an array of variables that can be accessed from
#    within a single *Process*.
#
#    When a *VariableArray* is created, it accepts a single argument, the
#    *size*.
#    
#    A *VariableArray* can be written to using the *write* method, the *write*
#    method accepts two arguments, an expression indicating the *address* to
#    write to, and an expression indicating the *data* to write. 
#
#    A *VariableArray* can be read to using the *read* method, the *read* method
#    accepts a single argument, an expression indicating the *address* to read
#    from. The *read method returns an expression that evaluates to the value
#    contained at *address*.
#
#    Example:: 
#
#        >>> from chips import *
#
#        >>> def reverse(stream, number_of_items):
#        ...      \"\"\"Read number_of_items from stream, and reverse them.\"\"\"
#        ...      temp = Variable(0)
#        ...      index = Variable(0)
#        ...      reversed_stream = Output()
#        ...      data_store = VariableArray(number_of_items)
#        ...      Process(8,
#        ...          index.set(0),
#        ...          While(index < number_of_items,
#        ...              stream.read(temp),
#        ...              data_store.write(index, temp),
#        ...              index.set(index+1),
#        ...          ),
#        ...          index.set(number_of_items - 1),
#        ...          While(index >= 0,
#        ...              reversed_stream.write(data_store.read(index)),
#        ...              index.set(index-1),
#        ...          ),
#        ...      )
#        ... 
#        ...      return reversed_stream
#
#            
#        >>> c = Chip(
#        ...     Console(
#        ...         Printer(
#        ...             reverse(Sequence(0, 1, 2, 3), 4)
#        ...         ),
#        ...      ),
#        ... )
#
#        >>> c.reset()
#
#        >>> c.execute(1000)
#        3
#        2
#        1
#        0
#        
#    """
    def __init__(self, size):
        self.size = size
        self.address_in = Output()
        self.data_in = Output()
        self.address_out = Output()
        self.temp = Variable(0)
        self.data_out = Array(self.address_in, self.data_in, self.address_out, size)
    def write(self, address, data):
        return Block((
            self.address_in.write(address), 
            self.data_in.write(data),
        ))
    def read(self, address):
        return Evaluate(
                self.address_out.write(address), 
                self.data_out.read(self.temp),
                Value(self.temp),
        )
    def __len__(self):
        return self.size
