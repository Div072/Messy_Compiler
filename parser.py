from unittest.mock import right

from parser_ast_expr_stmt import*
from Token import*
class Parser:
    def __init__(self,tokens):
        self.curr = 0
        self.tokens = tokens
        self.pecendece = {Tokentype.MINUS:45,Tokentype.DIVIDE:50,Tokentype.MULTIPLY:50,Tokentype.PLUS:45}
    def parse(self):
        return self.program()

    def program(self):
        fun_declar = self.stmt()
        return ProgramStmt(fun_declar)

    def stmt(self):
        if self.peek().type == Tokentype.INT:
            self.advance() #consume int
            if self.peek().type == Tokentype.INDENT:
                self.advance() # consume Indent
                name = self.peek_previous()
                if self.peek().type == Tokentype.OPENBRA:

                    self.advance()#consume (
                    return  self.fun_declaration(name)
            else:
                print("Error from parser: not a variable declaration or function dec")
                print("correct usage TYPE - IDENTIFIER ")
                exit()
        elif self.peek().type == Tokentype.RETURN:
            self.advance() #consume return
            val = self.expr()
            return Return(val)
    def fun_declaration(self,token:Token):
        name = token.lexeme
        statements = []
        if self.peek().type == Tokentype.CLOSEBRA:
            self.advance()#consume)
            if self.peek().type == Tokentype.OPENPARA:
                self.advance() #consume {
                while self.peek().type != Tokentype.SEMICOLON and not self.IsEnd():
                    statements.append(self.stmt())
                self.advance() #consume ;
                if self.peek().type != Tokentype.CLOSEPARA:
                    print("Missing } in function declaration")
                    exit()
                else:
                    self.advance() #consume }
            else:
                print("Missing { in function declaration")
                exit()
        else:
            print("Missing ) in function declaration ")
            exit()
        return Fun_Declaration(name,statements)
    def expr(self):
        return self.factor()
    def factor(self):
        left = self.term()
        while self.peek().type == Tokentype.PLUS or self.peek().type == Tokentype.MINUS:
            operator = self.peek()
            self.advance() #consume + or -
            right = self.term()
            left = Binary(operator,left,right)
        return left
    def term(self):
        left = self.unary()
        while self.peek().type == Tokentype.MULTIPLY or self.peek().type == Tokentype.DIVIDE:
            operator = self.peek()
            self.advance() #consume * /
            right = self.unary()
            left = Binary(operator,left,right)
        return left

    def unary(self):
        if self.peek().type == Tokentype.MINUS or self.peek().type == Tokentype.B_NOT:
            operator = self.peek()
            self.advance() # consume ~/-
            expr = self.unary()
            return Unary(operator,expr)
        else:
            return self.primary()
    def primary(self):
        token = self.peek()
        if token.type == Tokentype.NUMBER:
            self.advance()
            return Literal(token.lexeme,Tokentype.INT)
        if token.type == Tokentype.STRING:
            self.advance()
            return Literal(token.lexeme,Tokentype.STRING)
        if token.type == Tokentype.OPENBRA:
            self.advance() #consume (
            expr = self.expr() #change it future
            if self.peek().type == Tokentype.CLOSEBRA:
                self.advance() #consume )
                return expr
            else :
                print("Error from Lexer missing ) in grouping (expr)")
                exit()

    def peek(self):
        # be aware this peek method is also increasing curr pointer by one
        if self.curr<len(self.tokens):
            return self.tokens[self.curr]
        return Token(Tokentype.EOF,"EOF",0)
    def advance(self):
        if self.IsEnd():
            return False
        self.curr +=1
        return True
    def IsEnd(self):
        if self.curr>= len(self.tokens) or self.peek()==Tokentype.EOF:
            return True
        return False
    def peek_previous(self):
        if self.curr-1>=0:
            return self.tokens[self.curr-1]
        else:
            print("Error from parser: peek_previous() accessing index less than 0")
            exit()
    def consume(self,token_type:Tokentype,message):
        if self.peek().type != token_type:
            print(message)
            exit()
        else:
            self.advance()
            return self.peek_previous()