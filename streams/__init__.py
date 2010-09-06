import itertools
import primitives

#SOURCES
InPort = primitives.InPort
Repeater = primitives.Repeater
Counter = primitives.Counter

def Sequence(bits, *args):
    return Lookup(Counter(0, len(args)-1, 1), bits, *args)

#SINKS
Printer = primitives.Printer
Asserter = primitives.Asserter
OutPort = primitives.OutPort

#COMBINATORS
Switch = primitives.Switch
Clone = primitives.Clone
Lookup = primitives.Lookup

def Rotate(*args):
    return Switch(Counter(0, len(args)-1, 1), *args)
