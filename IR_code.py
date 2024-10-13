
class Program:
    def __init__(self,function_defination):
        self.fun_defination= function_defination
    def __repr__(self):
        return f"Program {self.fun_defination}"

class Fun_ction:
    def __init__(self,identifier,instructions:[]):
        self.identifier = identifier
        self.instructions = instructions
    def __repr__(self):
        return f"Function {self.identifier} {self.instructions}"

class Instruction(Fun_ction):
    pass

class Ret():
    def __init__(self,val):
        self.val = val
    def __repr__(self):
        return f"Return ()"

class Operator:
    pass

class Complement(Operator):
    def __repr__(self):
        return "Ircode Complement"
class Not(Operator):
    def __repr__(self):
        return "Not"
class Negete(Operator):
    def __repr__(self):
        return "Ircode Negate"
class Add(Operator):
    def __repr__(self):
        return "Add"
class Subtract(Operator):
    def __repr__(self):
        return "Subtract"
class Multiply():
    def __repr__(self):
        return "Multiply"
class Divide(Operator):
    def __repr__(self):
        return "Divide"
class Remainder(Operator):
    def __repr__(self):
        return "remainder"
class Bit_Or(Operator):
    def __repr__(self):
        return"bit_or"
class Bit_And(Operator):
    def __repr__(self):
        return "bit_and"
class Bit_Xor(Operator):
    def __repr__(self):
        return "Bit_xor"
class Left_Shift(Operator):
    def __repr__(self):
        return "left_Shift"
class Right_Shift(Operator):
    def __repr__(self):
        return "Right_Shift"
class Greater(Operator):
    def __repr__(self):
        return "Greater"
class Less(Operator):
    def __repr__(self):
        return "Less"
class GreaterEqual(Operator):
    def __repr__(self):
        return "GreaterEqual"
class LessEqual(Operator):
    def __repr__(self):
        return "LessEqual"
class Equal_Equal(Operator):
    def __repr__(self):
        return "Equal_Equal"
class Not_Equal(Operator):
    def __repr__(self):
        return "Not_Equal"
class Val:
    pass
# it generates ir value like
# temp = a + b
# c = temp
class Variable(Val):
    def __init__(self,identifier,value=None):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return "variable"
class Const(Val):
    def __init__(self,const):
        self.const = const

    def __repr__(self):
        return"const"

class U_nary():
    def __init__(self,operator:Operator,src:Val,ds:Val):
        self.operator = operator
        self.src = src
        self.ds = ds
    def __repr__(self):
        return"U_nary"
class B_inary():
    def __init__(self,operator:Operator,src1:Val,src2:Val,dst:Val):
        self.operator = operator
        self.src1 = src1
        self.src2 = src2
        self.dst = dst
    def __repr__(self):
        return "B_inary"

class Copy():
    def __init__(self,src:Val,dst:Val):
        self.src = src
        self.dst = dst
    def __repr__(self):
        return "Copy()"

class Jump():
    def __init__(self,target):
        self.target = target
    def __repr__(self):
        return"Jump"
class JumpIfZero():
    def __init__(self,condition,identifier):
        self.condition = condition
        self.identifier = identifier
    def __repr__(self):
        return"JumpIfZero"
class JumpIfNotZero():
    def __init__(self,condition,identifier):
        self.condition = condition
        self.identifier = identifier
    def __repr__(self):
        return "Jumpifnotzero"
class Label():
    def __init__(self,identifier):
        self.identifier = identifier
    def __repr__(self):
        return "Label"
