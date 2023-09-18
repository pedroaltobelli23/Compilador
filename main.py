import sys
import re
from abstractsyntaxtree import Node,BinOp,UnOp,IntVal

PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
INT = "INTEGER"
EOF = "End of File"
PAR_IN = "("
PAR_OUT = ")"

class PrePro:
    def __init__(self,source):
        self.source = source
        
    def filter(self):
        return re.sub(r"\/\/.*$","",self.source,flags=re.MULTILINE)
        
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
        node = self.parseTerm()
        while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS:
            if self.tokens.next.type == PLUS:
                self.tokens.selectNext()
                node = BinOp(PLUS,[node,self.parseTerm()])
            elif self.tokens.next.type == MINUS:
                self.tokens.selectNext()
                node = BinOp(MINUS,[node,self.parseTerm()])
        
        if self.tokens.next.type == INT:
            raise Exception("Code Incorrect")
           
        return node

    def parseTerm(self):
        node = self.parseFactor()
        while self.tokens.next.type == TIMES or self.tokens.next.type == DIV:
            if self.tokens.next.type == TIMES:
                self.tokens.selectNext()
                node = BinOp(TIMES,[node,self.parseFactor()])
            elif self.tokens.next.type == DIV:
                self.tokens.selectNext()
                node = BinOp(DIV,[node,self.parseFactor()])
            else:
                raise Exception("Code Incorrect")
            
        return node
    
    def parseFactor(self):
        node = 0
        if self.tokens.next.type == INT:
            node = IntVal(self.tokens.next.value, [])
            self.tokens.selectNext()
        elif self.tokens.next.type == PLUS:
            self.tokens.selectNext()
            node = UnOp(PLUS,[self.parseFactor()])
        elif self.tokens.next.type == MINUS:
            self.tokens.selectNext()
            node = UnOp(MINUS,[self.parseFactor()])
            
        elif self.tokens.next.type == PAR_IN:
            self.tokens.selectNext()
            node = self.parseExpression()
            if self.tokens.next.type == PAR_OUT:
                self.tokens.selectNext()
            else:
                raise Exception("Code Incorrect")
        else:
            raise Exception("Code Incorrect")
        
        return node
    
    def run(self, code):
        file = open(code,"r")
        new = file.read()
        file.close()
        filtered = PrePro(new).filter()
        filtered = filtered.strip()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        master_node = self.parseExpression()
        if self.tokens.next.type == EOF:
            return master_node.Evaluate()
        else:
            raise Exception("Code Incorrect")

if __name__ == "__main__":
    chain = sys.argv[1]

    parser = Parser()

    final = parser.run(chain)
    
    print(final)
