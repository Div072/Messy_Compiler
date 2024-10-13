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

def convert_ast_to_assembly(Ir_ast_node):
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
            Mov(convert_ast_to_assembly(Ir_ast_node.val), Register("Ax")),
            Ret()
        ]
    if isinstance(Ir_ast_node,IR_code.U_nary):
        if isinstance(Ir_ast_node.operator,IR_code.Not):
            return[
                Cmp(Imm(0),convert_ast_to_assembly(Ir_ast_node.src)),
                Mov(Imm(0),convert_ast_to_assembly(Ir_ast_node.ds)),
                SetCC("E",convert_ast_to_assembly(Ir_ast_node.ds))
            ]
        else:
            return[
            Mov(convert_ast_to_assembly(Ir_ast_node.src),convert_ast_to_assembly(Ir_ast_node.ds)),
            Ass_Unary(convert_ast_to_assembly(Ir_ast_node.operator),convert_ast_to_assembly(Ir_ast_node.ds))
            ]
    if isinstance(Ir_ast_node,IR_code.B_inary):
        operator = Ir_ast_node.operator
        src1 = Ir_ast_node.src1
        src2 = Ir_ast_node.src2
        dst = Ir_ast_node.dst
        if isinstance(operator,IR_code.Divide):
            return [Mov(convert_ast_to_assembly(src1),Register("Ax")),
                    Ass_Cdq(),
                    Ass_Idiv(convert_ast_to_assembly(src2)),
                    Mov(Register("Ax"),convert_ast_to_assembly(dst))
                    ]
        elif isinstance(operator,IR_code.Remainder):
            return[Mov(convert_ast_to_assembly(src1),Register("Ax")),
                    Ass_Cdq(),
                    Ass_Idiv(convert_ast_to_assembly(src2)),
                    Mov(Register("Dx"),convert_ast_to_assembly(dst))
                    ]
        elif isinstance(operator,IR_code.Multiply) or isinstance(operator,IR_code.Add) or isinstance(operator,IR_code.Negete) or isinstance(operator,IR_code.Bit_Or) or isinstance(operator,IR_code.Bit_And) or isinstance(operator,IR_code.Bit_Xor):
            return [Mov(convert_ast_to_assembly(src1),convert_ast_to_assembly(dst)),
                    Ass_Binary(convert_ast_to_assembly(operator),convert_ast_to_assembly(src2),convert_ast_to_assembly(dst))
                    ]
        elif isinstance(operator,IR_code.Right_Shift) or isinstance(operator,IR_code.Left_Shift):
            return [Mov(convert_ast_to_assembly(src1),convert_ast_to_assembly(dst)),
                    Ass_Binary(convert_ast_to_assembly(operator),convert_ast_to_assembly(src2),convert_ast_to_assembly(dst))
            ]
        elif isinstance(operator,IR_code.Less) or isinstance(operator,IR_code.LessEqual) or isinstance(operator,IR_code.Greater) or isinstance(operator,IR_code.GreaterEqual) or isinstance(operator,IR_code.Equal_Equal) or isinstance(operator,IR_code.Not_Equal):
            return[
                Cmp(convert_ast_to_assembly(src2),convert_ast_to_assembly(src1)),
                Mov(Imm(0),convert_ast_to_assembly(dst)),
                SetCC(get_relational_op(operator),convert_ast_to_assembly(dst))
            ]
        else:
            raise ValueError("Not defined type of Ir code operator",operator)
    if isinstance(Ir_ast_node,IR_code.Jump):
        return Jmp(Ir_ast_node.target)
    if isinstance(Ir_ast_node,IR_code.JumpIfZero):
        return [
            Cmp(Imm(0),convert_ast_to_assembly(Ir_ast_node.condition)),
            JmpCC("E",Ir_ast_node.identifier)
        ]
    if isinstance(Ir_ast_node,IR_code.JumpIfNotZero):
        return [
            Cmp(Imm(0),convert_ast_to_assembly(Ir_ast_node.condition)),
            JmpCC("NE",Ir_ast_node.identifier)
        ]
    if isinstance(Ir_ast_node,IR_code.Copy):
        return Mov(convert_ast_to_assembly(Ir_ast_node.src),convert_ast_to_assembly(Ir_ast_node.dst))
    if isinstance(Ir_ast_node,IR_code.Label):
        return Label(Ir_ast_node.identifier)
    if isinstance(Ir_ast_node,IR_code.Variable):
        return Pseudo(Ir_ast_node.identifier)
    if isinstance(Ir_ast_node,IR_code.Const):
        return Imm(Ir_ast_node.const)
    if isinstance(Ir_ast_node,IR_code.Complement):
        return Ass_Not()
    if isinstance(Ir_ast_node,IR_code.Negete):
        return Ass_Neg()
    if isinstance(Ir_ast_node,IR_code.Add):
        return Ass_Add()
    if isinstance(Ir_ast_node,IR_code.Subtract):
        return Ass_Sub()
    if isinstance(Ir_ast_node,IR_code.Multiply):
        return Ass_Mul()
    if isinstance(Ir_ast_node,IR_code.Bit_Or):
        return Ass_Bit_Or()
    if isinstance(Ir_ast_node,IR_code.Bit_And):
        return Ass_Bit_And()
    if isinstance(Ir_ast_node,IR_code.Bit_Xor):
        return Ass_Bit_Xor()
    if isinstance(Ir_ast_node,IR_code.Left_Shift):
        return Ass_Bit_Left_Shift()
    if isinstance(Ir_ast_node,IR_code.Right_Shift):
        return Ass_Bit_Right_Shift()
    raise ValueError("Unknown AST node type",Ir_ast_node)

