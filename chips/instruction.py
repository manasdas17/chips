#!/usr/bin/env python

""" The instructions provided here form the basis of the software that can be run inside *Processes*."""

from inspect import currentframe, getsourcefile
from chips_exceptions import ChipsSyntaxError

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "chips@jondawson.org.uk"
__status__ = "Prototype"

class Statement:
    def __iter__(self):
        """Enable an statement to act as a list of machine instructions"""
        rmap = RegisterMap()
        rmap.tos += 1 #reserve location 0 for evaluate blocks
        instructions = self.initialise(rmap) + self.comp(rmap)
        instructions.append(Instruction("LABEL", label="END"))
        instructions.append(Instruction("OP_JMP", immediate="END"))
        instructions.append(Instruction("OP_JMP", immediate=0))
        instructions = calculate_jumps(instructions)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        return instructions.__iter__()

    def is_loop(self):
        return False

    def is_process(self):
        return False

    def is_eval(self):
        return False

    def is_statement(self):
        return True

    def get_enclosing_loop(self):
        if self.parent.is_loop():
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.get_enclosing_loop()
        else:
            raise ChipsSyntaxError(
                "Break() must be within a loop", 
                self.filename, 
                self.lineno
            )

    def get_enclosing_eval(self):
        if self.parent.is_eval():
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.get_enclosing_eval()
        else:
            raise ChipsSyntaxError(
                "Value() must be within a evaluate block",
                self.filename, 
                self.lineno
            )


class Read(Statement):
    def __init__(self, stream, variable):
        """Do not directly call this method, it is called automatically
         Use stream.read(variable)"""
        self.variable = variable
        self.stream = stream
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

        _test_variable(variable, self)
        _test_stream(stream, self)

    def set_process(self, process):
        #have to explicitly test for identity because we have overridden __eq__
        for i in process.inputs:
            if i is self.stream: break
        else:
            process.inputs.append(self.stream)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.variable.initialise(rmap)

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = [
          Instruction(
              "OP_READ_{0}".format(
                  self.stream.get_identifier()
              ), 
              srca=self.variable.register, 
              lineno=self.lineno, 
              filename=self.filename
          ) 
        ]
        return instructions

class Write(Statement):
    def __init__(self, stream, expression):
        """Do not directly call this method, it is called automatically
         Use stream.write(expression)"""
        self.expression = constantize(expression)
        self.stream = stream
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

        _test_expression(self.expression, self)
        _test_stream(self.stream, self)

    def set_process(self, process):
        self.process=process
        self.stream.set_process(process)
        self.expression.set_process(process)
        #have to explicitly test for identity because we have overridden __eq__
        for i in process.outputs:
            if i is self.stream: break
        else:
            process.outputs.append(self.stream)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.expression.initialise(rmap)

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = self.expression.comp(rmap)
        instructions.append(
          Instruction("OP_WRITE_{0}".format(
              self.stream.get_identifier()), 
              srca=rmap.tos, 
              lineno=self.lineno, 
              filename=self.filename
          ) 
        )
        return instructions


class RegisterMap:
    def __init__(self):
        self.tos = 0

class Instruction:
    def __init__(self, operation, srca=None, srcb=None, immediate=None, 
            label=None, lineno=None, filename=None):
        self.operation = operation
        self.srca = srca
        self.srcb = srcb
        self.immediate = immediate
        self.label = label
        self.filename = filename
        self.lineno = lineno
    def __repr__(self):
        s = "Instruction(operation={0}, srca={1}, srcb={2}, immediate={3})"
        return s.format(
            self.operation, 
            self.srca, 
            self.srcb, 
            self.immediate
        )

def constantize(possible_constant):
    if hasattr(possible_constant, "comp"):
        return possible_constant
    else:
        return Constant(int(possible_constant))

