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
    return Lookup(Counter(0, len(args)-1, 1), *args)

#synthesised instructions
def While(condition, *instructions):
    loop_instructions = (If(condition==0, Break()),)+instructions
    return Loop(*loop_instructions)

def DoWhile(condition, *instructions):
    loop_instructions = instructions+(If(condition==0, Break()),)
    return Loop(*loop_instructions)

def Until(condition, *instructions):
    loop_instructions = (If(condition!=0, Break()),)+instructions
    return Loop(*loop_instructions)

def DoUntil(condition, *instructions):
    loop_instructions = instructions+(If(condition!=0, Break()),)
    return Loop(*loop_instructions)

def Not(thing):
    """Not(thing) is a nicer way of saying thing.Not()"""
    return thing.Not()

class Print(instruction.UserDefinedStatement):

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

        #decade of minumum number of digits
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
