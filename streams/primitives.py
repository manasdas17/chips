#!/usr/bin/env python
import itertools


#IMPLEMENTED

#streams base class
################################################################################

class Stream:
    identno = 0
    def __init__(self):
        self.identifier = str(Stream.identno)
        Stream.identno += 1

    def get_identifier(self):
        return self.identifier

    def __add__(self, other): return Binary(self, other, 'add')
    def __sub__(self, other): return Binary(self, other, 'sub')
    def __mul__(self, other): return Binary(self, other, 'mul')
    def __mod__(self, other): return Binary(self, other, 'mod')
    def __floordiv__(self, other): return Binary(self, other, 'div')
    def __and__(self, other): return Binary(self, other, 'and')
    def __or__(self, other): return Binary(self, other, 'or')
    def __xor__(self, other): return Binary(self, other, 'xor')
    def __rshift__(self, other): return Binary(self, other, 'sr')
    def __lshift__(self, other): return Binary(self, other, 'sl')
    def __eq__(self, other): return Binary(self, other, 'eq')
    def __ne__(self, other): return Binary(self, other, 'ne')
    def __gt__(self, other): return Binary(self, other, 'gt')
    def __ge__(self, other): return Binary(self, other, 'ge')
    def __lt__(self, other): return Binary(self, other, 'lt')
    def __le__(self, other): return Binary(self, other, 'le')

#streams sources
################################################################################

class Repeater(Stream):

    def __init__(self, value, bits=8):
        self.value, self.bits = value, bits
        Stream.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_repeater(self)

    def generator(self): 
        return itertools.repeat(self.value)

class Counter(Stream):

    def __init__(self, start, stop, step, bits=8):
        self.start = start
        self.stop = stop 
        self.step = step 
        self.bits = bits
        Stream.__init__(self)

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        plugin.write_counter(self)

    def generator(self): 
        return itertools.cycle(xrange(start, stop, step))

class InPort(Stream):

    def __init__(self, name, bits, stim=[]):
        self.name, self.bits, self.stim = name, bits, stim
        Stream.__init__(self)

    def get_bits(self): return self.bits

    def write_code(self, plugin): 
        plugin.write_in_port(self)

    def generator(self): 
        for i in self.stim:
            yield i

#streams sinks
################################################################################
class OutPort(Stream):

    def __init__(self, name, a):
        self.name, self.a = name, a
        Stream.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_out_port(self)

    def generator(self): 
        return self.a.generator()

class Asserter(Stream):

    def __init__(self, a):
        self.a = a
        Stream.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_asserter(self)

    def generator(self): 
        return self.a.generator()

class Printer(Stream):

    def __init__(self, a):
        self.a = a
        Stream.__init__(self)

    def get_bits(self): 
        return self.a.get_bits()

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_printer(self)

    def generator(self): 
        return self.a.generator()


#streams combinators
################################################################################
class _Spawn(Stream):

    def __init__(self, clone):
        self.clone = clone
        Stream.__init__(self)

    def get_bits(self):
        return self.clone.a.get_bits()

    def write_code(self, plugin):
        self.clone._write_code(self, plugin)

class Clone:

    def __init__(self, a):
        self.a = a
        self._spawn = []

    def spawn(self):
        _spawn = _Spawn(self)
        self._spawn.append(_spawn)
        return _spawn

    def _write_code(self, spawn, plugin):
        if spawn is self._spawn[0]:
            self.a.write_code(plugin)
            plugin.write_clone(self)

class  Binary(Stream):

    def __init__(self, a, b, function):
        self.a, self.b, self.function = a, b, function
        Stream.__init__(self)

    def get_bits(self):
        bit_function = {
        'add' : lambda x, y : max((x, y)) + 1,
        'sub' : lambda x, y : max((x, y)) + 1,
        'mul' : lambda x, y : (x + y),
        'and' : lambda x, y : max((x, y)),
        'or'  : lambda x, y : max((x, y)),
        'xor' : lambda x, y : max((x, y)),
        'sl'  : lambda x, y : max((x, y)),
        'sr'  : lambda x, y : max((x, y)),
        'eq'  : lambda x, y : 1,
        'ne'  : lambda x, y : 1,
        'lt'  : lambda x, y : 1,
        'le'  : lambda x, y : 1,
        'gt'  : lambda x, y : 1,
        'ge'  : lambda x, y : 1,
        }
        return bit_function[self.function](self.a.get_bits(), self.b.get_bits())

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        self.b.write_code(plugin)
        plugin.write_binary(self)

    def generator(self):
        generator_function = {
        'add' : lambda x, y : x + y,
        'sub' : lambda x, y : x - y,
        'mul' : lambda x, y : x * y,
        'and' : lambda x, y : x & y,
        'or'  : lambda x, y : x | y,
        'xor' : lambda x, y : x ^ y,
        'sl'  : lambda x, y : x << y,
        'sr'  : lambda x, y : x >> y,
        'eq'  : lambda x, y : x == y,
        'ne'  : lambda x, y : x != y,
        'lt'  : lambda x, y : x < y,
        'le'  : lambda x, y : x <= y,
        'gt'  : lambda x, y : x > y,
        'ge'  : lambda x, y : x >= y,
        }
        gena, genb = self.a.generator(), self.b.generator()
        f = generator_function[self.function]
        while True: yield f(next(gena), next(genb))

class Switch(Stream):

    def __init__(self, select, *args):
        Stream.__init__(self)
        self.select = select
        self.a = args

    def get_bits(self): 
        return max((i.get_bits() for i in self.a))

    def write_code(self, plugin): 
        for i in self.a:
            i.write_code(plugin)
        self.select.write_code(plugin)
        plugin.write_switch(self)

    def generator(self):
        a = self.a.generator()
        select = self.select.generate()
        while True:
            a = self.a[next(select)]
            yield next(a)

class Lookup(Stream):

    def __init__(self, source, bits, *args):
        Stream.__init__(self)
        self.a = source
        self.args = args
        self.bits = bits

    def get_bits(self): 
        return self.bits

    def write_code(self, plugin): 
        self.a.write_code(plugin)
        plugin.write_lookup(self)

    def generator(self):
        a = self.a.generator()
        while True:
            yield self.args[next(a)]

#UNIMPLEMENTED

class Register:
    def __init__(self, initval):
        self.initval = initval

    def set(self, a):
        self.a = a
        return self.clone

    def get(self):
        c, self.clone = clone(self)
        return c

    def generator(self):
        yield self.initval
        a = self.a.generator()
        while True:
            yield next(a)
