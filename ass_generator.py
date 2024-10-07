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
        print(self.output)
        with open("generated.s",'w') as file:
            file.write(self.output)


    def visit_program(self,program:Program):
        self.visi_function(program.function_definition)
        self.emit(".section .note.GNU-stack,\"\",@progbits")

    def visi_function(self,function:Function):
        self.emit(f".global {function.name}")
        self.emit(f"{function.name}: ")
        self.emit(f"  pushq    %rbp")
        self.emit("  movq   %rsp, %rbp")
        for instruction in function.instructions:
            self.visit_instruction(instruction)
    def visit_instruction(self,instructions:Instruction):
        for instruction in instructions:
            if isinstance(instruction,Mov):
                self.visit_Mov(instruction)
            elif isinstance(instruction,Ret):
                self.visit_ret(instruction)
            elif isinstance(instruction,Ass_Unary):
                self.visit_unary(instruction)
            elif isinstance(instruction,Ass_Ast.AlocateStack):
                self.visit_allocateStack(instruction)
            else:
                raise ValueError(f"Unknown instruction type: {type(instruction)}")
    def visit_allocateStack(self,allocatestack:AlocateStack):
        self.emit(f"subq   ${allocatestack.pointer}, %rsp")
        pass
    def visit_Mov(self,mov:Mov):
        src  = self.visit_operand(mov.src)
        dst  =  self.visit_operand(mov.dst)
        self.emit(f"    movl    {src}, {dst}")
    def visit_ret(self,ret:Ret):
        self.emit("    movq    %rbp, %rsp")
        self.emit("    popq    %rbp")
        self.emit("    ret")
    def visit_unary(self,un:Ass_Unary):
        operator = self.visit_unary_operator(un.operator)
        operand = self.visit_operand(un.operand)
        self.emit(f"{operator}  {operand}")

    def visit_unary_operator(self,operator):
        if isinstance(operator,Ass_Neg):
            return "negl"
        if isinstance(operator,Ass_Not):
            return "notl"
    def visit_operand(self,operand):
        if isinstance(operand,Register):
            if operand.name == "eax":
                return "%eax"
            if operand.name == "r10d":
                return "%r10d"
        if isinstance(operand,Ass_Stack):
            return f"{operand.pointer}(%rbp)"
        if isinstance(operand,Imm):
            return f"${operand.value}"


