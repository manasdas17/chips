"""VHDL generation of external ip interface"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def write(plugin, stream):

    identifier = stream.get_identifier()
    instance = stream
    definition = instance.definition

    #generate dependencies and declaration once for each definition
    if definition not in plugin.external_definitions:
        plugin.external_definitions.append(definition)

        #add external VHDL dependencies
        dependencies = []
        vhdl_dependencies = definition.dependencies["VHDL"]

        for dependency_file_name in vhdl_dependencies:
            dependency_file = open(dependency_file_name, 'r')
            dependency_file = dependency_file.read()
            dependencies.append(dependency_file)

        #add non-stream port mapping to top level
        ports = []

        for input_port, size in definition.input_ports.iteritems():
            mapping = instance.inport_mapping[input_port]
            if size == 1:
                ports.append("      {0} : in std_logic".format(mapping))
            else:
                ports.append("      {0} : in std_logic_vector({1} downto 0)".format(mapping, size-1))

        for output_port, size in definition.output_ports.iteritems():
            mapping = instance.outport_mapping[output_port]
            if size == 1:
                ports.append("      {0} : out std_logic".format(mapping))
            else:
                ports.append("      {0} : out std_logic_vector({1} downto 0)".format(mapping, size-1))
            
        #add component declaration
        component_ports = [
        "      CLK : in std_logic",
        "      RST : in std_logic",
        "      TIMER_1us : in std_logic",
        "      TIMER_10us : in std_logic",
        "      TIMER_100us : in std_logic",
        "      TIMER_1ms : in std_logic",
        ]

        for input_port, size in definition.input_ports.iteritems():
            if size == 1:
                component_ports.append("      {0} : in std_logic".format(input_port))
            else:
                component_ports.append("      {0} : in std_logic_vector({1} downto 0)".format(input_port, size-1))

        for output_port, size in definition.output_ports.iteritems():
            if size == 1:
                component_ports.append("      {0} : out std_logic".format(output_port))
            else:
                component_ports.append("      {0} : out std_logic_vector({1} downto 0)".format(output_port, size-1))

        for input_stream, size in definition.input_streams.iteritems():
            if size == 1:
                component_ports.append("      {0} : in std_logic".format(input_stream))
                component_ports.append("      {0}_STB : in std_logic".format(input_stream))
                component_ports.append("      {0}_ACK : out std_logic".format(input_stream))
            else:
                component_ports.append("      {0} : in std_logic_vector({1} downto 0)".format(input_stream, size-1))
                component_ports.append("      {0}_STB : in std_logic".format(input_stream))
                component_ports.append("      {0}_ACK : out std_logic".format(input_stream))

        for output_stream, size in definition.output_streams.iteritems():
            if size == 1:
                component_ports.append("      {0} : out std_logic".format(output_stream))
                component_ports.append("      {0}_STB : out std_logic".format(output_stream))
                component_ports.append("      {0}_ACK : in std_logic".format(output_stream))
            else:
                component_ports.append("      {0} : out std_logic_vector({1} downto 0)".format(output_stream, size-1))
                component_ports.append("      {0}_STB : out std_logic".format(output_stream))
                component_ports.append("      {0}_ACK : in std_logic".format(output_stream))

        declarations = [
"  component {0} is".format(definition.name),
"    port(",
';\n'.join(component_ports),
"    );",
"  end component {0};".format(definition.name),
"",
        ]

    else:
        declarations = []

    #per instance declarations
    for output_stream in instance.output_streams:
        identifier = output_stream.get_identifier()
        bits = output_stream.get_bits()
        declarations.extend([
    "  signal STREAM_{0}     : std_logic_vector({1} downto 0);".format(identifier, bits - 1),
    "  signal STREAM_{0}_STB : std_logic;".format(identifier),
    "  signal STREAM_{0}_ACK : std_logic;".format(identifier),
    "",
        ])

    component_port_map = [
    "      CLK => CLK",
    "      RST => RST",
    "      TIMER_1us => TIMER_1us",
    "      TIMER_10us => TIMER_10us",
    "      TIMER_100us => TIMER_100us",
    "      TIMER_1ms => TIMER_1ms",
    ]

    for input_port, size in definition.input_ports.iteritems():
        mapping = instance.inport_mapping[input_port]
        component_port_map.append("      {0} => {1}".format(input_port, mapping))

    for output_port, size in definition.output_ports.iteritems():
        mapping = instance.outport_mapping[output_port]
        component_port_map.append("      {0} => {1}".format(output_port, mapping))

    for instance_port, definition_port in zip(instance.input_streams, definition.input_streams):
        instance_port_identifier = instance_port.get_identifier()
        component_port_map.append("      {0} => STREAM_{1}".format(definition_port, instance_port_identifier))
        component_port_map.append("      {0}_STB => STREAM_{1}_STB".format(definition_port, instance_port_identifier))
        component_port_map.append("      {0}_ACK => STREAM_{1}_ACK".format(definition_port, instance_port_identifier))

    for instance_port, definition_port in zip(instance.output_streams, definition.output_streams):
        instance_port_identifier = instance_port.get_identifier()
        component_port_map.append("      {0} => STREAM_{1}".format(definition_port, instance_port_identifier))
        component_port_map.append("      {0}_STB => STREAM_{1}_STB".format(definition_port, instance_port_identifier))
        component_port_map.append("      {0}_ACK => STREAM_{1}_ACK".format(definition_port, instance_port_identifier))

    definitions = [
"  --file: {0}, line: {1}".format(stream.filename, stream.lineno),
"  --STREAM {0} ExternalIPInstance()".format(identifier),
"    {0}_{1} : {0} port map(".format(definition.name, identifier),
    ',\n'.join(component_port_map),
"    );",
"",
    ]

    return dependencies, ports, declarations, definitions
