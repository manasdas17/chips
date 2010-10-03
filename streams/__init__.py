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
Formater = streams.Formater

#SOURCES
InPort = streams.InPort
SerialIn = streams.SerialIn
Counter = streams.Counter
Repeater = streams.Repeater

#SINKS
OutPort = streams.OutPort
SerialOut = streams.SerialOut
Printer = streams.Printer
Asserter = streams.Asserter

#PROCESS INSTRUCTIONS
Output = streams.Output #also a source
Loop = instruction.Loop
Variable = instruction.Variable
Break = instruction.Break
Continue = instruction.Continue
If = instruction.If
Block = instruction.Block
Wait = instruction.Wait
