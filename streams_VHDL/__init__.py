"""VHDL Code Generation for streams library"""

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

#sources
import in_port
import repeater
import counter
import serial_in

#sinks
import out_port
import printer
import asserter
import serial_out

#combinators
import binary
import lookup
import resizer
import formater

#flow controllers
import clone
import switch

#system
import system

#processes
import process
import instructions

class Plugin:

    def __init__(
            self, 
            project_name = "project",
            internal_clock = True,
            internal_reset = True,
            ):
        self.project_name = project_name
        self.internal_clock = internal_clock
        self.internal_reset = internal_reset
        self.declarations = []
        self.definitions = []
        self.ports = []

    #sources

    def write_repeater(self, stream): 
        ports, declarations, definitions = repeater.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_counter(self, stream): 
        ports, declarations, definitions = counter.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_in_port(self, stream): 
        ports, declarations, definitions = in_port.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_serial_in(self, stream): 
        ports, declarations, definitions = serial_in.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    #sinks

    def write_out_port(self, stream): 
        ports, declarations, definitions = out_port.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_serial_out(self, stream): 
        ports, declarations, definitions = serial_out.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_printer(self, stream): 
        ports, declarations, definitions = printer.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_asserter(self, stream): 
        ports, declarations, definitions = asserter.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    #combinators

    def write_binary(self, stream): 
        ports, declarations, definitions = binary.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_lookup(self, stream): 
        ports, declarations, definitions = lookup.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_resizer(self, stream): 
        ports, declarations, definitions = resizer.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_formater(self, stream): 
        ports, declarations, definitions = formater.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_clone(self, stream): 
        ports, declarations, definitions = clone.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_switch(self, stream): 
        ports, declarations, definitions = switch.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    #instructions
    def write_process(self, p):
        process.write_process(p, self)

    def write_set(self, instruction):
        return instructions.write_set(instruction)

    def write_read(self, instruction):
        return instructions.write_read(instruction)

    def write_write(self, instruction):
        return instructions.write_write(instruction)

    def write_loop(self, instruction):
        return instructions.write_loop(instruction, self)

    def write_break(self, instruction):
        return instructions.write_break(instruction, self)


    #System VHDL Generation and external tools

    def write_system(self):
        output_file = open(
                ''.join([self.project_name, ".vhd"]),
                'w'
        )
        system.write(
                self.ports, 
                self.declarations, 
                self.definitions, 
                output_file, 
                self.internal_clock, 
                self.internal_reset
        )

    def ghdl_sim(self, analyze=True, elaborate=True, execute=False, generate_wave=False, stop_cycles=False):

        #enter project directory
        if not os.path.isdir(self.project_name): 
            if not os.path.exists(self.project_name):
                os.mkdir(self.project_name)
        os.chdir(self.project_name)

        #enter ghdl directory
        if not os.path.isdir("ghdl"): 
            if not os.path.exists("ghdl"):
                os.mkdir("ghdl")
        os.chdir("ghdl")

        #regenerate vhdl file
        self.write_system()

        if analyze:
            subprocess.call( ''.join([
            "ghdl -a ", 
            os.path.join(".", self.project_name),
            ".vhd", 
            ]), shell=True)

        if elaborate:
            subprocess.call(''.join([
            "ghdl -e ",
            "streams_vhdl_model"]), shell=True)

        if execute:
            parameters = [os.path.join(".", "streams_vhdl_model")]
            if generate_wave: 
                parameters.append(" --wave=wave.ghw")
            if stop_cycles: 
                parameters.append(" --stop-time={0}ns".format(stop_cycles * 10 + 20))
            parameters.append(" --disp-time")
            subprocess.call(''.join(parameters), shell=True)

        os.chdir(os.path.join("..", ".."))

    def ghdl_test(self, name, generate_wave=False, stop_cycles=False):

        #enter project directory
        if not os.path.isdir(self.project_name): 
            if not os.path.exists(self.project_name):
                os.mkdir(self.project_name)
        os.chdir(self.project_name)

        #enter ghdl directory
        if not os.path.isdir("ghdl"): 
            if not os.path.exists("ghdl"):
                os.mkdir("ghdl")
        os.chdir("ghdl")

        #regenerate vhdl file
        self.write_system()

        subprocess.call( ''.join([
        "ghdl -a ", 
        os.path.join(".", self.project_name),
        ".vhd", 
        ]), shell=True)

        subprocess.call(''.join([
        "ghdl -e ",
        "streams_vhdl_model"]), shell=True)

        parameters = [os.path.join(".", "streams_vhdl_model")]
        if generate_wave: 
            parameters.append(" --wave=wave.ghw")
        if stop_cycles: 
            parameters.append(" --stop-time={0}ns".format(stop_cycles * 10 + 20))

        pipe = subprocess.Popen(
                ''.join(parameters), 
                shell=True, 
                stderr=subprocess.PIPE, 
        )
        pipe.wait()
        error_message = pipe.communicate()[1]
        return_code = pipe.returncode

        os.chdir(os.path.join("..", ".."))

        if return_code == 0:
            print name,
            print "...Pass"
            return True
        else:
            print name,
            print "...Fail"
            print error_message
            return False


    def xilinx_build(self, part="xc5vlx30-3-ff676", synth=True, implement=True, bitgen=True):

        #enter project directory
        if not os.path.isdir(self.project_name): 
            if not os.path.exists(self.project_name):
                os.mkdir(self.project_name)
        os.chdir(self.project_name)

        #enter ghdl directory
        if not os.path.isdir("xilinx"): 
            if not os.path.exists("xilinx"):
                os.mkdir("xilinx")
        os.chdir("xilinx")

        #regenerate vhdl file
        self.write_system()

        #generate xst project file
        project = open(self.project_name+".prj", 'w')
        project.write(''.join([self.project_name, ".vhd\n"]))
        project.close()

        synthesis_options = ""
        if synth:
            synthesis_options = ' '.join([
            "-synth xst_vhdl.opt",
            ])

        implementation_options = ""
        if implement:
            implementation_options = ' '.join([
            "-implement balanced.opt",
            ])

        bitgen_options = ""
        if bitgen:
            bitgen_options = ' '.join([
            "-config bitgen.opt",
            ])

        subprocess.call( ' '.join([
        "xflow -p", part,
        synthesis_options,
        implementation_options,
        bitgen_options,
        self.project_name, 
        ]), shell=True)

        os.chdir(os.path.join("..", ".."))
