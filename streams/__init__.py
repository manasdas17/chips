"""A Stream based concurrent programming library for embedded systems"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import streams, process, instruction

System = streams.System
Process = process.Process

#COMBINATORS
Lookup = streams.Lookup
Decoupler = streams.Decoupler
Resizer = streams.Resizer
DecimalFormatter = streams.DecimalFormatter
HexFormatter = streams.HexFormatter

#SOURCES
InPort = streams.InPort
SerialIn = streams.SerialIn
Counter = streams.Counter
Repeater = streams.Repeater
Stimulus = streams.Stimulus

#SINKS
Response = streams.Response
OutPort = streams.OutPort
SerialOut = streams.SerialOut
SVGA = streams.SVGA
DecimalPrinter = streams.DecimalPrinter
HexPrinter = streams.HexPrinter
AsciiPrinter = streams.AsciiPrinter
Asserter = streams.Asserter

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
        
class PrintDecimal(instruction.UserDefinedStatement):

    variables={}

    def __init__(self, stream, exp, minimum_number_of_digits=None):
        self.stream = stream
        self.exp = exp

        self.minimum_number_of_digits = minimum_number_of_digits

    def on_execute(self):

        #Need to reference different variables in different processes
        if id(self.process) in PrintDecimal.variables:
            leading, decade, digit, count = PrintDecimal.variables[id(self.process)]
        else:
            decade = Variable(0)
            digit = Variable(0)
            count = Variable(0)
            leading = Variable(0)
            PrintDecimal.variables[id(self.process)] = leading, decade, digit, count

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
            count.set(self.exp),
            decade.set(initial_decade),
            leading.set(0),
            While(0 < decade,
                digit.set(0),
                While(count >= decade,
                    count.set(count-decade),
                    digit.set(digit+1),
                ),
                If(digit!=0 | decade==minimum_decade, leading.set(-1)),
                If(leading, self.stream.write(0x30|digit)),
                decade.set(decade//10),
            ),
            self.stream.write(0x0),
        )

class DecimalScan(instruction.UserDefinedStatement):

    variables={}

    def __init__(self, stream, variable):
        self.stream = stream
        self.variable = variable

    def on_execute(self):

        #Need to reference different variables in different processes
        if id(self.process) in DecimalScan.variables:
            digit, count = DecimalScan.variables[id(self.process)]
        else:
            digit = Variable(0)
            count = Variable(0)
            DecimalScan.variables[id(self.process)] = digit, count

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
                ).ElsIf(1, 
                    Break(),
                ),
            ),
            self.variable.set(count),
        )