class Expression:
    """Do not directly instantiate this class
    It is here to imbue derived expression classes with operators"""
    def __invert__(self): 
        return Unary(self, 'OP_INVERT')
    def __abs__(self): 
        return Unary(self, 'OP_ABS')
    def Not(self): 
        return Unary(self, 'OP_LNOT')
    def shift_left(self, n): 
        return Unary(self, 'OP_SLN_{0}'.format(n))
    def shift_right(self, n): 
        return Unary(self, 'OP_SRN_{0}'.format(n))
    def __add__(self, other): 
        return Binary(self, constantize(other), 'OP_ADD')
    def __sub__(self, other): 
        return Binary(self, constantize(other), 'OP_SUB')
    def __mul__(self, other): 
        return Binary(self, constantize(other), 'OP_MUL')
    def __mod__(self, other): 
        return Binary(self, constantize(other), 'OP_MOD')
    def __floordiv__(self, other): 
        return Binary(self, constantize(other), 'OP_DIV')
    def __and__(self, other): 
        return Binary(self, constantize(other), 'OP_BAND')
    def __or__(self, other): 
        return Binary(self, constantize(other), 'OP_BOR')
    def __xor__(self, other): 
        return Binary(self, constantize(other), 'OP_BXOR')
    def __rshift__(self, other): 
        return Binary(self, constantize(other), 'OP_SR')
    def __lshift__(self, other): 
        return Binary(self, constantize(other), 'OP_SL')
    def __eq__(self, other): 
        return Binary(self, constantize(other), 'OP_EQ')
    def __ne__(self, other): 
        return Binary(self, constantize(other), 'OP_NE')
    def __gt__(self, other): 
        return Binary(self, constantize(other), 'OP_GT')
    def __ge__(self, other): 
        return Binary(self, constantize(other), 'OP_GE')
    def __lt__(self, other): 
        return Binary(constantize(other), self, 'OP_GT')
    def __le__(self, other): 
        return Binary(constantize(other), self, 'OP_GE')
    def __radd__(self, other): 
        return Binary(constantize(other), self, 'OP_ADD')
    def __rsub__(self, other): 
        return Binary(constantize(other), self, 'OP_SUB')
    def __rmul__(self, other): 
        return Binary(constantize(other), self, 'OP_MUL')
    def __rmod__(self, other): 
        return Binary(constantize(other), self, 'OP_MOD')
    def __rfloordiv__(self, other): 
        return Binary(constantize(other), self, 'OP_DIV')
    def __rand__(self, other): 
        return Binary(constantize(other), self, 'OP_BAND')
    def __ror__(self, other): 
        return Binary(constantize(other), self, 'OP_BOR')
    def __rxor__(self, other): 
        return Binary(constantize(other), self, 'OP_BXOR')
    def __rrshift__(self, other): 
        return Binary(constantize(other), self, 'OP_SR')
    def __rlshift__(self, other): 
        return Binary(constantize(other), self, 'OP_SL')
    def __req__(self, other): 
        return Binary(constantize(other), self, 'OP_EQ')
    def __rne__(self, other): 
        return Binary(constantize(other), self, 'OP_NE')
    def __rgt__(self, other): 
        return Binary(constantize(other), self, 'OP_GT')
    def __rge__(self, other): 
        return Binary(constantize(other), self, 'OP_GE')
    def __rlt__(self, other): 
        return Binary(self, constantize(other), 'OP_GT')
    def __rle__(self, other): 
        return Binary(self, constantize(other), 'OP_GE')
    def is_expression(self):
        return True

class UserDefinedExpression(Expression):
    
    def set_process(self, process):
        self.process = process
        self.instructions = self.on_evaluate()
        for i in self.instructions:
            i.set_process(process)
        
    def on_evaluate(self):
        """Users should override this function
        it should return an Expression object"""
        return Constant(0)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions =  []
        for instruction in self.instructions:
            instructions.extend(instruction.initialise(rmap))
        return instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        return instructions

class Available(Expression):
    def __init__(self, stream):
        """Do not directly call this method, it is called automatically
         Use stream.available()"""
        self.stream = stream
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        _test_stream(stream, self)

    def set_process(self, process):
        self.process = process

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = [
          Instruction("OP_AVAILABLE_{0}".format(
                  self.stream.get_identifier()
              ), 
              srca=rmap.tos,
              lineno=self.lineno, 
              filename=self.filename
          ) 
        ]
        return instructions

class Evaluate(Expression):

    def __init__(self, *instructions):
        """Define a block of code that can be treated as an expression"""
        self.instructions = instructions
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        for child in instructions:
            _test_instruction(child, self)
            child.parent = self

    def set_process(self, process):
        for i in self.instructions:
            i.set_process(process)

    def is_eval(self):
        return True

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.initialise(rmap))
        return instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        self.end_of_eval = "END_{0}".format(id(self))
        instruction = []
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        instructions.append(Instruction("LABEL", label = self.end_of_eval, lineno=self.lineno, filename=self.filename))
        instructions.append(Instruction("OP_MOVE", rmap.tos, 0, lineno=self.lineno, filename=self.filename))
        return instructions