def second_pass_traverse(ass_obj):
    if isinstance(ass_obj,list):
        for instruction in ass_obj:
            second_pass_traverse(instruction)

    if isinstance(ass_obj,Ass_Ast.Program):
        second_pass_traverse(ass_obj.function_definition)
        return
    if isinstance(ass_obj,Ass_Ast.Function):
        for instruction in ass_obj.instructions:
            second_pass_traverse(instruction)
        return
    if isinstance(ass_obj,Ass_Ast.Ass_Unary):
        ds = ass_obj.operand
        ass_obj.operand = second_pass_traverse(ds)
        return
    if isinstance(ass_obj,Ass_Binary):
        ass_obj.left = second_pass_traverse(ass_obj.left)
        ass_obj.right = second_pass_traverse(ass_obj.right)
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
    if isinstance(ass_obj,Ass_Ast.Cmp):
        ass_obj.val1 = second_pass_traverse(ass_obj.val1)
        ass_obj.val2 = second_pass_traverse(ass_obj.val2)
        return
    if isinstance(ass_obj,Ass_Ast.SetCC):
        ass_obj.operand = second_pass_traverse(ass_obj.operand)
        return
    if isinstance(ass_obj,Ass_Ast.Imm):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Register):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Ret):
        return ass_obj


class counterA:
    def __init__(self):
        self.row_counter = 0
        self.col_counter = 0
