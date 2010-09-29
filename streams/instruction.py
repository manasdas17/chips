#!/usr/bin/env python

"""Process machine instructions"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"


################################################################################

class RegisterMap:
    def __init__(self):
        self.tos = 0

################################################################################

class Instruction:
    def __init__(self, operation, srca=None, srcb=None, immediate=None, 
            label=None):
        self.operation = operation
        self.srca = srca
        self.srcb = srcb
        self.immediate = immediate
        self.label = label
    def __repr__(self):
        s = "Instruction(operation={0}, srca={1}, srcb={2}, immediate={3})"
        return s.format(self.operation, self.srca, self.srcb, self.immediate)

################################################################################

def constantise(possible_constant):
    if hasattr(possible_constant, "comp"):
        return possible_constant
    else:
        return Constant(int(possible_constant))

class Expression:
    """Do not directly instantiate this class
    It is here to imbue derived expression classes with operators"""
    def __add__(self, other): return Binary(self, constantise(other), 'OP_ADD')
    def __sub__(self, other): return Binary(self, constantise(other), 'OP_SUB')
    def __mul__(self, other): return Binary(self, constantise(other), 'OP_MUL')
    def __mod__(self, other): return Binary(self, constantise(other), 'OP_MOD')
    def __floordiv__(self, other): return Binary(self, constantise(other), 'OP_DIV')
    def __and__(self, other): return Binary(self, constantise(other), 'OP_BAND')
    def __or__(self, other): return Binary(self, constantise(other), 'OP_BOR')
    def __xor__(self, other): return Binary(self, constantise(other), 'OP_BXOR')
    def __rshift__(self, other): return Binary(self, constantise(other), 'OP_SR')
    def __lshift__(self, other): return Binary(self, constantise(other), 'OP_SL')
    def __eq__(self, other): return Binary(self, constantise(other), 'OP_EQ')
    def __ne__(self, other): return Binary(self, constantise(other), 'OP_NE')
    def __gt__(self, other): return Binary(self, constantise(other), 'OP_GT')
    def __ge__(self, other): return Binary(self, constantise(other), 'OP_GE')
    def __lt__(self, other): return Binary(constantise(other), self, 'OP_GT')
    def __le__(self, other): return Binary(constantise(other), self, 'OP_GE')
    def __radd__(other, self): return Binary(self, constantise(other), 'OP_ADD')
    def __rsub__(other, self): return Binary(self, constantise(other), 'OP_SUB')
    def __rmul__(other, self): return Binary(self, constantise(other), 'OP_MUL')
    def __rmod__(other, self): return Binary(self, constantise(other), 'OP_MOD')
    def __rfloordiv__(other, self): return Binary(self, constantise(other), 'OP_DIV')
    def __rand__(other, self): return Binary(self, constantise(other), 'OP_BAND')
    def __ror__(other, self): return Binary(self, constantise(other), 'OP_BOR')
    def __rxor__(other, self): return Binary(self, constantise(other), 'OP_BXOR')
    def __rrshift__(other, self): return Binary(self, constantise(other), 'OP_SR')
    def __rlshift__(other, self): return Binary(self, constantise(other), 'OP_SL')
    def __req__(other, self): return Binary(self, constantise(other), 'OP_EQ')
    def __rne__(other, self): return Binary(self, constantise(other), 'OP_NE')
    def __rgt__(other, self): return Binary(self, constantise(other), 'OP_GT')
    def __rge__(other, self): return Binary(self, constantise(other), 'OP_GE')
    def __rlt__(other, self): return Binary(constantise(other), self, 'OP_GT')
    def __rle__(other, self): return Binary(constantise(other), self, 'OP_GE')

################################################################################

class Binary(Expression):

    def __init__(self, left, right, operation):
        """Do not directly instantiate this class
        It is created automatically by operators +, -, * ..."""
        self.left = left
        self.right = right
        self.operation = operation

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.left.initialise(rmap)+self.right.initialise(rmap)

    def comp(self, rmap):
        """compile an expression into a list of machine instructions"""
        instructions = self.left.comp(rmap)
        rmap.tos += 1
        instructions.extend(self.right.comp(rmap))
        instructions.extend(
          [Instruction(self.operation, rmap.tos-1, rmap.tos)]
        )
        rmap.tos -= 1
        return instructions

################################################################################

class Variable(Expression):

    def __init__(self, initial):
        """Create a variable

        Accepts one argument, initial.
        The variable gets initiated to this value at reset.
        
        To assign an expression to a variable use the .set() method"""
        self.initial = initial

    def set(self, value):
        """Assign a value to this variable

        Accepts one argument, an expression.
        The expression will be assigned to the variable"""
        return Set(self, value)

    def get_bits(self):
        """Returns the width of the variable.
        
        Remember that variables are signed, so an 8 bit variable can
        accecpt value from -128 to 127 for example."""
        return self.parent.get_bits()

    def __repr__(self):
        """Remember that variables are signed, so an 8 bit variable can
        accecpt value from -128 to 127 for example."""
        return "Variable({0})".format(self.initial)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        if not hasattr(self, "register"):
            self.register = rmap.tos
            rmap.tos+=1
            return [Instruction("OP_IMM", self.register, None, self.initial)]
        else:
            return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return [Instruction("OP_MOVE", rmap.tos, self.register)]

################################################################################

class Constant(Expression):

    def __init__(self, constant):
        """Do not directly call this method, it is called automatically"""
        self.constant = constant

    def __repr__(self):
        return "Constant({0})".format(self.initial)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return [Instruction("OP_LIT", rmap.tos, immediate=self.constant)]

################################################################################

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

class Statement:
    def __iter__(self):
        """Enable an statement to act as a list of machine instructions"""
        rmap = RegisterMap()
        instructions = self.initialise(rmap) + self.comp(rmap)
        instructions = calculate_jumps(instructions)
        return instructions.__iter__()

    def is_loop(self):
        return False

    def get_enclosing_loop(self):
        if self.parent.is_loop():
            return self.parent
        elif hasattr(self.parent, 'parent'):
            return self.parent.get_enclosing_loop()
        else:
            raise SyntaxError()

################################################################################

class Loop(Statement):

    def __init__(self, *instructions):
        for child in instructions:
            child.parent = self
        self.instructions = instructions

    def is_loop(self):
        return True

    def __repr__(self):
        return "Loop({0})".format(self.instruction)

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
        instructions.append(Instruction("LABEL", label = self.start_of_loop))
        for instruction in self.instructions:
            instructions.extend(instruction.comp(rmap))
        instructions.append(Instruction("OP_JMP", immediate = self.start_of_loop)) 
        instructions.append(Instruction("LABEL", label = self.end_of_loop))
        return instructions

################################################################################

class If(Statement):

    def __init__(self, condition, *instructions):
        for child in instructions:
            child.parent = self
        self.conditionals = [(condition, instructions)]

    def Elsif(self, condition, *instructions):
        for child in instructions:
            child.parent = self
        self.conditionals.append((condition, instructions))

    def __repr__(self):
        return "If({0})".format(self.instruction)

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
        for condition, instructions in self.conditionals:
            skip_to_if_false = "SKIP_{0}_{1}".format(id(self), i)
            machine_instructions.extend(condition.comp(rmap))
            machine_instructions.append(Instruction("OP_JMPF", rmap.tos, immediate=skip_to_if_false))
            for instruction in instructions:
                machine_instructions.extend(instruction.comp(rmap))
            machine_instructions.append(Instruction("LABEL", label=skip_to_if_false))
            i+=1
        return machine_instructions

################################################################################

class Break(Statement):

    def __repr__(self):
        return "Break({0})".format(self.instruction)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        end_of_loop = self.get_enclosing_loop().end_of_loop
        return [Instruction("OP_JMP", immediate = end_of_loop)]

################################################################################

class Continue(Statement):

    def __repr__(self):
        return "Continue({0})".format(self.instruction)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return []

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        start_of_loop = self.get_enclosing_loop().start_of_loop
        return [Instruction("OP_JMP", immediate = start_of_loop)]

################################################################################

class Block(Statement):

    def __init__(self, *instructions):
        """A block of statements

        Accepts an arbitrary number of statements as arguments, and executes
        each one in sequeunce"""
        for child in instructions:
            child.parent = self

        for this_ins, next_ins in zip(instructions, instructions[1:]):
            this_ins.next_instruction = next_ins

        self.instructions = instructions

    def what_are_you(self):
        return "Block"

    def __repr__(self):
        return "Block({0})".format(self.instruction)

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

################################################################################

class Set(Statement):
    def __init__(self, variable, expression):
        """Do not instantiate Set directly.
        Use Variable.set() method"""
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return "Set({0}, {1})".format(self.variable, self.other)

    def initialise(self, rmap):
        """Do not directly call this method, it is called automatically"""
        return self.variable.initialise(rmap)+self.expression.initialise(rmap)

    def comp(self, rmap):
        """Do not directly call this method, it is called automatically"""
        instructions = self.expression.comp(rmap)
        instructions.append(
            Instruction("OP_MOVE", self.variable.register, rmap.tos)
        )
        return instructions