class Binary(Expression):

    def __init__(self, left, right, operation):
        """Do not directly instantiate this class
        It is created automatically by operators +, -, * ..."""
        self.left = constantize(left)
        self.right = constantize(right)
        self.operation = operation
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        _test_expression(self.left, self)
        _test_expression(self.right, self)

    def set_process(self, process):
        self.process=process
        self.left.set_process(process)
        self.right.set_process(process)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.left.initialise(rmap)+self.right.initialise(rmap)

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = self.left.comp(rmap)
        rmap.tos += 1
        instructions.extend(self.right.comp(rmap))
        instructions.extend(
            [
                Instruction(
                    self.operation, 
                    rmap.tos-1, 
                    rmap.tos, 
                    lineno=self.lineno, 
                    filename=self.filename
                )
            ]
        )
        rmap.tos -= 1
        return instructions

class Unary(Expression):

    def __init__(self, right, operation, constant=0):
        """Do not directly instantiate this class
        It is created automatically by operators ~, abs() ..."""
        self.right = right
        self.operation = operation
        self.constant = constant
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        _test_expression(self.right, self)

    def set_process(self, process):
        self.process=process
        self.right.set_process(process)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.right.initialise(rmap)

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = self.right.comp(rmap)
        instructions.extend(
            [
                Instruction(
                    self.operation, 
                    rmap.tos, 
                    lineno=self.lineno, 
                    filename=self.filename
                )
            ]
        )
        return instructions

class Variable(Expression):
    """A *Variable* is used within a *Process* to store data. A *Variable* can
    be used in only one *Process*. If you need to communicate with another
    *Process* you must use a stream. 

    A *Variable* accepts a single argument, the initial value. A *Variable*
    will be reset to the initial value when a simulation, or actual device is
    reset.

    A *Variable* can be assigned an expression using the *set* method.
    
    """

    def __init__(self, initial):
        """Create a variable

        Accepts one argument, initial.
        The variable gets initiated to this value at reset.
        
        To assign an expression to a variable use the .set() method"""
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        self.initial = int(initial)

    def set(self, value):
        """Assign a value to this variable

        Accepts one argument, an expression.
        The expression will be assigned to the variable"""
        return Set(self, value)

    def get_bits(self):
        """Returns the width of the variable.
        
        Remember that variables are signed, so an 8 bit variable can
        accept value from -128 to 127 for example."""
        return self.parent.get_bits()

    def set_process(self, process):
        self.process=process
        #have to explicitly test for identity because we have overridden __eq__
        for i in process.variables:
            if i is self: break
        else:
            process.variables.append(self)

    def __repr__(self):
        """Remember that variables are signed, so an 8 bit variable can
        accept value from -128 to 127 for example."""
        return "Variable({0})".format(self.initial)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        if not hasattr(self, "register"):
            self.register = rmap.tos
            rmap.tos+=1
            return [
                Instruction(
                    "OP_IMM", 
                    self.register, 
                    None, 
                    self.initial,
                    lineno=self.lineno, 
                    filename=self.filename
                )
            ]
        else:
            return []

    def is_variable(self):
        return True

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return [
            Instruction(
                "OP_MOVE", 
                rmap.tos, 
                self.register, 
                lineno=self.lineno, 
                filename=self.filename
            )
        ]

class Constant(Expression):

    def __init__(self, constant):
        """Do not directly call this method, it is called automatically"""
        self.constant = int(constant)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

    def __repr__(self):
        return "Constant({0})".format(self.constant)

    def set_process(self, process):
        self.process=process

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return [
            Instruction(
                "OP_IMM", 
                rmap.tos, 
                immediate=self.constant, 
                lineno=self.lineno, 
                filename=self.filename
            )
        ]

def calculate_jumps(instructions):
    address = 0
    new_instructions = []
    labels = {}

    for instruction in instructions:
        if instruction.label:
            labels[instruction.label] = address
        else:
            address += 1
            new_instructions.append(instruction)

    for instruction in new_instructions:
        if type(instruction.immediate) is str:
            instruction.immediate = labels[instruction.immediate]

    return new_instructions

