"""C++ code generator for streams library"""

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
#streams modules
import process

class Plugin:

    def __init__(self, project_name="project"):
        self.project_name = project_name
        self.source = []
        self.execute = []
        self.declarations = [""]

    #sources
    def write_stimulus(self, stream): 
        pass

    def write_repeater(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//repeater",
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data =",
            "  {",
            "    {0},".format(stream.value),
            "    false",
            "  };",
            "  if(debug){",
            "   cerr << {0} << \" repeater \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return data;".format(stream.value),
            "}",
            "",
        ])

    def write_counter(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//counter",
            "int count_{0} = {1};".format(stream.get_identifier(), stream.start),
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data;",
            "  data.stalled = false;",
            "  data.value = count_{0};".format(stream.get_identifier()),
            "  count_{0} += {1};".format(stream.get_identifier(), stream.step),
            "  if (count_{0} > {1}) count_{0} = {2};".format(stream.get_identifier(), stream.stop, stream.start),
            "  if(debug){",
            "   cerr << {0} << \" counter \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return data;",
            "}",
            "",
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

    def write_console(self, stream): 
        self.declarations.append("void execute_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//console",
            "void execute_{0}()".format(stream.get_identifier()),
            "{",
            "  char c = get_stream_{0}().value&0xff;".format(stream.a.get_identifier()),
            "  cout << c;".format(stream.a.get_identifier()),
            "}",
            "",
        ])
        self.execute.extend([
            "  execute_{0}();".format(stream.get_identifier()),
        ])

    def write_asserter(self, stream): 
        self.declarations.append("void execute_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//asserter",
            "void execute_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data = get_stream_{0}();".format(stream.a.get_identifier()),
            "  if (!data.stalled)",
            "  {",
            "    assert(data.value);".format(stream.a.get_identifier()),
            "  }",
            "}",
            "",
        ])
        self.execute.extend([
            "  execute_{0}();".format(stream.get_identifier()),
        ])

    #combinators

    def write_binary(self, stream): 
        functions = { 'add' : '+', 'sub' : '-', 'mul' : '*', 'div' : '/', 'mod' : '%',
            'and' : '&', 'or'  : '|', 'xor' : '^', 'sl'  : '<<', 'sr'  : '>>', 
            'eq'  : '==', 'ne'  : '!=', 'lt'  : '<', 'le'  : '<=', 'gt'  : '>',
            'ge'  : '>='
        }
        negate = { 'add' : '', 'sub' : '', 'mul' : '', 'div' : '', 'mod' : '',
            'and' : '', 'or'  : '', 'xor' : '', 'sl'  : '', 'sr'  : '', 
            'eq'  : '-', 'ne'  : '-', 'lt'  : '-', 'le'  : '-', 'gt'  : '-',
            'ge'  : '-'
        }
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//binary",
            "data_type data_1_{0} = {1}0, true{2};".format(stream.get_identifier(), "{", "}"),
            "data_type data_2_{0} = {1}0, true{2};".format(stream.get_identifier(), "{", "}"),
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data;".format(stream.get_identifier()),
            "  if (data_1_{0}.stalled)".format(stream.get_identifier()),
            "    data_1_{0} = get_stream_{1}();".format(stream.get_identifier(), stream.a.get_identifier()),
            "  if (data_2_{0}.stalled)".format(stream.get_identifier()),
            "    data_2_{0} = get_stream_{1}();".format(stream.get_identifier(), stream.b.get_identifier()),
            "  if(!data_1_{0}.stalled && !data_2_{0}.stalled)".format(stream.get_identifier()),
            "  {",
            "    data_1_{0}.stalled = true;".format(stream.get_identifier()),
            "    data_2_{0}.stalled = true;".format(stream.get_identifier()),
            "  }",
            "  data.value = {0}resize((data_1_{1}.value {2} data_2_{1}.value), {3});".format(
                negate[stream.function],
                stream.get_identifier(), 
                functions[stream.function], 
                stream.get_bits()
            ),
            "  data.stalled = data_1_{0}.stalled || data_2_{0}.stalled;".format(stream.get_identifier()),
            "  if(debug){",
            "   cerr << {0} << \" binary \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return data;",
            "}",
            "",
        ])

    def write_lookup(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//lookup table",
            "int lookup_{0}[{1}] = ".format(stream.get_identifier(), len(stream.args)),
            "{",
            ",".join([str(i) for i in stream.args]),
            "};",
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data = get_stream_{1}();".format(stream.get_identifier(), stream.a.get_identifier()),
            "  data.value = lookup_{0}[data.value];".format(stream.get_identifier(), stream.a.get_identifier()),
            "  data.stalled = false;",
            "  if(debug){",
            "   cerr << {0} << \" lookup \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return data;",
            "}",
            "",
        ])

    def write_array(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.declarations.append("void execute_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//array",
            "data_type array_{0}[{1}];".format(stream.get_identifier(), stream.depth),
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data;",
            "  data = get_stream_{0}()".format(stream.c.get_identifier()),
            "  if(debug){",
            "   cerr << {0} << \" array \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return lookup_{0}[get_stream_{0}()];".format(stream.c.get_identifier()),
            "}",
            "",
            #"data_type data_1_{0} = {0; true};".format(stream.get_identifier()),
            #"data_type data_2_{0} = {0; true};".format(stream.get_identifier()),
            "void execute_{0}()".format(stream.get_identifier()),
            "{",
            "  if (data_1_{0}.stalled)".format(stream.get_identifier()),
            "    data_1_{0} = get_stream_{1}();".format(stream.get_identifier(), stream.a.get_identifier()),
            "  if (data_2_{0}.stalled)".format(stream.get_identifier()),
            "    data_2_{0} = get_stream_{1}();".format(stream.get_identifier(), stream.b.get_identifier()),
            "  if(!data_1_{0}.stalled && !data_2_{0}.stalled)".format(stream.get_identifier()),
            "  {",
            "    array_{0}[data_1_{0}.value] = data_2_{0}.value;".format(stream.get_identifier()),
            "    data_1_{0}.stalled = true;".format(stream.get_identifier()),
            "    data_2_{0}.stalled = true;".format(stream.get_identifier()),
            "  }",
            "}",
            "",
        ])
        self.execute.extend([
            "  execute_{0}();".format(stream.get_identifier()),
        ])

    def write_fifo(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//fifo",
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  return get_stream_{0}();".format(stream.a.get_identifier()),
            "}",
            "",
        ])

    def write_decoupler(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//decoupler",
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  return get_stream_{0}();".format(stream.a.get_identifier()),
            "}",
            "",
        ])

    def write_resizer(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//resizer",
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  return get_stream_{0}();".format(stream.a.get_identifier()),
            "}",
            "",
        ])

    def write_printer(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//printer",
            "string chars_{0};".format(stream.get_identifier()),
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "    ostringstream charstream;",
            "    data_type data;",
            "    char c;",
            "    if (chars_{0}.length() > 0)".format(stream.get_identifier()),
            "    {",
            "        c = chars_{0}[0];".format(stream.get_identifier()),
            "        data.value = c;",
            "        data.stalled = false;".format(stream.get_identifier()),
            "        chars_{0}.erase(0,1);".format(stream.get_identifier()),
            "        if(debug){",
            "          cerr << {0} << \" printer \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "        }",
            "        return data;",
            "    }",
            "    else",
            "    {",
            "        data = get_stream_{0}();".format(stream.a.get_identifier()),
            "        if (data.stalled)",
            "        {",
            "            data.value = 0;",
            "            data.stalled = true;",
            "            return data;",
            "        }",
            "        charstream << data.value << endl;",
            "        chars_{0} = charstream.str();".format(stream.get_identifier()),
            "        c = chars_{0}[0];".format(stream.get_identifier()),
            "        data.value = c;",
            "        data.stalled = false;".format(stream.get_identifier()),
            "        chars_{0}.erase(0,1);".format(stream.get_identifier()),
            "        if(debug){",
            "          cerr << {0} << \" printer \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "        }",
            "        return data;",
            "    }",
            "}",
        ])

    def write_output(self, stream): 
        self.declarations.append("data_type get_stream_{0}();".format(stream.get_identifier()))
        self.source.extend([
            "//process output",
            "data_type output_{0} = {1}0, true{2};".format(stream.get_identifier(), "{", "}"),
            "data_type get_stream_{0}()".format(stream.get_identifier()),
            "{",
            "  data_type data = output_{0};".format(stream.get_identifier()),
            "  output_{0}.stalled = true;".format(stream.get_identifier()),
            "  if(debug){",
            "   cerr << {0} << \" process output \" << data.value << \" \" << data.stalled << endl;".format(stream.get_identifier()),
            "  }",
            "  return data;",
            "}",
            "",
        ])

    def write_process(self, p):
        declarations, definitions, execute = process.write_process(p, self)
        self.declarations.extend(declarations)
        self.source.extend(definitions)
        self.execute.extend(execute)

    def write_system(self, *args):
        header = [
        "#include <iostream>",
        "#include <sstream>",
        "#include <string>",
        "using namespace std;",
        "#include <assert.h>",
        "",
        "struct data_type {",
        "  int value;",
        "  bool stalled;",
        "};",
        "",
        "int resize(int val, int bits)",
        "{",
        "    int mask = (1<<bits)-1;",
        "    int sign_bit = 1<<(bits-1);",
        "    val = val & mask;",
        "    if (val & sign_bit) ",
        "    {",
        "        val = val|~mask;",
        "    }",
        "    return val;",
        "}",
        "",
        "  const bool debug = true;",
        "",
        ]
        body = [
        "",
        "//main body",
        "int main(int argc, char **argv)",
        "{",
        "  istringstream is;",
        "  string cycle_string;",
        "  int cycles;",
        "  if (argc > 0)",
        "  {",
        "    cycle_string = argv[1];",
        "    is.str(cycle_string);",
        "    is >> cycles;",
        "    for(int i = 0; i < cycles; i++)",
        "    {",
        "      cerr << \"cycle ......................\" << i << endl;",
        '\n'.join(self.execute),
        "    }",
        "  }",
        "}",
        ]
        self.declarations.append("");
        self.declarations.append("");
        output_file = open(
            os.path.join(".", self.project_name+".cpp"), "w")
        output_file.write('\n'.join(header))
        output_file.write('\n'.join(self.declarations))
        output_file.write('\n'.join(self.source))
        output_file.write('\n'.join(body))

    def test(self, name, stop_cycles=False):

        #enter project directory
        if not os.path.isdir(self.project_name): 
            if not os.path.exists(self.project_name):
                os.mkdir(self.project_name)
        os.chdir(self.project_name)

        #enter cpp directory
        if not os.path.isdir("cpp"): 
            if not os.path.exists("cpp"):
                os.mkdir("cpp")
        os.chdir("cpp")

        #regenerate cpp file
        self.write_system(None)

        pipe = subprocess.Popen( ''.join([
        "g++ ", 
        os.path.join(".", self.project_name),
        ".cpp -o ", 
        "streams_cpp_model", 
        ]), shell=True)
        pipe.wait()
        error_message = pipe.communicate()[1]
        return_code = pipe.returncode

        if return_code != 0:
            print name,
            print "...Fail"
            print error_message
            return False

        parameters = [os.path.join(".", "streams_cpp_model")]
        parameters += " " + str(stop_cycles)
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
