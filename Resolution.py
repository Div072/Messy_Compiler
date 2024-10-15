variable_map = {}
name_cnt  = 0
from parser_ast_expr_stmt import*
# To implement typedef for compiler we need to move this Resolution pass into parser and analyse and resolute variables as we parse the program.
class resolution():
    def traverse_syntax_analysis(self,obj):
        if isinstance(obj,list):
            for statement in obj:
                self.traverse_syntax_analysis(statement)
        if isinstance(obj,IDENTIFIER):
            obj.name = self.resolve_expr(obj).name
        elif isinstance(obj,Expression):
            self.traverse_syntax_analysis(obj.expr)
        elif isinstance(obj,Unary):
            return self.visitUnaryExpr(obj)
        elif isinstance(obj,Binary):
            return self.visitBinaryExpr(obj)
        elif isinstance(obj,ProgramStmt):
            return self.visitprogramStmt(obj)
        elif isinstance(obj,Fun_Declaration):
            return self.visitFunStmt(obj)
        elif isinstance(obj,Return):
            return self.visitReturnStmt(obj)
        elif isinstance(obj,Declaration):
            obj.name = self.resolve_Declaration(obj.name,obj.expr)
        elif isinstance(obj,Assignment):
            if isinstance(obj.left, IDENTIFIER):
                self.traverse_syntax_analysis(obj.left)
                self.traverse_syntax_analysis(obj.right)
            else:
                raise ValueError("left side of assignment should be variable (IDENTIFIER) but got",obj.left)
        elif isinstance(obj,NULL):
            return obj
        elif isinstance(obj,If_Else):
            self.visitIfElseStmt(obj)
        elif isinstance(obj,Ternary):
            self.visitTernary(obj)
    def visitprogramStmt(self,stmt:ProgramStmt):
        self.traverse_syntax_analysis(stmt.fun_declaration)
        return
    def visitFunStmt(self,stmt:Fun_Declaration):
        for statment in stmt.block_items:
            self.traverse_syntax_analysis(statment)

    def visitIfElseStmt(self,if_else:If_Else):
        self.traverse_syntax_analysis(if_else.conditional)
        self.traverse_syntax_analysis(if_else.If_staments)
        self.traverse_syntax_analysis(if_else.El_staments)
    def visitReturnStmt(self,ret:Return):

        self.traverse_syntax_analysis(ret.expression)
    def visitTernary(self,ternary:Ternary):
        self.traverse_syntax_analysis(ternary.condition)
        self.traverse_syntax_analysis(ternary.then_part)
        self.traverse_syntax_analysis(ternary.else_part)
    def visitUnaryExpr(self,unary):
        self.traverse_syntax_analysis(unary.expr)
    def visitBinaryExpr(self,binary):
        self.traverse_syntax_analysis(binary.left)
        self.traverse_syntax_analysis(binary.right)
    def resolve_Declaration(self,name:IDENTIFIER,expr):
        if name.name in variable_map:
            raise ValueError("Duplicate variable declaration")
        unique_name = make_unique_name(name.name)
        variable_map[name.name] = unique_name
        if expr is not None:
            self.traverse_syntax_analysis(expr)
        return IDENTIFIER(unique_name)
    def resolve_expr(self,expr):
        if isinstance(expr,IDENTIFIER):
            name = expr.name
            if name in variable_map:
                return IDENTIFIER(variable_map.get(name))
            else:
                raise ValueError("Undeclared variable",name)





def make_unique_name(name):
    global name_cnt
    name_cnt+= 1
    return f"{name}.{name_cnt}"