class Value(Statement):
    """

    The *Value* statement gives a value to the surrounding *Evaluate*
    construct.
    
    An *Evaluate*  expression allows a block of statements to be used as an
    expression. When a *Value* is encountered, the supplied expression becomes
    the value of the whole evaluate statement.

    Example::

        >>> from chips import *

        >>> #provide a And expression similar to Pythons and expression
        >>> def LogicalAnd(a, b):
        ...     return Evaluate(
        ...         If(a,
        ...             Value(b),
        ...         ).Else(
        ...             Value(0),
        ...         )
        ...     )

        >>> check = Output()
        >>> Process(8,
        ...     If(LogicalAnd(1, 4),
        ...         check.write(-1),#true
        ...     ).Else(
        ...         check.write(0),#false
        ...     )
        ... )
        Process(...

        >>> c = Chip(Asserter(check))
        >>> c.reset()
        >>> c.execute(100)


    """
    def __init__(self, expression):
        """Set the value of an evaluate block, and cease execution of the block"""
        self.expression = constantize(expression)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        _test_expression(self.expression, self)

    def __repr__(self):
        return "Value()"

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.expression.initialise(rmap)

    def set_process(self, process):
        self.process=process
        self.expression.set_process(process)

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        end_of_eval = self.get_enclosing_eval().end_of_eval
        instructions = self.expression.comp(rmap)
        instructions.append(
            Instruction(
                "OP_MOVE", 
                0, 
                rmap.tos, 
                lineno=self.lineno, 
                filename=self.filename
            )
        )
        instructions.append(
            Instruction(
                "OP_JMP", 
                immediate = end_of_eval, 
                lineno=self.lineno, 
                filename=self.filename
            )
        )
        return instructions

class Loop(Statement):
    """

    The *Loop* statement executes instructions repeatedly.
    
    A *Loop* can be exited using the *Break* instruction. A *Continue*
    instruction causes the remainder of instructions in the loop to be skipped.
    Execution then repeats from the beginning of the *Loop*.

    Example::

        >>> from chips import *

        >>> #filter values over 50 out of a stream
        >>> in_stream = Sequence(10, 20, 30, 40, 50, 60, 70, 80, 90)
        >>> out_stream = Output()
        >>> a = Variable(0)
        >>> Process(8,
        ...     Loop(
        ...         in_stream.read(a),
        ...         If(a > 50, Continue()),
        ...         out_stream.write(a),
        ...     )
        ... )
        Process(...

        >>> c = Chip(
        ...     Console(
        ...         Printer(out_stream)
        ...     )
        ... )

        >>> c.reset()
        >>> c.execute(100)
        10
        20
        30
        40
        50
        10
        ...



    Example::

        >>> from chips import *

        >>> #initialise an array
        >>> myarray = VariableArray(100)
        >>> index = Variable(0)
        >>> Loop(
        ...     If(index == 100,
        ...         Break(),
        ...     ),
        ...     myarray.write(index, 0),
        ... )
        Loop(...

    """

    def __init__(self, *instructions):
        self.instructions = instructions
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        for child in self.instructions:
            child.parent = self
            _test_instruction(child, self)

    def is_loop(self):
        return True

    def __repr__(self):
        return "Loop({0})".format(self.instructions)

    def set_process(self, process):
        self.process=process
        for i in self.instructions:
            i.set_process(process)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.initialise(rmap))
        return instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        self.start_of_loop = "START_{0}".format(id(self))
        self.end_of_loop = "END_{0}".format(id(self))
        instructions.append(
            Instruction(
                "LABEL", 
                label = self.start_of_loop, 
                lineno=self.lineno, 
                filename=self.filename
            )
        )
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        instructions.append(
            Instruction(
                "OP_JMP", 
                immediate = self.start_of_loop, 
                lineno=self.lineno, 
                filename=self.filename
            )
        ) 
        instructions.append(
            Instruction(
                "LABEL", 
                label = self.end_of_loop, 
                lineno=self.lineno, 
                filename=self.filename
            )
        )
        return instructions

