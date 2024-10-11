from unittest.mock import right

from ass_traverser import second_pass_traverse
from parser_ast_expr_stmt import*
from Token import*
"""Precedence Table (from highest to lowest)
Parentheses: ()
Unary Operators: +, -, ~ (bitwise NOT), ! (logical NOT)
Multiplicative: *, /, %
Additive: +, -
Shift: <<, >>
Relational: <, >, <=, >=
Equality: ==, !=
Bitwise AND: &
Bitwise XOR: ^
Bitwise OR: |
Logical AND: &&
Logical OR: ||"""
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
        return self.bit_or()
    def bit_or(self):
        left = self.bit_xor()
        while self.peek().type == Tokentype.BIT_OR:
            self.advance()
            operator = self.peek_previous()
            right = self.bit_xor()
            left = Binary(operator,left,right)
        return left
    def bit_xor(self):
        left = self.bit_and()
        while self.peek().type == Tokentype.BIT_XOR:
            operator = self.peek()
            self.advance() #comsume operator
            right = self.bit_and()
            left = Binary(operator, left, right)
        return left
    def bit_and(self):
        left = self.bit_shift()
        while self.peek().type == Tokentype.BIT_AND:
            self.advance()
            operator = self.peek_previous()
            right = self.bit_shift()
            left = Binary(operator, left, right)
        return left
    def bit_shift(self):
        left = self.factor()
        while self.peek().type == Tokentype.LEFT_SWIFT or self.peek().type == Tokentype.RIGHT_SWIFT:
            operator = self.peek()
            self.advance()
            right = self.factor()
            left = Binary(operator,left,right)
        return left
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
        self.curr = self.curr + 1
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