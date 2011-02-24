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
import stimulus

#sinks
import out_port
import console
import asserter
import serial_out
import response

#combinators
import binary
import lookup
import array
import fifo
import decoupler
import resizer
import printer

#system
import system

#processes
import process
import external_ip

class Plugin:

    def __init__(
            self, 
            project_name = "project",
            clock_frequency = 50000000,
            internal_clock = True,
            internal_reset = True,
            ):
        self.project_name = project_name
        self.internal_clock = internal_clock
        self.internal_reset = internal_reset
        self.clock_frequency = 50000000
        self.declarations = []
        self.definitions = []
        self.ports = []
        self.dependencies = []
        self.processes = []
        self.external_definitions=[]

    #sources
    def write_stimulus(self, stream): 
        ports, declarations, definitions = stimulus.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

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
    def write_response(self, stream): 
        ports, declarations, definitions = response.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

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

    def write_svga(self, stream): 
        dependencies, ports, declarations, definitions = svga.write(stream)
        self.dependencies.extend(dependencies)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_console(self, stream): 
        ports, declarations, definitions = console.write(stream)
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

    def write_array(self, stream): 
        dependencies, ports, declarations, definitions = array.write(self, stream)
        self.dependencies.extend(dependencies)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_fifo(self, stream): 
        dependencies, ports, declarations, definitions = fifo.write(self, stream)
        self.dependencies.extend(dependencies)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_decoupler(self, stream): 
        ports, declarations, definitions = decoupler.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_resizer(self, stream): 
        ports, declarations, definitions = resizer.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_printer(self, stream): 
        ports, declarations, definitions = printer.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_external_ip(self, ip): 
        dependencies, ports, declarations, definitions = external_ip.write(self, ip)
        self.dependencies.extend(dependencies)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    def write_process(self, p):
        process.write_process(p, self)

    def write_output(self, p):
        pass

    #System VHDL Generation and external tools

    def write_system(self, s):
        output_file = open(
                ''.join([self.project_name, ".vhd"]),
                'w'
        )
        system.write(
                self.dependencies, 
                self.ports, 
                self.declarations, 
                self.definitions, 
                output_file, 
                self.internal_clock, 
                self.internal_reset
        )

    def set_simulation_data(self, stimulus, iterator):

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

        stimulus_file = open(
            "stim_{0}.txt".format(stimulus.get_identifier()),
            'w'
        )

        for i in iterator:
            stimulus_file.write(str(i)+"\n")

        stimulus_file.close()
        
        #leave ghdl directory
        os.chdir(os.path.join("..", ".."))

    def get_simulation_data(self, response):

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

        stimulus_file = open(
            "resp_{0}.txt".format(response.a.get_identifier()),
            'r'
        )

        data = [int(i) for i in stimulus_file]

        stimulus_file.close()
        
        #leave ghdl directory
        os.chdir(os.path.join("..", ".."))

        return data


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
        self.write_system(None)

        pipe = subprocess.Popen( ''.join([
        "ghdl -a ", 
        os.path.join(".", self.project_name),
        ".vhd", 
        ]), shell=True)
        pipe.wait()
        error_message = pipe.communicate()[1]
        return_code = pipe.returncode

        if return_code != 0:
            print name,
            print "...Fail"
            print error_message
            return False

        pipe = subprocess.Popen(''.join([
        "ghdl -e ",
        "streams_vhdl_model"]), shell=True)
        pipe.wait()
        error_message = pipe.communicate()[1]
        return_code = pipe.returncode

        if return_code != 0:
            print name,
            print "...Fail"
            print error_message
            return False

        parameters = [os.path.join(".", "streams_vhdl_model")]
        if generate_wave: 
            parameters.append(" --wave=wave.ghw")
        if stop_cycles: 
            parameters.append(" --stop-time={0}ns".format((stop_cycles * 10) + 20))

        pipe = subprocess.Popen(
                ''.join(parameters), 
                shell=True, 
                stderr=subprocess.PIPE, 
        )
        error_message = pipe.communicate()[1]
        pipe.wait()
        return_code = pipe.returncode

        if return_code != 0:
            print name,
            print "...Fail"
            print error_message
            return False

        os.chdir(os.path.join("..", ".."))

        print name,
        print "...Pass"
        return True

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
        self.write_system(None)

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
