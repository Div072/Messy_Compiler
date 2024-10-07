from IR_code import*
from Token import Tokentype
from parser_ast_expr_stmt import*
# should I use visitor pattern of simple match instance??

class parse_to_IR():
    def __init__(self):
        self.identifer_val = 0
        self.EXPR_instructions = []
    def traverse(self,obj,instruction=[]):

        if isinstance(obj,Literal):
            return self.visitConstantExpr(obj)
        elif isinstance(obj,Unary):
            return self.visitUnaryExpr(obj,instruction)
        elif isinstance(obj,ProgramStmt):
            return self.visitprogramStmt(obj)
        elif isinstance(obj,Fun_Declaration):
            return self.visitFunStmt(obj)
        elif isinstance(obj,Return):
            return self.visitRetstmt(obj,instruction)
        elif isinstance(obj,Token):
            if obj.type == Tokentype.B_NOT:
                return self.visitComplementOperator()
            elif obj.type == Tokentype.MINUS:
                return self.visitNegOperator()
    def visitprogramStmt(self,stmt:ProgramStmt):

        declaration = self.traverse(stmt.fun_declaration)

        return Program(declaration)

    def visitFunStmt(self,stmt:Fun_Declaration):
        inst = []
        for statment in stmt.statements:
            instrct = []
            self.traverse(statment, instrct)
            inst.append(instrct)
        return Fun_ction(stmt.name, inst)
    def visitRetstmt(self,stmt:Return,instructions):
        val = self.traverse(stmt.expression,instructions)
        instructions.append(Ret(val))

    def visitUnaryExpr(self,expr:Unary,instructions):
        src = self.traverse(expr.expr,instructions)
        identifier_name = self.make_identifer()
        dst = Variable(identifier_name)
        op = self.traverse(expr.operator)
        instructions.append(U_nary(op,src,dst))
        return dst
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