class If(Statement):
    """

    The *If* statement conditionally executes instructions.

    The condition of the *If* branch is evaluated, followed by the condition of
    each of the optional *Elif* branches. If one of the conditions evaluates
    to non-zero then the corresponding instructions will be executed. If the
    *If* condition, and all of the *Elif* conditions evaluate to zero, then
    the instructions in the optional *Else* branch will be evaluated.

    Example::

        If(condition,
            #do something
        ).Elif(condition,
            #do something else
        ).Else(
            #if all else fails do this
        )

    """
        

    def __init__(self, condition, *instructions):
        condition = constantize(condition)
        self.conditionals = [(condition, instructions)]
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno
        _test_expression(condition, self)

        for child in instructions:
            child.parent = self
            _test_instruction(child, self)

    def Elif(self, condition, *instructions):
        for child in instructions:
            _test_instruction(child, self)
            child.parent = self

        self.conditionals.append((constantize(condition), instructions))
        return self

    def Else(self, *instructions):
        return self.Elif(-1, *instructions)

    def set_process(self, process):
        self.process=process
        for condition, instructions in self.conditionals:
            condition.set_process(process)
            for instruction in instructions:
                instruction.set_process(process)

    def __repr__(self):
        return "If({0})".format(self.conditionals)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        machine_instructions = []
        for condition, instructions in self.conditionals:
            machine_instructions.extend(condition.initialise(rmap))
            for instruction in instructions:
                machine_instructions.extend(instruction.initialise(rmap))
        return machine_instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        machine_instructions = []
        i = 0
        skip_to_end = "SKIP_{0}".format(id(self))
        for condition, instructions in self.conditionals:
            skip_to_if_false = "SKIP_{0}_{1}".format(id(self), i)
            machine_instructions.extend(condition.comp(rmap))
            machine_instructions.append(
                Instruction(
                    "OP_JMPF", 
                    rmap.tos, 
                    immediate=skip_to_if_false
                )
            )
            for instruction in instructions:
                machine_instructions.extend(instruction.comp(rmap))
            machine_instructions.append(
                Instruction(
                    "OP_JMP", 
                    immediate=skip_to_end
                )
            )
            machine_instructions.append(
                Instruction(
                    "LABEL", 
                    label=skip_to_if_false
                )
            )
            i+=1
        machine_instructions.append(Instruction("LABEL", label=skip_to_end))
        return machine_instructions

class Break(Statement):
    """

    The *Break* statement causes the flow of control to immediately exit the loop.

    Example::

        #equivalent to a While loop
        Loop(
            If(Not(condition),
                Break(),
            ),
            #do stuff here
        ),

    Example::

        #equivalent to a DoWhile loop
        Loop(
            #do stuff here
            If(Not(condition),
                Break(),
            ),
        ),
        
    """

    def __init__(self):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

    def __repr__(self):
        return "Break()"

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def set_process(self, process):
        self.process=process

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        end_of_loop = self.get_enclosing_loop().end_of_loop
        return [
            Instruction(
                "OP_JMP", 
                immediate = end_of_loop, 
                lineno=self.lineno, 
                filename=self.filename
            )
        ]

class WaitUs(Statement):
    """

    *WaitUs* causes execution to halt until the next tick of the microsecond
    timer. 

    In practice, this means that the process is stalled for less than 1
    microsecond. This behaviour is useful when implementing a real-time
    counter function because the execution time of statements does not affect
    the time between *WaitUs* statements (Providing the statements do not take
    more than 1 microsecond to execute of course!).

    Example::

        >>> from chips import *

        >>> seconds = Variable(0)
        >>> count = Variable(0)
        >>> out_stream = Output()
        >>> Process(12,
        ...     seconds.set(0),
        ...     Loop(
        ...         count.set(1000),
        ...         While(count,
        ...             WaitUs(),
        ...             count.set(count-1),
        ...         ),
        ...         seconds.set(seconds + 1),
        ...         out_stream.write(seconds),
        ...     ),
        ... )
        Process(...
        
    """
    def __init__(self):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

    def __repr__(self):
        return "WaitUs({0})".format(self.clock_cycles)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def set_process(self, process):
        self.process=process

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return [
            Instruction(
                "OP_WAIT_US", 
                lineno=self.lineno, 
                filename=self.filename
            )
        ]

