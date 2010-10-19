"""VHDL Code Generation for streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from process import Process

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))


class Plugin:
    def __init__(self):
        self.processes = []

    #sources
    def write_repeater(self, stream): 
        def repeater():
            while True: yield stream.value
        stream.generator=repeater

    def write_counter(self, stream): 
        def counter():
            while True:
                count = stream.start
                while True:
                    yield count
                    if count == stream.stop:
                        break
                    else:
                        count += stream.step
        stream.generator=counter

    def write_in_port(self, stream): 
        pass

    def write_serial_in(self, stream): 
        pass

    #sinks
    def write_out_port(self, stream): 
        pass

    def write_serial_out(self, stream): 
        pass

    def write_ascii_printer(self, stream): 
        source = stream.a.generator()
        def printer():
            while True:
                data = next(source)
                if data is not None:
                    print chr(data&0xff)
                yield None
        stream.generator = printer

    def write_decimal_printer(self, stream): 
        source = stream.a.generator()
        def printer():
            while True:
                data = next(source)
                if data is not None:
                    print data
                yield None
        stream.generator = printer

    def write_hex_printer(self, stream): 
        source = stream.a.generator()
        def printer():
            while True:
                data = next(source)
                if data is not None:
                    print hex(data)
                yield None
        stream.generator = printer

    def write_asserter(self, stream): 
        source = stream.a.generator()
        def asserter():
            while True:
                data = next(source)
                if data is not None:
                    assert data
                yield None
        stream.generator = asserter

    #combinators
    def write_binary(self, stream): 
        functions = {
            'add' : lambda a, b: a+b,
            'sub' : lambda a, b: a-b,
            'mul' : lambda a, b: a*b,
            'div' : lambda a, b: c_style_division(a, b),
            'mod' : lambda a, b: c_style_modulo(a, b),
            'and' : lambda a, b: a&b,
            'or'  : lambda a, b: a|b,
            'xor' : lambda a, b: a^b,
            'sl'  : lambda a, b: a<<b,
            'sr'  : lambda a, b: a>>b,
            'eq'  : lambda a, b: -int(a==b),
            'ne'  : lambda a, b: -int(a!=b),
            'lt'  : lambda a, b: -int(a<b),
            'le'  : lambda a, b: -int(a<=b),
            'gt'  : lambda a, b: -int(a>b),
            'ge'  : lambda a, b: -int(a>=b),
        }
        source_a = stream.a.generator()
        source_b = stream.b.generator()
        function = functions[stream.function]
        def binary():
            while True:
                while True:
                    a = next(source_a)
                    if a is not None:
                        break
                while True:
                    b = next(source_b)
                    if b is not None:
                        break
                yield function(a, b)
        stream.generator=binary



    def write_lookup(self, stream): 
        args = stream.args
        source = stream.a.generator()
        print source
        def lookup():
            for i in source:
                print i
                if i is not None:
                    yield args[i]
                else:
                    yield None
        stream.generator=lookup

    def write_resizer(self, stream): 
        source = stream.a.generator()
        bits = stream.get_bits()
        sign_bits = -(2**(bits-1))
        def resizer(val):
            while True:
                val = next(source)
                if val is not None:
                    yield val | sign_bits if val & sign_bits else val & ~sign_bits

    def write_decimal_formatter(self, stream): 
        source = stream.a.generator()
        def formater():
            while True:
                data = next(source)
                if data is not None:
                    string = str(data)
                    for i in string:
                        yield(ord(i))
        stream.generator=formater

    def write_hex_formatter(self, stream): 
        source = stream.a.generator()
        def formater():
            while True:
                data = next(source)
                if data is not None:
                    string = hex(data)
                    for i in string:
                        yield(ord(i))
        stream.generator=formater

    def write_process(self, p):
        Process(p)

    def write_system(self, system):
        self.generators = [i.generator for i in system.sinks]

    def start_sim(self):
        self.iterators = [i() for i in self.generators]

    def step_sim(self):
        for i in self.processes:
            i.execute()
        for i in self.iterators:
            next(i)

    def python_test(self, name, stop_cycles=100):

        iterators = [i() for i in self.generators]
        try:
            for i in range(stop_cycles):
                for i in iterators:
                    next(i)
                
        except AssertionError:
            print name,
            print "...Fail"
            return False

        print name,
        print "...Pass"
        return True
