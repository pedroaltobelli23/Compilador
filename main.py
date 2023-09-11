import sys
import re


PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
INT = "INTEGER"
EOF = "End of File"
PAR_IN = "("
PAR_OUT = ")"


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source, next=None, position=0):
        self.source = str(source)
        self.next = next
        self.position = position

    def selectNext(self):
        value = ""
        type = None

        if self.position >= len(self.source):
            value = "EOF"
            type = EOF
            self.next = Token(type=type, value=value)
            return

        while self.position != len(self.source):
            if re.match("[0-9]", self.source[self.position]):  # Checking if is number
                while self.position < len(self.source):
                    if re.match(r"[0-9]", self.source[self.position]):
                        value += self.source[self.position]
                        self.position += 1
                    else:
                        type = INT
                        self.next = Token(type=type, value=int(value))
                        return
                type = INT
                self.next = Token(type=type, value=int(value))
                return
            elif self.source[self.position] == "+":  # Checking if is plus
                value = self.source[self.position]
                type = PLUS
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "-":  # Checking if is minus
                value = self.source[self.position]
                type = MINUS
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "*":  # Checking if is times
                value = self.source[self.position]
                type = TIMES
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "/":  # Checking if is division
                value = self.source[self.position]
                type = DIV
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "(":  # Checking if is parentheses open
                value = self.source[self.position]
                type = PAR_IN
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == ")":  # Checking if is parentheses close
                value = self.source[self.position]
                type = PAR_OUT
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == " ":
                self.position += 1
                continue
            else:
                raise Exception("Incorrect value")


class ParserError(Exception):
    pass


class Parser:
    tokens = None

    def parseExpression(self):
        total = 0
        total += self.parseTerm()
        while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS:
            if self.tokens.next.type == PLUS:
                self.tokens.selectNext()
                left = self.parseTerm()
                total += left
            elif self.tokens.next.type == MINUS:
                self.tokens.selectNext()
                left = self.parseTerm()
                total -= left
        
        if self.tokens.next.type == INT:
            raise Exception("Code Incorrect")
        
            
        return total

    def parseTerm(self):
        total = 0
        total += self.parseFactor()
        while self.tokens.next.type == TIMES or self.tokens.next.type == DIV:
            if self.tokens.next.type == TIMES:
                self.tokens.selectNext()
                left = self.parseFactor()
                total *= left
            elif self.tokens.next.type == DIV:
                self.tokens.selectNext()
                left = self.parseFactor()
                total //= left
            
        return total
    
    def parseFactor(self):
        totalparcial = 1
        if self.tokens.next.type == INT:
            totalparcial = self.tokens.next.value
            self.tokens.selectNext()
        elif self.tokens.next.type == PLUS:
            self.tokens.selectNext()
            totalparcial = 1*self.parseFactor()
        elif self.tokens.next.type == MINUS:
            self.tokens.selectNext()
            totalparcial = -1*self.parseFactor()
        elif self.tokens.next.type == PAR_IN:
            self.tokens.selectNext()
            totalparcial = self.parseExpression()
            if self.tokens.next.type == PAR_OUT:
                self.tokens.selectNext()
            else:
                raise Exception("Code Incorrect")
        else:
            raise Exception("Code Incorrect")
        return totalparcial
    
    def run(self, code):
        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        total = self.parseExpression()
        if self.tokens.next.type == EOF:
            return total
        else:
            raise Exception("Code Incorrect")


if __name__ == "__main__":
    chain = sys.argv[1]

    parser = Parser()

    final = parser.run(chain)
    
    print(final)