class Continue(Statement):
    """

    The *Continue* statement causes the flow of control to immediately jump to
    the next iteration of the containing loop.

    Example::

        >>> from chips import *

        >>> in_stream = Counter(0, 100, 1)
        >>> out_stream = Output()
        >>> a = Variable(0)
        >>> #allow only even numbers
        >>> Process(12,
        ...     Loop(
        ...         in_stream.read(a),
        ...         If(a&1,
        ...             Continue(),
        ...         ),
        ...         out_stream.write(a),
        ...     ),
        ... )
        Process(...
        
        >>> c = Chip(Console(Printer(out_stream)))
        >>> c.reset()
        >>> c.execute(100)
        0
        2
        4
        6
        8
        ...
        
    """

    def __init__(self):
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

    def __repr__(self):
        return "Continue()".format(self.instruction)

    def set_process(self, process):
        self.process=process

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        start_of_loop = self.get_enclosing_loop().start_of_loop
        return [
            Instruction(
                "OP_JMP", 
                immediate = start_of_loop, 
                lineno=self.lineno, 
                filename=self.filename
            )
        ]

class UserDefinedStatement(Statement):

    def set_process(self, process):
        self.process = process
        self.instructions = self.on_execute()
        for i in self.instructions:
            i.set_process(process)
        
    def on_execute(self):
        """Users should override this function
        it should return a statement object"""
        return Block(tuple())

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions =  []
        for instruction in self.instructions:
            instructions.extend(instruction.initialise(rmap))
        return instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        return instructions

class Block(Statement):
    """

    The *Block* statement allows instructions to be nested into a single
    statement. Using a *Block* allows a group of instructions to be stored as a
    single object. A block accepts a single argument, *instructions*, a Python
    Sequence of instructions

    Example::

        >>> from chips import *

        >>> a = Variable(0)
        >>> b = Variable(1)
        >>> c = Variable(2)

        >>> initialise = Block((a.set(0), b.set(0), c.set(0)))
        >>> Process(8,
        ...     initialise,
        ...     a.set(a+1), b.set(b+1), c.set(c+1),
        ... )
        Process(...
        
    """

    def __init__(self, instructions):
        """A block of statements

        Accepts an arbitrary number of statements as arguments, and executes
        each one in sequence"""

        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

        for child in instructions:
            child.parent = self
            _test_instruction(child, self)

        for this_ins, next_ins in zip(instructions, instructions[1:]):
            this_ins.next_instruction = next_ins

        self.instructions = instructions

    def set_process(self, process):
        self.process=process
        for i in self.instructions:
            i.set_process(process)

    def what_are_you(self):
        return "Block"

    def __repr__(self):
        return "Block({0})".format(self.instructions)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.initialise(rmap))
        return instructions

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = []
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        return instructions

class Set(Statement):
    def __init__(self, variable, expression):
        """Do not instantiate Set directly.
        Use Variable.set() method"""
        self.variable = variable
        self.expression = constantize(expression)
        self.filename = getsourcefile(currentframe().f_back)
        self.lineno = currentframe().f_back.f_lineno

        _test_expression(self.expression, self)
        _test_variable(self.variable, self)

    def __repr__(self):
        return "Set({0}, {1})".format(self.variable, self.expression)

    def set_process(self, process):
        self.process=process
        self.expression.set_process(process)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.variable.initialise(rmap)+\
           self.expression.initialise(rmap)

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = self.expression.comp(rmap)
        instructions.append(
            Instruction(
                "OP_MOVE", 
                self.variable.register, 
                rmap.tos, 
                lineno=self.lineno, 
                filename=self.filename
            )
        )
        return instructions

def _test_variable(variable, self):

    if ((not hasattr(variable, "is_variable")) or
            (not variable.is_variable())):

            raise ChipsSyntaxError(
                (
                    "Expected a variable."+
                    repr(expression)+
                    " is not a variable."
                ),
                self.filename,
                self.lineno
            )

def _test_expression(expression, self):

    if ((not hasattr(expression, "is_expression")) or
            (not expression.is_expression())):

            raise ChipsSyntaxError(
                (
                    "Expected a expression."+
                    repr(expression)+
                    " is not a expression."
                ),
                self.filename,
                self.lineno
            )

def _test_instruction(statement, self):

    if ((not hasattr(statement, "is_statement")) or
            (not statement.is_statement())):

            raise ChipsSyntaxError(
                (
                    "Expected a statement."+
                    repr(statement)+
                    " is not a statement."
                ),
                self.filename,
                self.lineno
            )

def _test_stream(stream, self):

    if not hasattr(stream, "get"):

            raise ChipsSyntaxError(
                (
                    "Expected a stream."+
                    repr(stream)+
                    " is not a stream."
                ),
                self.filename,
                self.lineno
            )

