"""VHDL Code Generation for streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

class Plugin:

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

    def write_printer(self, stream): 
        source = stream.a.generator()
        def printer():
            while True:
                print next(source)
                yield None
        stream.generator = printer

    def write_asserter(self, stream): 
        source = stream.a.generator()
        def asserter():
            while True:
                assert next(source)
                yield None
        stream.generator = asserter

    #combinators
    def write_binary(self, stream): 
        functions = {
            'add' : lambda a, b: a+b,
            'sub' : lambda a, b: a-b,
            'mul' : lambda a, b: a*b,
            'div' : lambda a, b: int((1.0*a)/(1.0*b)),
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
                yield function(next(source_a), next(source_b))
        stream.generator=binary



    def write_lookup(self, stream): 
        args = stream.args
        source = stream.a.generator()
        def lookup():
            for i in source:
                yield args[i]
        stream.generator=lookup

    def write_resizer(self, stream): 
        pass

    def write_formater(self, stream): 
        source = stream.a.generator()
        def formater():
            while True:
                string = str(next(source))
                for i in string:
                    yield(ord(i))
        stream.generator=formater

    def write_process(self, p):
        pass

    def write_system(self, system):
        self.generators = [i.generator for i in system.sinks]

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
