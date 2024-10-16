from collections import namedtuple
import copy
variable_map_global = {}
name_cnt  = 0

from parser_ast_expr_stmt import*
# To implement typedef for compiler we need to move this Resolution pass into parser and analyse and resolute variables as we parse the program.
class resolution():
    def traverse_syntax_analysis(self,obj,variable_map):
        if isinstance(obj,list):
            for statement in obj:
                self.traverse_syntax_analysis(statement,variable_map)
        if isinstance(obj,IDENTIFIER):
            obj.name = self.resolve_expr(obj,variable_map).name
        elif isinstance(obj,Expression):
            self.traverse_syntax_analysis(obj.expr,variable_map)
        elif isinstance(obj,Unary):
            return self.visitUnaryExpr(obj,variable_map)
        elif isinstance(obj,Binary):
            return self.visitBinaryExpr(obj,variable_map)
        elif isinstance(obj,ProgramStmt):
            return self.visitprogramStmt(obj,variable_map)
        elif isinstance(obj,Fun_Declaration):
            return self.visitFunStmt(obj,variable_map)
        elif isinstance(obj,Block):
            return self.traverse_syntax_analysis(obj.block_items,variable_map)
        elif isinstance(obj,Return):
            return self.visitReturnStmt(obj,variable_map)
        elif isinstance(obj,Declaration):
            obj.name = self.resolve_Declaration(obj.name,obj.expr,variable_map)
        elif isinstance(obj,Assignment):
            if isinstance(obj.left, IDENTIFIER):
                self.traverse_syntax_analysis(obj.left,variable_map)
                self.traverse_syntax_analysis(obj.right,variable_map)
            else:
                raise ValueError("left side of assignment should be variable (IDENTIFIER) but got",obj.left)
        elif isinstance(obj,NULL):
            return obj
        elif isinstance(obj,If_Else):
            self.visitIfElseStmt(obj,variable_map)
        elif isinstance(obj,Ternary):
            self.visitTernary(obj,variable_map)
        elif isinstance(obj,Compound):
            self.visitCompound(obj,variable_map)
    def visitprogramStmt(self,stmt:ProgramStmt,variable_map):
        self.traverse_syntax_analysis(stmt.fun_declaration,variable_map)
        return
    def visitFunStmt(self,stmt:Fun_Declaration,variable_map):
        self.traverse_syntax_analysis(stmt.block,variable_map)

    def visitIfElseStmt(self,if_else:If_Else,variable_map):
        self.traverse_syntax_analysis(if_else.conditional,variable_map)
        self.traverse_syntax_analysis(if_else.If_staments,variable_map)
        self.traverse_syntax_analysis(if_else.El_staments,variable_map)
    def visitCompound(self,compund:Compound,variable_map):
        copy_map = copy.deepcopy(variable_map)
        for key,value in copy_map.items():
            value[1] = False # setting every value to False so that same name variable can exist in block scope
        self.traverse_syntax_analysis(compund.block,copy_map)

    def visitReturnStmt(self,ret:Return,variable_map):
        self.traverse_syntax_analysis(ret.expression,variable_map)
    def visitTernary(self,ternary:Ternary,variable_map):
        self.traverse_syntax_analysis(ternary.condition,variable_map)
        self.traverse_syntax_analysis(ternary.then_part,variable_map)
        self.traverse_syntax_analysis(ternary.else_part,variable_map)
    def visitUnaryExpr(self,unary,variable_map):
        self.traverse_syntax_analysis(unary.expr,variable_map)
    def visitBinaryExpr(self,binary,variable_map):
        self.traverse_syntax_analysis(binary.left,variable_map)
        self.traverse_syntax_analysis(binary.right,variable_map)
    def resolve_Declaration(self,name:IDENTIFIER,expr,variable_map):
        if name.name in variable_map and variable_map[name.name][1] == True: # here were accessing [unique_name,False/True] by [1]
            raise ValueError("Duplicate variable declaration")
        unique_name = make_unique_name(name.name)
        variable_map[name.name] = [unique_name,True]
        if expr is not None:
            self.traverse_syntax_analysis(expr,variable_map)
        return IDENTIFIER(unique_name)
    def resolve_expr(self,expr,variable_map):
        if isinstance(expr,IDENTIFIER):
            name = expr.name
            if name in variable_map:
                return IDENTIFIER(variable_map.get(name)[0])
            else:
                raise ValueError("Undeclared variable",name)


def make_unique_name(name):
    global name_cnt
    name_cnt+= 1
    return f"{name}.{name_cnt}"

