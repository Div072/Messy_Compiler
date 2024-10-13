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
class Cond_code():
    def __init__(self,type):
        self.type == type
    def __repr__(self):
        return f"Cond_code {self.type}"
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

class MovB(Instruction):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def __repr__(self):
        return f"Movb({self.src}, {self.dst})"

class Ret():
    def __repr__(self):
        return "Ret()"

class Ass_Unary():
    def __init__(self,unary_operator,operand):
        self.operator = unary_operator
        self.operand = operand
    def __repr__(self):
        return  f"Ass_Unary {self.operator}  {self.operand}"
class Ass_Binary():
    def __init__(self,binary_operator,left,right):
        self.binary_operator = binary_operator
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Ass_Binary {self.left,self.right,self.binary_operator}"

class Cmp():
    def __init__(self,val1,val2):
        self.val1 = val1
        self.val2 = val2
    def __repr__(self):
        return f"Cmp {self.val1} {self.val2}"
class Jmp():
    def __init__(self,identifier):
        self.identifier = identifier
    def __repr__(self):
        return f"Jmp {self.identifier}"
class JmpCC():
    def __init__(self,cond_code,identifier):
        self.cond_code = cond_code
        self.identifier = identifier
    def __repr__(self):
        return f"JmpCC {self.cond_code} {self.identifier}"
class SetCC():
    def __init__(self,cond_code,operand):
        self.cond_code = cond_code
        self.operand = operand
    def __repr__(self):
        return (f"SetCC {self.cond_code} {self.operand}")
class Label():
    def __init__(self,identifer):
        self.identifer = identifer
    def __repr__(self):
        return f"Label {self.identifer}"
class Ass_Idiv():
    def __init__(self,operand):
        self.operand = operand
    def __repr__(self):
        return f"Ass_Idiv {self.operand}"

class Ass_Cdq():
    def __repr__(self):
        return "Ass_Cdq"

class Ass_Neg():
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Neg"
class Ass_Not():
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Not"
class Ass_Add():
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Add"
class Ass_Sub():
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_sub"
class Ass_Mul():
    def __init__(self):
        pass
    def __repr__(self):
        return "Ass_Mul"
class Ass_Bit_And():
    def __repr__(self):
        return "Ass_bit_and"
class Ass_Bit_Or():
    def __repr__(self):
        return "Ass_bit_or"
class Ass_Bit_Xor():
    def __repr__(self):
        return "Ass_bit_xor"
class Ass_Bit_Left_Shift():
    def __repr__(self):
        return "Ass_bit_left_shift"
class Ass_Bit_Right_Shift():
    def __repr__(self):
        return "Ass_bit_right_shift"
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
