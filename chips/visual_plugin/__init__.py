"""Visualisation for streams library"""

import subprocess
import os

from pygraphviz import AGraph

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"


class Plugin:

    def __init__(self, title="System"):
        self.schematic = AGraph(
                directed=True, 
                label=title, 
                rankdir='LR', 
                splines='true'
        )
        self.nodes = []
        self.edges = []
        self.outputs = {}
        self.ip_outputs = {}

    #sources
    def write_stimulus(self, stream): 
        self.nodes.append((id(stream), "Stimulus", "ellipse"))

    def write_repeater(self, stream): 
        self.nodes.append(
            (id(stream), "Repeater : {0}".format(stream.value), "ellipse")
        )

    def write_counter(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "Counter : {0}, {1}, {2}".format(
                    stream.start, 
                    stream.stop,
                    stream.step
                ), 
                "ellipse"
            )
        )

    def write_in_port(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "InPort : {0} {1}".format(
                    stream.name, stream.bits
                ), "ellipse"
            )
        )

    def write_serial_in(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "SerialIn : {0}".format(
                    stream.name
                ), 
                "ellipse"
            )
        )

    #sinks
    def write_response(self, stream): 
        self.nodes.append((id(stream), "Response", "box"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_out_port(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "OutPort : {0}".format(
                    stream.name
                ), 
                "box"
            )
        )
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_serial_out(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "SerialOut : {0}".format(
                    stream.name
                ), 
                "box"
            )
        )
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_svga(self, stream): 
        self.nodes.append((id(stream), "SVGA", "box"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_console(self, stream): 
        self.nodes.append((id(stream), "Console", "box"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_asserter(self, stream): 
        self.nodes.append((id(stream), "Asserter", "box"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    #combinators

    def write_binary(self, stream): 
        labels = { 'add' : '+', 'sub' : '-', 'mul' : '*', 'div' : '//', 
            'mod' : '%', 'and' : '&', 'or'  : '|', 'xor' : '^', 
            'sl'  : '<<', 'sr'  : '>>', 'eq'  : '==', 'ne'  : '!=', 
            'lt'  : '<=', 'le'  : '<', 'gt'  : '>', 'ge'  : '>='
        }
        self.nodes.append((id(stream), labels[stream.function], "circle"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "nw"
            )
        )
        self.edges.append(
            (
                id(stream.b), 
                id(stream), 
                stream.b.get_bits(), 
                "sw"
            )
        )

    def write_unary(self, stream): 
        labels = { 'abs' : 'abs', 'not' : '!', 'invert' : '~', 'sln' : '<<', 
            'srn' : '>>',
        }
        self.nodes.append((id(stream), labels[stream.function], "circle"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "nw"
            )
        )
        self.edges.append(
            (
                id(stream.b), 
                id(stream), 
                stream.b.get_bits(), 
                "sw"
            )
        )

    def write_lookup(self, stream): 
        self.nodes.append((id(stream), "Lookup", "ellipse"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_array(self, stream): 
        self.nodes.append((id(stream), "Array", "ellipse"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "nw"
            )
        )
        self.edges.append(
            (
                id(stream.b), 
                id(stream), 
                stream.b.get_bits(), 
                "w"
            )
        )
        self.edges.append(
            (
                id(stream.c), 
                id(stream), 
                stream.c.get_bits(), 
                "sw"
            )
        )

    def write_decoupler(self, stream): 
        self.nodes.append(
            (
                id(stream), 
                "Decoupler", 
                "ellipse"
            )
        )
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_resizer(self, stream): 
        self.nodes.append((id(stream), "Resizer", "ellipse"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_printer(self, stream): 
        self.nodes.append((id(stream), "Printer", "ellipse"))
        self.edges.append(
            (
                id(stream.a), 
                id(stream), 
                stream.a.get_bits(), 
                "w"
            )
        )

    def write_output(self, stream): 
        self.outputs[id(stream)] = id(stream.process)

    def write_process(self, p):
        self.nodes.append((id(p), "Process", "ellipse"))
        for i in p.inputs:
            self.edges.append((id(i), id(p), i.get_bits(), "centre"))

    def write_external_ip(self, ip): 
        for i in ip.output_streams:
            self.ip_outputs[id(i)]=id(ip)

        self.nodes.append((id(ip), ip.definition.name, "ellipse"))
        for i in ip.input_streams:
            self.edges.append((id(i), id(ip), i.get_bits(), "centre"))

    def write_chip(self, *args):
        pass

    #System VHDL Generation and external tools
    def draw(self, filename):
        for ident, label, shape in self.nodes:
            self.schematic.add_node(
                str(ident), 
                shape=shape, 
                label=str(label)
            )
        for from_node, to_node, bits, headport in self.edges:
            if from_node in self.outputs:
                self.schematic.add_edge(
                    str(self.outputs[from_node]), 
                    str(to_node), 
                    label=str(bits), 
                    headport=headport
                )
            elif from_node in self.ip_outputs:
                self.schematic.add_edge(
                    str(self.ip_outputs[from_node]), 
                    str(to_node), 
                    label=str(bits), 
                    headport=headport
                )
            else:
                self.schematic.add_edge(
                    str(from_node), 
                    str(to_node), 
                    label=str(bits)
                )
        self.schematic.layout(prog='dot')
        self.schematic.draw(filename)

