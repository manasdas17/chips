#!/usr/bin/env python

"""

*Processes* are used to define the programs that will be executed in the target
*Chip*.  Each *Process* contains a single program made up of instructions. When
a *Chip* is simulated, or run in real hardware, the program within each process
will be run concurrently.

Process Inputs
--------------

Any *Stream* may be used as the input to a *Process*. Only one process may read
from any particular stream.  A *Process* may read from a *Stream* using the
*read* method. The *read* method accepts a *Variable* as its argument. A *read*
from a *Stream* will stall execution of the *Process* until data is available.
Similarly, the stream will be stalled, until data is read from it. This
provides a handy way to synchronise processes together, and simplifies the
design of concurrent systems.

Example::

    #sending process
    theoutput = Output()
    count = Variable(0)
    Process(16,
        #wait for 1 second
        count.set(1000),
        While(count, 
            count.set(count-1),
            WaitUs()
        ),
        #send some data
        theoutput.write(123),
    )

    #receiving process
    target_variable = Variable(100)
    Process(16,
        #This instruction will stall the process until data is available
        theoutput.read(target_variable),
        #This instruction will not be run for 1 second
        #..
    )

Process Outputs
---------------

An *Output* is a special *Stream* that can be written to by a *Process*. Only one
*Process* may write to any particular stream. Like any other *Stream*, an
*Output* may be:

    * Read by a *Process*.  
    * Consumed by a *Sink*.  
    * Modified to form another *Stream*.

A *Process* may write to an *Output* stream using the *write* method. The
*write* method accepts an expression as its argument. A *write* to an output
will stall the process until the receiver is ready to receive data.

Example::

    #sending process
    theoutput = Output()
    Process(16,
        #This instruction will stall the process until data is available
        theoutput.write(123),
        #This instruction will not be run for 1 second
        #..
    )

    #receiving process
    target_variable = Variable(0)
    count = Variable(0)
    Process(16,
        #wait for 1 second
        count.set(1000),
        While(count, 
            count.set(count-1),
            WaitUs(),
        ),
        #get some data
        theoutput.read(target_variable),
    )

Variables
---------

Data is stored and manipulated within a process using *Variables*. A *Variable*
may only be accessed by one process.  When a *Variable* an initial value must
be supplied. A variable will be reset to its initial value before any process
instructions are executed.  A *Variable* may be assigned a value using the
*set* method. The *set* method accepts an expression as its argument.

It is important to understand that a *Variable* object created like this::

    a = Variable(12)

is very different from a normal Python variable created like this::

    a = 12

The key is to understand that a *Variable* will exist in the target *Chip*, and
may be assigned and referenced as the *Process* executes. A Python variable can
exist only in the Python environment, and not in a *Chip*. While a Python
variable may be converted into a constant in the target *Chip*, a *Process*
has no way to change its value when it executes.

Expressions
-----------

*Variables* and *Constants* are the most basic form of expressions. More
complex expressions can be formed by combining *Constants*, *Variables* and
other expressions using following unary operators::

	~

and the folowing binary operators::

    +, -, *, \/, %, &, |, ^, <<, >>, ==, !=, <, <=, >, >=

The function *Not* evaluates to the logical negation of each data item
equivalent to ``==0``. The function *abs* evaluates to the magnitude of each
data item.

If one of the operands of a binary operator is not an expression, the Chips
library will attempt to convert this operand into an integer. If the conversion
is successful, a *Constant* object will be created using the integer value.
The *Constant* object will be used in place of the non-expression operand. This
allows constructs such as ``a = 47+Constant(10)`` to be used as a shorthand for
``a = Constant(47)+Constant(10)`` or ``count.set(Constant(15)+3*2`` to be used
as a shorthand for ``count.set(Constant(15)+Constant(6)``.  Of course ``a=1+1``
still yields the integer 2 rather than an expression.

An expression within a process will always inherit the data width in bits of
the *Process* in which it is evaluated. A *Stream* expression such as
``Repeater(255) + 1`` will automatically yield a 10-bit *Stream* so that the
value 256 can be represented. A similar expression Constant(255)+1 will give an
9-bit result in a 9-bit process yielding the value -1. If the same expression
is evaluated in a 10-bit process, the result will be 256.

Operator Precedence
-------------------

The operator precedence is inherited from the Python language. The following
table summarizes the operator precedences, from lowest precedence (least
binding) to highest precedence (most binding). Operators in the same row have
the same precedence.

+----------------------+-------------------------------------+
|  Operator            | Description                         |
+======================+=====================================+
| ==, !=, <, <=, >, >= | Comparisons                         | 
+----------------------+-------------------------------------+
| |                    | Bitwise OR                          |
+----------------------+-------------------------------------+
| ^                    | Bitwise XOR                         | 
+----------------------+-------------------------------------+
| &                    | Bitwise AND                         | 
+----------------------+-------------------------------------+
| <<, >>               | Shifts                              |
+----------------------+-------------------------------------+
| +, -                 | Addition and subtraction            | 
+----------------------+-------------------------------------+
| \*, //, %            | multiplication, division and modulo |
+----------------------+-------------------------------------+
| ~                    | bitwise NOT                         |
+----------------------+-------------------------------------+
| Not, abs             | logical NOT, absolute               |
+----------------------+-------------------------------------+

"""

from common import Unique, resize
from instruction import Write, Block
from inspect import currentframe, getsourcefile
from chips_exceptions import ChipsSyntaxError

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

def sign(x):
    return -1 if x < 0 else 1

def c_style_modulo(x, y):
    return sign(x)*(abs(x)%abs(y))

