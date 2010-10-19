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
Resizer = streams.Resizer
DecimalFormatter = streams.DecimalFormatter
HexFormatter = streams.HexFormatter

#SOURCES
InPort = streams.InPort
SerialIn = streams.SerialIn
Counter = streams.Counter
Repeater = streams.Repeater

#SINKS
OutPort = streams.OutPort
SerialOut = streams.SerialOut
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
Wait = instruction.Wait
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
