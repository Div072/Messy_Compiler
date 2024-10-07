import Ass_Ast
import IR_code
from IR_code import*
from Ass_Ast import*

stack_map = {}
stack_pointer = 0
def get_stack_pointer(keyword):
    if keyword in stack_map:
        return stack_map[keyword]
def initiate_pointer(keyword,value):
    stack_map[keyword] = value
stack = Ass_Stack(0)

def convert_ast_to_assembly(Ir_ast_node) -> Union[Program, Function]:
    if isinstance(Ir_ast_node,IR_code.Program):

        function_def = convert_ast_to_assembly(Ir_ast_node.fun_defination)
        return Program(function_def)

    if isinstance(Ir_ast_node, IR_code.Fun_ction):
        instructions = []
        for instr in Ir_ast_node.instructions:
            for item in instr:
                instructions.append(convert_ast_to_assembly(item))
        return Function(Ir_ast_node.identifier, instructions)

    if isinstance(Ir_ast_node, IR_code.Ret):
        return [
            Mov(convert_ast_to_assembly(Ir_ast_node.val), Register("eax")),
            Ret()
        ]
    if isinstance(Ir_ast_node,IR_code.U_nary):
        return[
            Mov(convert_ast_to_assembly(Ir_ast_node.src),convert_ast_to_assembly(Ir_ast_node.ds)),
            Ass_Unary(convert_ast_to_assembly(Ir_ast_node.operator),convert_ast_to_assembly(Ir_ast_node.ds))
        ]
    if isinstance(Ir_ast_node,IR_code.Variable):
        return Pseudo(Ir_ast_node.identifier)
    if isinstance(Ir_ast_node,IR_code.Const):
        return Imm(Ir_ast_node.const)
    if isinstance(Ir_ast_node,IR_code.Complement):
        return Ass_Not()
    if isinstance(Ir_ast_node,IR_code.Negete):
        return Ass_Neg()

    raise ValueError("Unknown AST node type")
#TODO: need to replace pseudoregisters with stack(int) in second traverse
def second_pass_traverse(ass_obj):
    if isinstance(ass_obj,Ass_Ast.Program):
        second_pass_traverse(ass_obj.function_definition)
        return
    if isinstance(ass_obj,Ass_Ast.Function):
        for instruction in ass_obj.instructions:
            for inter in instruction:
                second_pass_traverse(inter)
        return
    if isinstance(ass_obj,Ass_Ast.Ass_Unary):
        ds = ass_obj.operand
        ass_obj.operand = second_pass_traverse(ds)
        return
    if isinstance(ass_obj,Ass_Ast.Mov):
        ass_obj.src = second_pass_traverse(ass_obj.src)
        ass_obj.dst = second_pass_traverse(ass_obj.dst)
        return
    if isinstance(ass_obj,Ass_Ast.Pseudo):
        if ass_obj.identifier in stack_map:
            return Ass_Stack(stack_map[ass_obj.identifier])
        stack.pointer = stack.pointer - 4
        initiate_pointer(ass_obj.identifier,stack.pointer)
        return Ass_Stack(stack_map[ass_obj.identifier])
    if isinstance(ass_obj,Ass_Ast.Imm):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Register):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Ret):
        return ass_obj
    raise ValueError("Unknown ASS node type")

class counterA:
    def __init__(self):
        self.row_counter = 0
        self.col_counter = 0
cnt = counterA()
class third_pass:
    def __int__(self):
        pass
    def third_pass_traverse(self,ass_obj,instructions = []):
        if isinstance(ass_obj,Ass_Ast.Program):
            self.third_pass_traverse(ass_obj.function_definition)
        if isinstance(ass_obj,Ass_Ast.Function):
            cnt.row_counter = 0
            ass_obj.instructions[0].insert(0,AlocateStack(get_max_stack_pointer()))
            for instruction in ass_obj.instructions:

                cnt.col_counter = 0
                for inter in instruction:

                    self.third_pass_traverse(inter,ass_obj.instructions)
                    cnt.col_counter += 1

                cnt.row_counter += 1

        if isinstance(ass_obj,Ass_Ast.Ret):
            return
        if isinstance(ass_obj,Ass_Ast.Ass_Unary):
            ds = ass_obj.operand
            self.third_pass_traverse(ds,instructions)
        if isinstance(ass_obj,Ass_Ast.Mov):
            src = self.third_pass_traverse(ass_obj.src)
            dst = self.third_pass_traverse(ass_obj.dst)
            if isinstance(src,Ass_Ast.Ass_Stack) and isinstance(dst,Ass_Ast.Ass_Stack):
                ass_obj.dst = Register("r10d")
                instructions[cnt.row_counter].insert(cnt.col_counter+1,Mov(Register("r10d"),dst))


        if isinstance(ass_obj,Ass_Ast.Ass_Stack):
            return ass_obj

def get_max_stack_pointer():
    ma = 0
    for keyword in stack_map:
        val = stack_map[keyword]
        if val <= ma:
            ma =val
    return abs(ma)
