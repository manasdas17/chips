#!/usr/bin/env python
"""insert nops to remove hazards"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright 2010, Jonathan P Dawson"
__license__ = "None"
__version__ = "0.1"
__maintainer__ = "Jon Dawson"
__email__ = "jon@jondawson.org.uk"
__status__ = "Prototype"

from chips.instruction import Instruction

register_modifying_instructions = [
      "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV", "OP_BAND", "OP_BOR", "OP_BXOR", 
      "OP_SL", "OP_SR", "OP_EQ", "OP_NE", "OP_GT", "OP_GE", 
      "OP_IMM", "OP_MOVE", "OP_MOD", "OP_LNOT", "OP_ABS", "OP_INVERT"
    ]

srca_dependent_instructions = [
      "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV", "OP_BAND", "OP_BOR", "OP_BXOR", 
      "OP_SL", "OP_SR", "OP_EQ", "OP_NE", "OP_GT", "OP_GE", 
      "OP_MOD", "OP_LNOT", "OP_ABS", "OP_INVERT", "OP_JMPF"
    ]

srcb_dependent_instructions = [
      "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV", "OP_BAND", "OP_BOR", "OP_BXOR", 
      "OP_SL", "OP_SR", "OP_EQ", "OP_NE", "OP_GT", "OP_GE", 
      "OP_MOVE", "OP_MOD"
    ]

def is_register_modifying(instruction):
    if instruction.operation in register_modifying_instructions:
        return True
    if instruction.operation.startswith("OP_READ"):
        return True
    if instruction.operation.startswith("OP_SLN"):
        return True
    if instruction.operation.startswith("OP_SRN"):
        return True
    if instruction.operation.startswith("OP_AVAILABLE"):
        return True
    return False

def is_srca_dependent(instruction):
    if instruction.operation in srca_dependent_instructions:
        return True
    if instruction.operation.startswith("OP_WRITE"):
        return True
    if instruction.operation.startswith("OP_SLN"):
        return True
    if instruction.operation.startswith("OP_SRN"):
        return True
    return False

def is_srcb_dependent(instruction):
    if instruction.operation in srcb_dependent_instructions:
        return True
    return False

#simlest version, inserts 3 NOOPS after every instruction
#def optimize(instructions):
#
#    #reorder instructions to prevent data hazards
#    new_instructions = []
#    for instruction in instructions:
#        new_instructions.append(instruction)
#        for i in range(2):
#            new_instructions.append(Instruction("OP_NOOP"))
#    return new_instructions

#register aware version adds noops after register modifying instructions
#def optimize(instructions):
#
#    #reorder instructions to prevent data hazards
#    new_instructions = []
#    for instruction in instructions:
#        new_instructions.append(instruction)
#        if is_register_modifying(instruction):
#            for i in range(3):
#                new_instructions.append(Instruction("OP_NOOP"))
#    return new_instructions


#register aware version adds noops if a dependency exists
def optimize(instructions):

    new_instructions = []
    wait_1 = None
    wait_2 = None
    #wait_3 = None

    for instruction in instructions:

        #add wait states until data dependencies are fullfilled
        while True:
            #determine dependencies
            has_dependencies = False
            if is_srca_dependent(instruction):
                if instruction.srca in (wait_1, wait_2):
                    has_dependencies = True
            if is_srcb_dependent(instruction):
                if instruction.srcb in (wait_1, wait_2):
                    has_dependencies = True

            #add waits noops if needed
            if has_dependencies:
                new_instructions.append(Instruction("OP_NOOP"))
                wait_1 = wait_2
                wait_2 = None
                continue
            else:
                break

        #add the instruction
        new_instructions.append(instruction)

        #modify state of data availability
        wait_1 = wait_2
        wait_2 = None
        if is_register_modifying(instruction):
            wait_2 = instruction.srca 

        new_instructions.append(Instruction("OP_NOOP"))
        new_instructions.append(Instruction("OP_NOOP"))

    return new_instructions
