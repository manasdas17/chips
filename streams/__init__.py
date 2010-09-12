"""A Stream based concurrent programming library for embedded systems"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import itertools
import primitives
import serial

#SOURCES
InPort = primitives.InPort
Repeater = primitives.Repeater
Counter = primitives.Counter
SerialIn = serial.SerialIn

def Sequence(bits, *args):
    return Lookup(Counter(0, len(args)-1, 1), bits, *args)

#SINKS
Printer = primitives.Printer
Asserter = primitives.Asserter
OutPort = primitives.OutPort
SerialOut = serial.SerialOut

#COMBINATORS
Switch = primitives.Switch
Clone = primitives.Clone
Lookup = primitives.Lookup
Resizer = primitives.Resizer
Formater = primitives.Formater

def Rotate(*args):
    return Switch(Counter(0, len(args)-1, 1), *args)
