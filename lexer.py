import Token

from Token import*
class Lexer:
     def __init__(self,source):
          self.source = source
          self.curr = 0
          self.line = 1
          self.tokens = []
          self.keywords ={"return":Tokentype.RETURN,"int":Tokentype.INT,"void":Tokentype.VOID,"if":Tokentype.IF,"else":Tokentype.ELSE}

     def scan(self):
          while not self.Isend():
               self.scan_token()
          self.tokens.append(Token.addToken(Tokentype.EOF, "EOF", self.line))

     def scan_token(self):
          start = self.curr
          ch = self.peek()
          self.advance()

          match ch:
               case '(':
                    self.tokens.append(Token.addToken(Tokentype.OPENBRA, "Openbra", self.line))
                    return
               case ')':
                    self.tokens.append(Token.addToken(Tokentype.CLOSEBRA, "closebra", self.line))
                    return
               case ';':
                    self.tokens.append(Token.addToken(Tokentype.SEMICOLON, "Semicolon", self.line))
                    return
               case ',':
                    self.tokens.append(Token.addToken(Tokentype.COMA, "coma", self.line))
                    return
               case '+':
                    self.tokens.append(Token.addToken(Tokentype.PLUS, "Plus", self.line))
                    return
               case '-':
                    self.tokens.append(Token.addToken(Tokentype.MINUS, "Minus", self.line))
                    return
               case '*':
                    self.tokens.append(Token.addToken(Tokentype.MULTIPLY, "Multiply", self.line))
                    return
               case '/':
                    self.tokens.append(Token.addToken(Tokentype.DIVIDE, "DIVISION", self.line))
                    return
               case '%':
                    self.tokens.append(Token.addToken(Tokentype.REMAINDER,"Remainder",self.line))
                    return
               case '>':
                    if self.peek() == '=':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.GREATER_EQUAL, "GREATER_EQUAL", self.line))
                         return
                    elif self.peek() == '>':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.RIGHT_SWIFT,"right_swift",self.line))
                         return
                    self.tokens.append(Token.addToken(Tokentype.GREATER, "GREATER", self.line))
                    return
               case '<':
                    if self.peek() == '=':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.LESS_EQUAL, "LESS_EQUAL", self.line))
                         return
                    elif self.peek() == '<':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.LEFT_SWIFT,"Left_swift",self.line))
                         return
                    self.tokens.append(Token.addToken(Tokentype.LESS, "LESS", self.line))
                    return
               case '=':
                    if self.peek() == '=':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.EQUAL_EQUAL, "EQUAL_EQUAL", self.line))
                         return
                    self.tokens.append(Token.addToken(Tokentype.EQUAL, "EQUAL", self.line))
                    return
               case '!':

                    if self.peek() == '=':
                         self.advance()
                         self.tokens.append(Token.addToken(Tokentype.BANG_EQUAL, "BANG_EQUAL", self.line))
                         return
                    self.tokens.append(Token.addToken(Tokentype.BANG, "BANG", self.line))
                    return
               case '&':
                    if self.peek() == '&':
                         self.advance()  # consume &
                         self.tokens.append(Token.addToken(Tokentype.AND, "AND", self.line))
                         return
                    else:
                         self.tokens.append(Token.addToken(Tokentype.BIT_AND,"Bit_and",self.line))
                         return

               case '|':
                    if self.peek() == '|':
                         self.advance()  # consume |
                         self.tokens.append(Token.addToken(Tokentype.OR, "OR", self.line))
                         return
                    else:
                         self.tokens.append(Token.addToken(Tokentype.BIT_OR, "Bit_or", self.line))
                         return
               case '^':
                    self.tokens.append(Token.addToken(Tokentype.BIT_XOR,"bit_xor",self.line))
                    return
               case '~':
                    self.tokens.append(Token.addToken(Tokentype.B_NOT,"~",self.line))
                    return
               case '?':
                    self.tokens.append(Token.addToken(Tokentype.QUESTION,"?",self.line))
                    return
               case ':':
                    self.tokens.append(Token.addToken(Tokentype.COLON,":",self.line))
                    return
               case '\n':
                    self.line += 1
                    return
               case '{':
                    self.tokens.append(Token.addToken(Tokentype.OPENPARA, "{", self.line))
                    return
               case '}':
                    self.tokens.append(Token.addToken(Tokentype.CLOSEPARA, "}", self.line))
                    return
               case ' ':
                    return
               case '"':
                    row = self.line
                    start = self.curr
                    while self.peek() != '"' and not self.Isend():
                         self.advance()
                    if self.Isend():
                         print('missing " in line', row)
                         exit()
                    self.tokens.append(Token.addToken(Tokentype.STRING, self.source[start:self.curr], self.line))
                    self.advance()  # consume "
                    return
               case '#':
                    while self.peek() != '#' and not self.Isend():
                         self.advance()
                    if self.Isend():
                         print("missing # in")
                         exit()
                    self.advance()  # consume #
               case _:
                    flag = False
                    start = self.curr - 1
                    if self.Isalphanumeric(ch):
                         self.curr = self.curr - 1
                         while self.Isalphanumeric(self.peek()):
                              if (self.Isnumber(self.peek())):  # check for number
                                   flag = True
                              else:
                                   flag = False
                              self.advance()
                         if flag == True:  # it is number
                              self.tokens.append(
                                   Token.addToken(Tokentype.NUMBER, int(self.source[start:self.curr]), self.line))
                              return
                         else:

                              if self.keywords.get(self.source[start:self.curr], False):
                                   if self.keywords.get(self.source[start:self.curr],
                                                        Tokentype.TRUE) == Tokentype.FALSE:
                                        self.tokens.append(Token.addToken(Tokentype.FALSE, False, self.line))
                                        return
                                   elif self.keywords.get(self.source[start:self.curr],
                                                          Tokentype.FALSE) == Tokentype.TRUE:
                                        self.tokens.append(Token.addToken(Tokentype.TRUE, True, self.line))
                                        return
                                   self.tokens.append(
                                        Token.addToken(self.keywords[self.source[start:self.curr]], "", self.line))
                                   return
                              else:
                                   self.tokens.append(
                                        Token.addToken(Tokentype.INDENT, self.source[start:self.curr], self.line))
                              return
                    else:
                         print("Error from Lexer: invalid character")
                         exit()
                    return

     def advance(self):
          self.curr = self.curr + 1

     def Isend(self):
          if self.curr < len(self.source):
               return False
          else:
               return True

     def Isnumber(self, ch):
          return ch.isdigit()

     def Isalphabet(self, ch):
          return ch.isalpha() or ch == '_'

     def Isalphanumeric(self, ch):
          return ch.isdigit() or self.Isalphabet(ch)

     def peek(self):
          if not self.Isend():
               return self.source[self.curr]
          return '\0'

     def peek_next(self):
          if self.curr + 1 < len(self.source):
               return self.source[self.curr + 1]
          else:
               return '\0'