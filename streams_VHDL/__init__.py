#python modules
import subprocess
import os

#sources
import in_port
import repeater
import counter

#sinks
import out_port
import printer
import asserter

#combinators
import binary
import clone
import switch
import lookup

#system
import system

class Plugin:

    def __init__(
            self, 
            project_name = "streams_project",
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

    #sinks

    def write_out_port(self, stream): 
        ports, declarations, definitions = out_port.write(stream)
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

    def write_lookup(self, stream): 
        ports, declarations, definitions = lookup.write(stream)
        self.ports.extend(ports)
        self.declarations.extend(declarations)
        self.definitions.extend(definitions)

    #combinators

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
            os.path.join("..", self.project_name),
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
            subprocess.call(''.join(parameters), shell=True)

        os.chdir(os.path.join("..", ".."))

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
