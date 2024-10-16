from IR_code import*
from Resolution import make_unique_name
from Token import Tokentype
from parser_ast_expr_stmt import*
# should I use visitor pattern of simple match instance??

class parse_to_IR():
    def __init__(self):
        self.identifer_val = 0
        self.global_identifier = 0

    def traverse(self,obj,instruction=[]):
        if isinstance(obj,list):
            for statement in obj:
                self.traverse(statement,instruction)
        elif isinstance(obj,Literal):
            return self.visitConstantExpr(obj)
        elif isinstance(obj,Expression):
            return self.visitExpression(obj,instruction)
        elif isinstance(obj,Unary):
            return self.visitUnaryExpr(obj,instruction)
        elif isinstance(obj,Binary):
            return self.visitBinaryExpr(obj.binary_op,obj.left,obj.right,instruction)
        elif isinstance(obj,ProgramStmt):
            return self.visitprogramStmt(obj)
        elif isinstance(obj,Fun_Declaration):
            return self.visitFunStmt(obj,instruction)
        elif isinstance(obj,Block):
            return self.visitBlockStmt(obj,instruction)
        elif isinstance(obj,Return):
            return self.visitRetstmt(obj,instruction)
        elif isinstance(obj,IDENTIFIER):
            return self.visitIdentifier(obj)
        elif isinstance(obj,Assignment):
            return self.visitAssignment(obj,instruction)
        elif isinstance(obj,Declaration):
            return self.visitDeclaration(obj,instruction)
        elif isinstance(obj,If_Else):
            return self.visitIfElseStmt(obj,instruction)



    def visitprogramStmt(self,stmt:ProgramStmt):
        declaration = self.traverse(stmt.fun_declaration)
        return Program(declaration)

    def visitFunStmt(self,stmt:Fun_Declaration,instructions):
        self.traverse(stmt.block,instructions)
        return Fun_ction(stmt.name,instructions)
        """inst = []
        for statment in stmt.block_items:
            instrct = []
            self.traverse(statment, instrct)
            if instrct:
                inst.append(instrct)
        return Fun_ction(stmt.name, inst)"""
    def visitBlockStmt(self,block:Block,instructions):
        # need to do it
        for statment in block.block_items:
            instruct = []
            self.traverse(statment,instruct)
            if instruct:
                instructions.append(instruct)
    def visitIfElseStmt(self,if_else:If_Else,instructions):
        condition = self.traverse(if_else.conditional,instructions)
        else_label = self.make_global_identifer()
        end_label = self.make_global_identifer()
        instructions.append(JumpIfZero(condition,else_label))
        self.traverse(if_else.If_staments,instructions)
        instructions.append(Jump(end_label))
        instructions.append(Label(else_label))
        self.traverse(if_else.El_staments,instructions)
        instructions.append(Label(end_label))

    def visitRetstmt(self,stmt:Return,instructions):
        val = self.traverse(stmt.expression,instructions)
        instructions.append(Ret(val))
    def visitDeclaration(self,obj:Declaration,instructions):
        if obj.expr is not None:
            return self.visitAssignment(Assignment(obj.name,obj.expr),instructions)
        return

    def visitExpression(self,Ex:Expression,instructions):
        expr = self.traverse(Ex.expr,instructions)

    def visitUnaryExpr(self,expr:Unary,instructions):
        src = self.traverse(expr.expr,instructions)
        identifier_name = self.make_identifer()
        dst = Variable(identifier_name)
        op = self.convert_to_op(expr.operator)
        instructions.append(U_nary(op,src,dst))
        return dst
    def visitBinaryExpr(self,operator:Token,left:Expr,right:Expr,instructions):
        if operator.type ==Tokentype.OR or operator.type == Tokentype.AND:
            v1 = self.traverse(left,instructions)
            v2 = self.traverse(right,instructions)
            false_label = self.make_global_identifer()
            end_label = self.make_global_identifer()
            dst_name = self.make_identifer()
            dst = Variable(dst_name)
            if operator.type == Tokentype.AND:
                instructions.append(JumpIfZero(v1,false_label))
                instructions.append(JumpIfZero(v2,false_label))
                instructions.append(Copy(Const(1),dst))
                instructions.append(Jump(end_label))
                instructions.append(Label(false_label))
                instructions.append(Copy(Const(0),dst))
                instructions.append(Label(end_label))
            else:
                instructions.append(JumpIfNotZero(v1,false_label))
                instructions.append(JumpIfNotZero(v2,false_label))
                instructions.append(Copy(Const(0),dst))
                instructions.append(Jump(end_label))
                instructions.append(Label(false_label))
                instructions.append(Copy(Const(1),dst))
                instructions.append(Label(end_label))
            return dst
        else:
            v1 = self.traverse(left,instructions)
            v2 = self.traverse(right,instructions)
            dst_name = self.make_identifer()
            dst = Variable(dst_name)
            op = self.convert_to_op(operator)
            instructions.append(B_inary(op,v1,v2,dst))
            return dst
    def visitIdentifier(self,identifer:IDENTIFIER):
        return Variable(identifer.name)
    def visitAssignment(self,assingment:Assignment,instructions):
        expr = self.traverse(assingment.right,instructions)
        identifier = assingment.left.name
        instructions.append(Copy(expr,Variable(identifier)))
        return Variable(identifier)

    def visitConstantExpr(self,expr:Literal):
        return Const(expr.value)
    def visitComplementOperator(self):
        return Complement()
    def visitNegOperator(self):
        return Negete()
    def make_identifer(self):
        self.identifer_val = self.identifer_val+ 1
        return f"temp{self.identifer_val}"
    def convert_to_op(self,operator):
        if operator.type ==Tokentype.B_NOT:
            return Complement()
        elif operator.type == Tokentype.MINUS:
            return Negete()
        elif operator.type == Tokentype.PLUS:
            return Add()
        elif operator.type == Tokentype.DIVIDE:
            return Divide()
        elif operator.type == Tokentype.MULTIPLY:
            return Multiply()
        elif operator.type == Tokentype.REMAINDER:
            return Remainder()
        elif operator.type == Tokentype.BIT_AND:
            return Bit_And()
        elif operator.type == Tokentype.BIT_XOR:
            return Bit_Xor()
        elif operator.type ==  Tokentype.BIT_OR:
            return Bit_Or()
        elif operator.type == Tokentype.LEFT_SWIFT:
            return Left_Shift()
        elif operator.type == Tokentype.RIGHT_SWIFT:
            return Right_Shift()
        elif operator.type == Tokentype.GREATER:
            return Greater()
        elif operator.type ==Tokentype.GREATER_EQUAL:
            return GreaterEqual()
        elif operator.type == Tokentype.LESS:
            return Less()
        elif operator.type == Tokentype.LESS_EQUAL:
            return LessEqual()
        elif operator.type == Tokentype.EQUAL_EQUAL:
            return Equal_Equal()
        elif operator.type == Tokentype.BANG_EQUAL:
            return Not_Equal()
        elif operator.type == Tokentype.BANG:
            return Not()

    def make_global_identifer(self):
        self.global_identifier +=1
        return f"global{self.global_identifier}"