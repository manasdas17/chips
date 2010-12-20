"""Visualisation for streams library"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

#python modules
import subprocess
import os

class Plugin:

    def __init__(self, title="System"):

    #sources
    def write_stimulus(self, stream): 
        pass

    def write_repeater(self, stream): 
        self.source.append
            "int get_stream_{0}() return {1};".format(stream.get_identifier() stream.value)
            "int reset_stream_{0}(){".format(stream.get_identifier()),
            "  count_{0} = {1};".format(stream.get_identifier(), stream.start),
            "}",
        )

    def write_counter(self, stream): 
        self.source.extend([
            "int count_{0} = {1};".format(stream.get_identifier() stream.start),
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  int ret = count_{0};".format(stream.get_identifier()),
            "  count_{0} += {1};".format(stream.get_identifier(), stream.start),
            "  if (count == {0}) count = {1};".format(stream.stop, stream.step),
            "  return ret;",
            "}",
            "int reset_stream_{0}(){".format(stream.get_identifier()),
            "  count_{0} = {1};".format(stream.get_identifier(), stream.start),
            "}",
        ])

    def write_in_port(self, stream): 
        pass

    def write_serial_in(self, stream): 
        pass

    #sinks
    def write_response(self, stream): 
        pass

    def write_out_port(self, stream): 
        pass

    def write_serial_out(self, stream): 
        pass

    def write_svga(self, stream): 
        pass

    def write_console(self, stream): 
        self.source.extend([
            "int execute_{0}(){".format(stream.get_identifier()),
            "  char c = get_stream_{0}()&0xff;".format(stream.a.get_identifier()),
            "  cout << c;".format(stream.a.get_identifier()),
            "}",
        ])

    def write_asserter(self, stream): 
        self.source.extend([
            "int execute_{0}(){".format(stream.get_identifier()),
            "  assert get_stream_{0};".format(stream.a.get_identifier()),
            "}",
        ])

    #combinators

    def write_binary(self, stream): 
        labels = { 'add' : '+', 'sub' : '-', 'mul' : '*', 'div' : '//', 'mod' : '%',
            'and' : '&', 'or'  : '|', 'xor' : '^', 'sl'  : '<<', 'sr'  : '>>', 
            'eq'  : '==', 'ne'  : '!=', 'lt'  : '<=', 'le'  : '<', 'gt'  : '>',
            'ge'  : '>='
        }
        self.source.extend([
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  int a = get_stream_{0}();".format(stream.a.get_identifier()),
            "  int b = get_stream_{0}();".format(stream.b.get_identifier()),
            "  return a {0} b;".format(labels[a.function]),
            "}",
            "void reset_stream_{0}(){}".format(stream.get_identifier()),
        ])

    def write_lookup(self, stream): 
        self.source.extend([
            "int lookup_{0}[{1}];".format(stream.get_identifier(), stream.size),
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  return = lookup_{0}[get_stream_{0}()];".format(stream.a.get_identifier()),
            "}",
            "void reset_stream_{0}(){}".format(stream.get_identifier()),
        ])

    def write_array(self, stream): 
        self.source.extend([
            "int array_{0}[{1}];".format(stream.get_identifier(), stream.size),
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  return = lookup_{0}[get_stream_{0}()];".format(stream.c.get_identifier()),
            "}",
            "int execute_{0}(){".format(stream.get_identifier()),
            "  array_{0}[get_stream_{1}()] = get_stream_{2};".format(stream.get_identifier(), stream_a.get_identifier(), stream.b.get_identifier()),
            "}",
            "void reset_stream_{0}(){}".format(stream.get_identifier()),
        ])

    def write_decoupler(self, stream): 
        self.source.extend([
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  return get_stream_{0}();".format(stream.a.get_identifier()),
            "}",
            "void reset_stream_{0}(){}".format(stream.get_identifier()),
        ])

    def write_resizer(self, stream): 
        self.source.extend([
            "int get_stream_{0}(){".format(stream.get_identifier()),
            "  return get_stream_{0}();".format(stream.a.get_identifier()),
            "}",
            "void reset_stream_{0}(){}".format(stream.get_identifier()),
        ])

    def write_printer(self, stream): 
        pass

    def write_output(self, stream): 
        pass

    def write_process(self, p):
        pass

    def write_system(self, *args):
        pass

