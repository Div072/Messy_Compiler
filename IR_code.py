
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

class Negete(Operator):
    def __repr__(self):
        return "Ircode Negate"
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

