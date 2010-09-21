"""A Stream based concurrent programming library for embedded systems"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

import streams, process

System = streams.System

#COMBINATORS
Lookup = streams.Lookup
Resizer = streams.Resizer
Formater = streams.Formater

#flow controllers
Switch = streams.Switch
Clone = streams.Clone

#process instructions
Output = process.Output
Loop = process.Loop
Variable = process.Variable
Break = process.Break
If = process.If
