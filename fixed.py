#!/usr/bin/env python
from streams import *

default_fraction_bits = 8

class FixedPointError(Exception):
    """Error in FixedPointInstruction"""

    def __init__(self, message):
       self.message = message 

def constantize(potential_constant, fraction_bits=default_fraction_bits):
    if hasattr(potential_constant, "fraction_bits") and hasattr(potential_constant, "expression"):
        return potential_constant
    else:
        return FixedConstant(potential_constant, default_fraction_bits)

class FixedStream:
    def __init__(self, stream, fraction_bits):
        self.stream = stream
        self.fraction_bits = fraction_bits

    def read(self, fixedvariable):
        return self.stream.read(fixedvariable.expression)

operations = {
        "add":lambda a,b,fb : a+b,
        "sub":lambda a,b,fb : a-b,
        "mul":lambda a,b,fb : (a*b)>>fb,
        "div":lambda a,b,fb : (a//b)<<fb,
        "lshift":lambda a,b,fb : (a)<<(b>>fb),
        "rshift":lambda a,b,fb : (a)>>(b>>fb),
}

class FixedExpression:
    def __add__(self, other): return FixedBinary("add", self, other)
    def __sub__(self, other): return FixedBinary("sub", self, other)
    def __mul__(self, other): return FixedBinary("mul", self, other)
    def __div__(self, other): return FixedBinary("div", self, other)
    def __lshift__(self, other): return FixedBinary("lshift", self, other)
    def __rshift__(self, other): return FixedBinary("rshift", self, other)
    def __radd__(self, other): return FixedBinary("add", other, self)
    def __rsub__(self, other): return FixedBinary("sub", other, self)
    def __rmul__(self, other): return FixedBinary("mul", other, self)
    def __rdiv__(self, other): return FixedBinary("div", other, self)
    def __rlshift__(self, other): return FixedBinary("lshift", other, self)
    def __rrshift__(self, other): return FixedBinary("rshift", other, self)
    def __gt__(self, other): return self.expression > constantize(other).expression
    def __ge__(self, other): return self.expression >= constantize(other).expression
    def __lt__(self, other): return self.expression < constantize(other).expression
    def __le__(self, other): return self.expression <= constantize(other).expression
    def __eq__(self, other): return self.expression == constantize(other).expression
    def __ne__(self, other): return self.expression != constantize(other).expression
    def __rgt__(other, self): return constantize(other).expression >  self.expression
    def __rge__(other, self): return constantize(other).expression >= self.expression
    def __rlt__(other, self): return constantize(other).expression <  self.expression
    def __rle__(other, self): return constantize(other).expression <= self.expression
    def __req__(other, self): return constantize(other).expression == self.expression
    def __rne__(other, self): return constantize(other).expression != self.expression
    def to_integer(self): return self.expression >> self.fraction_bits

class ToFixed(FixedExpression):
    def __init__(self, integerexpression, fraction_bits = default_fraction_bits):
        self.expression = integerexpression << fraction_bits
        self.fraction_bits = fraction_bits
        self.instructions = tuple()

class FixedBinary(FixedExpression):
    def __init__(self, operation, left, right):

        left = constantize(left)
        right = constantize(right)

        if not hasattr(left, "expression"): raise FixedPointError("not a fixed point expression")
        if not hasattr(left, "fraction_bits"): raise FixedPointError("not a fixed point object")
        if not hasattr(right, "expression"): raise FixedPointError("not a fixed point expression")
        if not hasattr(right, "fraction_bits"): raise FixedPointError("not a fixed point object")
        if left.fraction_bits != right.fraction_bits: raise FixedPointError("incompatible radix point")

        self.fraction_bits = left.fraction_bits
        self.instructions = left.instructions+right.instructions
        self.expression = operations[operation](left.expression, right.expression, self.fraction_bits)


class FixedOutput(FixedStream):
    def __init__(self, fraction_bits=default_fraction_bits):
        self.stream = Output()
        self.fraction_bits = fraction_bits

    def write(self, fixedexpression):
        fixedexpression=constantize(fixedexpression, self.fraction_bits)
        return Block((
            Block(fixedexpression.instructions),
            self.stream.write(fixedexpression.expression)
        ))

class FixedRepeater(FixedStream):
    def __init__(self, fraction_bits, value):
        self.stream = Repeater(int(value*(2**fraction_bits)))
        self.fraction_bits = fraction_bits

class Fixed(FixedExpression):
    def __init__(self, value, fraction_bits=default_fraction_bits):
        self.instructions = tuple()
        self.expression = Variable(int(value*(2**fraction_bits)))
        self.fraction_bits = fraction_bits

    def set(self, fixedexpression):
        fixedexpression=constantize(fixedexpression, self.fraction_bits)
        return Block((
            Block(fixedexpression.instructions),
            self.expression.set(fixedexpression.expression)
        ))

class FixedConstant(FixedExpression):
    def __init__(self, value, fraction_bits=default_fraction_bits):
        self.instructions = tuple()
        try:
            self.expression = Constant(int(value*(2**fraction_bits)))
        except AttributeError:
            raise FixedPointError("Cannot interpret as fixed point expression")

        self.fraction_bits = fraction_bits

class Function:
    def __init__(self, arguments=tuple(), output=tuple(), instructions=tuple()):
        self.arguments = arguments
        self.output = output
        self.instructions = instructions

    def __call__(self, *values):  
        instructions = tuple((a.set(v) for a, v in zip(self.arguments, values)))+self.instructions
        if hasattr(self.output, "instructions"):
            self.output.instructions = instructions
            return self.output
        else:
            return Evaluate(Block((instructions)), Value(self.output))

Integer = Variable



if __name__ == "__main__":

    import streams_python
    import streams_VHDL

    z = Output()
    a=Process(32,
       z.write(FixedConstant(1)==1), #256
       z.write(FixedConstant(0.5)==0.5), #128
       z.write(FixedConstant(-1)==-1), #-256
       z.write(FixedConstant(-0.5)==-0.5), #-128
       z.write((FixedConstant(1))+1==2), #512
       z.write((FixedConstant(1))-1==0), #0
       z.write((FixedConstant(1))*1==1), #256
       z.write((FixedConstant(1))*0.5==0.5), #128
       z.write((FixedConstant(1))>>2==0.25), #64
    )

    s=System(( Asserter(z), ))

    simulation_plugin = streams_python.Plugin()
    s.write_code(simulation_plugin)
    simulation_plugin.python_test("fixed test python", stop_cycles=1000)

    simulation_plugin = streams_VHDL.Plugin()
    s.write_code(simulation_plugin)
    simulation_plugin.ghdl_test("fixed test VHDL", stop_cycles=1000)

    from math import atan, degrees, sqrt, radians
    from math import sin, pi
    #scale degrees so that 0=0 and 1=360
    sin_values = []
    for i in range(256):
        sin_values.append(sin(i*radians(90)/255)*255)
    print sin_values

    

    z = Output()

    theta = Fixed(0)
    result = Fixed(0)

    a=Process(32,
       theta.set(radians(90)),
       sin(theta, result),
       z.write(result.expression),
    )

    s=System(
        (
            DecimalPrinter(z), 
        )
    )

    simulation_plugin = streams_python.Plugin()
    s.write_code(simulation_plugin)
    simulation_plugin.python_test("fixed test ", stop_cycles=1000)

    simulation_plugin = streams_VHDL.Plugin()
    s.write_code(simulation_plugin)
    simulation_plugin.ghdl_test("fixed test ", stop_cycles=1000)

