
from typing import List, Union
from IR_code import Operator


class Operand:
    pass

class Imm(Operand):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Imm({self.value})"

class Register(Operand):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"Register({self.name})"
class Ass_reg(Register):
    def __init__(self,type):
        self.type = type
    def __repr__(self):
        return f"register type {self.type}"
class Pseudo(Operator):
    def __init__(self,identifier):
        self.identifier = identifier
    def __repr__(self):
        return "Pseudo"
class Ass_Stack(Operator):
    def __init__(self,pointer):
        self.pointer = pointer
    def __repr__(self):
        return  f"Ass_Stack {self.pointer}"

class Instruction:
    pass

class Mov(Instruction):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def __repr__(self):
        return f"Mov({self.src}, {self.dst})"

class Ret(Instruction):
    def __repr__(self):
        return "Ret()"

class Ass_Unary(Instruction):
    def __init__(self,unary_operator,operand):
        self.operator = unary_operator
        self.operand = operand
    def __repr__(self):
        return  f"Ass_Unary {self.operator}  {self.operand}"

class Ass_Neg(Ass_Unary):
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Neg"
class Ass_Not(Ass_Unary):
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Not"

class AlocateStack():
    def __init__(self,val):
        self.pointer = val
    def __repr__(self):
        return "AllocateStack"
class Function:
    def __init__(self, name: str, instructions: List[Instruction]):
        self.name = name
        self.instructions = instructions

    def __repr__(self):
        return f"Function({self.name}, {self.instructions})"

class Program:
    def __init__(self, function_definition):
        self.function_definition = function_definition

    def __repr__(self):
        return f"Program({self.function_definition})"
