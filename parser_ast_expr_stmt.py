from __future__ import annotations
from Token import Token
from abc import  ABC, abstractmethod
class Visitor(ABC):
    @abstractmethod
    def visitLiteralExpr(self,expr:Literal)->None:
        pass
    @abstractmethod
    def visitFun_DeclarationStmt(self,stmt:Fun_Declaration)->None:
        pass
    @abstractmethod
    def visitUnaryExpr(self,expr:Unary)->None:
        pass
    @abstractmethod
    def visitBinaryExpr(self,expr:Binary)->None:
        pass
    @abstractmethod
    def visitRetrunStmt(self,stmt:Return)->None:
        pass
    @abstractmethod
    def visitProgramStmt(self,stmt:ProgramStmt)->None:
        pass
    @abstractmethod
    def visitAssignmentStmt(self,stmt:Assignment)->None:
        pass
    @abstractmethod
    def VisitDeclarationStmt(self,stmt:Declaration)->None:
        pass


class Expr(ABC):
    def accept(self,visitor:Visitor)->None:
        pass
class Unary(Expr):
    def __init__(self,operator:Token,expr:Expr):
        self.operator = operator
        self.expr = expr
    def accept(self,visitor:Visitor):
        return visitor.visitUnaryExpr(self)

class Literal(Expr):
    def __init__(self, value,type= None):
        self.value = value
        self.type = type
    def accept(self,visitor:Visitor):
        return visitor.visitLiteralExpr(self)
class IDENTIFIER():
    def __init__(self,name):
        self.name = name

class Binary(Expr):
    def __init__(self,binary_op,left, right):
        self.binary_op = binary_op
        self.left = left
        self.right = right
    def accept(self,visitor:Visitor):
        return visitor.visitBinaryExpr(self)
class NULL(Expr):
    pass
class Expression():
    def __init__(self,expr:Expr):
        self.expr = expr

class Stmt(ABC):
    def accept(self,visitor:Visitor)->None:
        pass

class ProgramStmt(Stmt):
    def __init__(self,fun_declaration:Fun_Declaration):
        self.fun_declaration = fun_declaration
    def accept(self,visitor:Visitor):
        return visitor.visitProgramStmt(self)
class Fun_Declaration(Stmt):
    def __init__(self,name,block_items:[]):
        self.name = name
        self.block_items = block_items
    def accept(self,visitor:Visitor):
        return visitor.visitFun_DeclarationStmt(self)
class Return(Stmt):
    def __init__(self,expr:Expr):
        self.expression = expr
    def accept(self,visitor:Visitor):
        return visitor.visitRetrunStmt(self)
class Assignment(Stmt):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def accept(self,visitor:Visitor):
        return visitor.visitAssignmentStmt(self)
class Declaration(Stmt):
    def __init__(self,name,expr:Expr=None):
        self.name = name
        self.expr = expr
    def accept(self,visitor:Visitor):
        return visitor.VisitDeclarationStmt(self)