from cProfile import label

import Ass_Ast
import IR_code
from IR_code import*
from Ass_Ast import*

class Ass_Generator:
    def __init__(self):
        self.output = ""
    def emit(self,text:str):
        self.output+=text +"\n"
    def generate_ass(self,program:Program):
        self.visit_program(program)
        with open("generated.s",'w') as file:
            file.write(self.output)

    def visit_program(self,program:Program):
        self.visi_function(program.function_definition)
        self.emit(".section .note.GNU-stack,\"\",@progbits")

    def visi_function(self,function:Function):
        self.emit(f".global {function.name}")
        self.emit(f"{function.name}: ")
        self.emit(f"     pushq    %rbp")
        self.emit("     movq   %rsp, %rbp")
        for instruction in function.instructions:
            self.visit_instruction(instruction)

    def visit_instruction(self,instructions:Instruction):
        if isinstance(instructions,list):
            for instruction in instructions:
                self.visit_single_instruction(instruction)
        else:
            self.visit_single_instruction(instructions)
    def visit_single_instruction(self,instruction):
        if isinstance(instruction,Mov):
            self.visit_Mov(instruction)
        elif isinstance(instruction,MovB):
            self.visit_Movb(instruction)
        elif isinstance(instruction,Ret):
            self.visit_ret(instruction)
        elif isinstance(instruction,Ass_Unary):
            self.visit_unary(instruction)
        elif isinstance(instruction,Ass_Binary):
            self.visit_binary(instruction)
        elif isinstance(instruction,Ass_Idiv):
            self.visit_Idiv(instruction)
        elif isinstance(instruction,Ass_Cdq):
            self.visit_cdq()
        elif isinstance(instruction,Ass_Ast.AlocateStack):
            self.visit_allocateStack(instruction)
        elif isinstance(instruction,Ass_Ast.Cmp):
            self.visit_Cmp(instruction)
        elif isinstance(instruction,Ass_Ast.Jmp):
            self.visit_jmp(instruction)
        elif isinstance(instruction,Ass_Ast.JmpCC):
            self.visit_jmpcc(instruction)
        elif isinstance(instruction,Ass_Ast.SetCC):
            self.visit_setcc(instruction)
        elif isinstance(instruction,Label):
            self.visit_label(instruction)
        else:
            raise ValueError(f"Unknown instruction type: {type(instruction)}")
    def visit_allocateStack(self,allocatestack:AlocateStack):
        self.emit(f"     subq   ${allocatestack.pointer}, %rsp")
    def visit_Mov(self,mov:Mov):
        src  = self.visit_operand(mov.src)
        dst  =  self.visit_operand(mov.dst)
        self.emit(f"     movl    {src}, {dst}")
    def visit_Movb(self,mov:MovB):
        src  = self.visit_operand(mov.src)
        dst  =  self.visit_operand(mov.dst)
        self.emit(f"     movb    {src}, {dst}")
    def visit_ret(self,ret:Ret):
        self.emit("     movq    %rbp, %rsp")
        self.emit("     popq    %rbp")
        self.emit("     ret")
    def visit_Cmp(self,cmp:Cmp):
        val1 = self.visit_operand(cmp.val1)
        val2 = self.visit_operand(cmp.val2)
        self.emit(f"cmpl    {val1}, {val2}")
    def visit_jmp(self,jmp:Jmp):
        label = jmp.identifier
        self.emit(f"jmp     .L{label}")
    def visit_jmpcc(self,jmpcc:JmpCC):
        label = jmpcc.identifier
        cond_code = self.visit_cond_code(jmpcc.cond_code)
        self.emit(f"    j{cond_code}       .L{label}")
    def visit_setcc(self,setcc:SetCC):
        cond_code = self.visit_cond_code(setcc.cond_code)
        operand = self.visit_operand(setcc.operand,1)
        self.emit(f"set{cond_code}      {operand}")
    def visit_label(self,label:Label):
        self.emit(f".L{label.identifer}:")
    def visit_unary(self,un:Ass_Unary):
        operator = self.visit_unary_operator(un.operator)
        operand = self.visit_operand(un.operand)
        self.emit(f"     {operator} {operand}")
    def visit_binary(self,binary:Ass_Binary):
        op = self.visi_binary_operator(binary.binary_operator)
        src = self.visit_operand(binary.left)
        dst = self.visit_operand(binary.right)
        self.emit(f"     {op}  {src}, {dst}")
    def visit_Idiv(self,idiv:Ass_Idiv):
        operand = self.visit_operand(idiv.operand)
        self.emit(f"     idivl  {operand}")
    def visit_cdq(self):
        self.emit("     cdq")
    def visit_unary_operator(self,operator):
        if isinstance(operator,Ass_Neg):
            return "negl"
        if isinstance(operator,Ass_Not):
            return "notl"
    def visi_binary_operator(self,operator):
        if isinstance(operator,Ass_Add):
            return "addl"
        if isinstance(operator,Ass_Neg):
            return "subl"
        if isinstance(operator,Ass_Mul):
            return "imull"
        if isinstance(operator,Ass_Bit_And):
            return "andl"
        if isinstance(operator,Ass_Bit_Or):
            return "orl"
        if isinstance(operator,Ass_Bit_Xor):
            return "xorl"
        if isinstance(operator,Ass_Bit_Left_Shift):
            return "shll"
        if isinstance(operator,Ass_Bit_Right_Shift):
            return "sarl"
        else:
            raise ValueError("not recongnised binary_operator in ass_obj")
    def visit_operand(self,operand,one_four = 4 ):
        if isinstance(operand,Register):
            if operand.name == "Ax":
                if one_four == 1:
                    return "%al"
                return "%eax"
            if operand.name == "r10d":
                if one_four == 1:
                    return "%r10b"
                return "%r10d"
            if operand.name == "r11d":
                if one_four == 1:
                    return "%r11b"
                return "%r11d"
            if operand.name == "Dx":
                if one_four == 1:
                    return "%dl"
                return "%edx"
            if operand.name == "cl":
                return  "%cl"
        if isinstance(operand,Ass_Stack):
            return f"{operand.pointer}(%rbp)"
        if isinstance(operand,Imm):
            return f"${operand.value}"
    def visit_cond_code(self,con):
        if con == "E":
            return "e"
        if con == "NE":
            return "ne"
        if con == "L":
            return "l"
        if con == "LE":
            return "le"
        if con == "G":
            return "g"
        if con == "GE":
            return "ge"