cnt = counterA()
def third_pass_traverse(ass_obj,instructions = []):
    if isinstance(ass_obj,Ass_Ast.Program):
        third_pass_traverse(ass_obj.function_definition)
    if isinstance(ass_obj,Ass_Ast.Function):
        cnt.row_counter = 0
        for instruction in ass_obj.instructions:
            cnt.col_counter = 0
            third_pass_traverse(instruction,ass_obj.instructions)
            cnt.row_counter += 1
        ass_obj.instructions.insert(0, AlocateStack(get_max_stack_pointer()))
    if isinstance(ass_obj,list):
        for instruct in ass_obj:
            third_pass_traverse(instruct,instructions)
            cnt.col_counter += 1
    if isinstance(ass_obj,Ass_Ast.Ret):
        return
    if isinstance(ass_obj,Ass_Ast.Ass_Unary):
        ds = ass_obj.operand
        third_pass_traverse(ds,instructions)
    if isinstance(ass_obj,Ass_Ast.Mov):
        src = third_pass_traverse(ass_obj.src,instructions)
        dst = third_pass_traverse(ass_obj.dst,instructions)
        if isinstance(src,Ass_Ast.Ass_Stack) and isinstance(dst,Ass_Ast.Ass_Stack):
            ass_obj.dst = Register("r10d")
            instructions[cnt.row_counter].insert(cnt.col_counter+1,Mov(Register("r10d"),dst))
    if isinstance(ass_obj,Ass_Idiv):
        if isinstance(ass_obj.operand,Ass_Ast.Imm):
            instructions[cnt.row_counter].insert(cnt.col_counter,Mov(ass_obj.operand,Register("r10d")))
            ass_obj.operand = Register("r10d")
    if isinstance(ass_obj,Ass_Ast.Cmp):
        if isinstance(ass_obj.val1,Ass_Ast.Ass_Stack) and isinstance(ass_obj.val2,Ass_Ast.Ass_Stack):
            val1 = ass_obj.val1
            ass_obj.val1 = Register("r10d")
            instructions[cnt.row_counter].insert(cnt.col_counter,Mov(val1,Register("r10d")))
        if isinstance(ass_obj.val2,Ass_Ast.Imm):
            val2 = ass_obj.val2
            ass_obj.val2 = Register("r11d")
            instructions[cnt.row_counter].insert(cnt.col_counter,Mov(val2,Register("r11d")))
    if isinstance(ass_obj,Ass_Ast.Ass_Binary):
        left = third_pass_traverse(ass_obj.left,instructions)
        right = third_pass_traverse(ass_obj.right,instructions)
        dst = right
        operator = ass_obj.binary_operator
        if isinstance(operator,Ass_Ast.Ass_Add) or isinstance(operator,Ass_Ast.Ass_Neg) or isinstance(operator,Ass_Ast.Ass_Mul):
            if isinstance(right,Ass_Ast.Imm):
                ass_obj.right = Register("r11d")
                instructions[cnt.row_counter].insert(cnt.col_counter,Mov(right,Register("r11d")))
        if isinstance(operator,Ass_Ast.Ass_Add) or isinstance(operator,Ass_Ast.Ass_Neg):
            if isinstance(left, Ass_Ast.Ass_Stack) and isinstance(right, Ass_Ast.Ass_Stack):
                instructions[cnt.row_counter].insert(cnt.col_counter,Mov(left,Register("r10d")))
                ass_obj.left = Register("r10d")
        if  isinstance(operator,Ass_Ast.Ass_Bit_Right_Shift) or isinstance(operator,Ass_Ast.Ass_Bit_Left_Shift):
            if isinstance(left, Ass_Ast.Ass_Stack) and isinstance(right, Ass_Ast.Ass_Stack):
                instructions[cnt.row_counter].insert(cnt.col_counter,MovB(left,Register("cl")))
                ass_obj.left = Register("cl")
        if isinstance(operator,Ass_Ast.Ass_Mul):
            if isinstance(right,Ass_Ast.Ass_Stack):
                instructions[cnt.row_counter].insert(cnt.col_counter,Mov(right,Register("r11d")))
                ass_obj.right = Register("r11d")
                cnt.col_counter += 1
                instructions[cnt.row_counter].insert(cnt.col_counter+1,Mov(Register("r11d"),dst))
        if isinstance(operator,Ass_Ast.Ass_Bit_And) or isinstance(operator,Ass_Bit_Or) or isinstance(operator,Ass_Bit_Xor):
            if isinstance(left,Ass_Ast.Ass_Stack) and isinstance(right,Ass_Ast.Ass_Stack):
                instructions[cnt.row_counter].insert(cnt.col_counter,Mov(left,Register("r10d")))
                ass_obj.left = Register("r10d")
    if isinstance(ass_obj,Ass_Ast.Ass_Stack):
        return ass_obj
    if isinstance(ass_obj, Ass_Ast.Ass_Add):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Ass_Sub):
        return ass_obj
    if isinstance(ass_obj,Ass_Ast.Imm):
        return ass_obj

def get_max_stack_pointer():
    ma = 0
    for keyword in stack_map:
        val = stack_map[keyword]
        if val <= ma:
            ma =val
    return abs(ma)
def get_relational_op(operator):
    if isinstance(operator,IR_code.Not_Equal):
        return "NE"
    if isinstance(operator,IR_code.LessEqual):
        return "LE"
    if isinstance(operator,IR_code.Greater):
        return "G"
    if isinstance(operator,IR_code.GreaterEqual):
        return "GE"
    if isinstance(operator,IR_code.Less):
        return "L"
    if isinstance(operator,IR_code.LessEqual):
        return "LE"
    if isinstance(operator,IR_code.Equal_Equal):
        return "E"
    else:
        raise ValueError("Not valid relational operator",operator)