def c_style_division(x, y):
    return sign(x)*sign(y)*(abs(x)//abs(y))

class Process(Unique):

    def __init__(self, bits, *instructions):
        Unique.__init__(self)
        self.instructions = None
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.bits = int(bits)
        self.variables = []
        self.inputs = []
        self.outputs = []
        self.prefetch = {}
        self.timeouts = {}
        self.timer_number = 0
        for i in instructions:
            if not hasattr(i, "set_process"): 
               raise ChipsSyntaxError(
                    (
                        "expecting an instruction " +
                        repr(i) + 
                        " is not an instruction."
                    ),
                    self.filename,
                    self.lineno
                )
            i.set_process(self)
        for i in self.inputs:
            if hasattr(i, "receiver"):
                raise ChipsSyntaxError(
                    "stream already has a receiver", 
                    self.filename, 
                    self.lineno
                )
            if not hasattr(i, "get"): 
               raise ChipsSyntaxError(
                    (
                        "Source must be a stream " +
                        repr(i) + 
                        " is not a stream."
                    ),
                    self.filename,
                    self.lineno
                )
            i.receiver = self
        self.receivers = {}
        self.transmitters = {}
        for i in self.inputs:
            self.transmitters[i.get_identifier()] = i
        for i in self.outputs:
            self.receivers[i.get_identifier()] = i
        self.instructions = tuple(Block(instructions))
        self.instruction_memory = dict(enumerate(self.instructions))

    def set_chip(self, chip):
        if self not in chip.processes:
            chip.processes.append(self)
            for i in self.inputs:
                i.set_chip(chip)

    def is_process(self):
        return True

    def get_bits(self):
        return self.bits

    def write_code(self, plugin): 
        plugin.write_process(self)

    def reset(self):

        self.registers = {}
        self.pc = 0

    def get_data(self, key):
        if (key not in self.prefetch) or (self.prefetch[key] is None):
            self.prefetch[key] = self.transmitters[key].get()
        data = self.prefetch[key]
        self.prefetch[key] = None
        return data

    def peek_data(self, key):
        if (key not in self.prefetch) or (self.prefetch[key] is None):
            self.prefetch[key] = self.transmitters[key].get()
        return self.prefetch[key]

    def execute(self):
        instruction = self.instruction_memory[self.pc]
        if instruction.operation == "OP_ADD":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega+regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_SUB":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega-regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_MUL":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega*regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_DIV":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                c_style_division(rega, regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_MOD":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                c_style_modulo(rega, regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_SL":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega<<regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_SR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega>>regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_ABS":
            rega = self.registers[instruction.srca]
            self.registers[instruction.srca] = resize(abs(rega), self.bits)
            self.pc += 1
        elif instruction.operation == "OP_LNOT":
            rega = self.registers[instruction.srca]
            self.registers[instruction.srca] = resize(not rega, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_INVERT":
            rega = self.registers[instruction.srca]
            self.registers[instruction.srca] = resize(~rega, self.bits)
            self.pc += 1
        elif instruction.operation.startswith("OP_SLN_"):
            rega = self.registers[instruction.srca]
            shift_by = int(instruction.operation[7:])
            self.registers[instruction.srca] = resize(
                    rega<<shift_by, 
                    self.bits
            )
            self.pc += 1
        elif instruction.operation.startswith("OP_SRN_"):
            rega = self.registers[instruction.srca]
            shift_by = int(instruction.operation[7:])
            self.registers[instruction.srca] = resize(
                    rega>>shift_by, 
                    self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_BAND":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega&regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_BOR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega|regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_BXOR":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(rega^regb, self.bits)
            self.pc += 1
        elif instruction.operation == "OP_EQ":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                -int(rega==regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_NE":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                -int(rega!=regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_GT":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                -int(rega>regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_GE":
            rega = self.registers[instruction.srca]
            regb = self.registers[instruction.srcb]
            self.registers[instruction.srca] = resize(
                -int(rega>=regb), 
                self.bits
            )
            self.pc += 1
        elif instruction.operation == "OP_MOVE":
            self.registers[instruction.srca] = self.registers[
                instruction.srcb
            ]
            self.pc += 1
        elif instruction.operation == "OP_IMM":
            self.registers[instruction.srca] = instruction.immediate
            self.pc += 1
        elif instruction.operation == "OP_JMP":
            self.pc = instruction.immediate
        elif instruction.operation == "OP_JMPF":
            if self.registers[instruction.srca]:
                self.pc += 1
            else:
                self.pc = instruction.immediate
        elif instruction.operation.startswith("OP_WRITE"):
            key = instruction.operation[9:]
            receiver = self.receivers[key]
            data = self.registers[instruction.srca]
            receiver.put(resize(data, self.bits))
            self.pc += 1
        elif instruction.operation.startswith("OP_READ"):
            key = instruction.operation[8:]
            read_data = self.get_data(key)
            if read_data is not None:
                self.registers[instruction.srca] = resize(
                    read_data, 
                    self.bits
                )
                self.pc += 1
        elif instruction.operation.startswith("OP_AVAILABLE"):
            key = instruction.operation[13:]
            transmitter = self.transmitters[key]
            read_data = self.peek_data(key)
            if read_data is None:
                self.registers[instruction.srca] = resize(
                    0, 
                    self.bits
                )
            else:
                self.registers[instruction.srca] = resize(
                    -1, 
                    self.bits
                )
            self.pc += 1

    def __repr__(self):
        return '\n'.join([
            "Process(",
            "    bits = {0},".format(self.bits),
            "    instructions = {0},".format(self.instructions),
            ")"
        ])
