import sys
import re
from abstractsyntaxtree import Node,BinOp,UnOp,IntVal,SymbolTable,Identifier,Assigment,Println,Block,NoOp

PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
INT = "INTEGER"
EOF = "End of File"
PAR_IN = "("
PAR_OUT = ")"
IDENTIFIER = "IDENTIFIER"
EQUAL = "="
PRINT = "println"
END = "\n"

class PrePro:
    def __init__(self,source):
        self.source = source
        
    def filter(self):
        a = re.sub(r"\/\/.*$","",self.source)
        return a
        
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
            elif self.source[self.position] == "=":  # Checking if is equal
                value = self.source[self.position]
                type = EQUAL
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif self.source[self.position] == "\n":  # Checking if is end
                value = self.source[self.position]
                type = END
                self.next = Token(type=type, value=value)
                self.position += 1
                return
            elif re.match("[a-zA-Z]", self.source[self.position]):  # Checking if is IDENTIFIER
                while self.position < len(self.source) and re.match(r"[a-zA-Z1-9_]", self.source[self.position]):
                    value += self.source[self.position]
                    self.position += 1
                if value == PRINT:
                    type = PRINT
                    self.next = Token(type=type, value=str(value))
                else:
                    type = IDENTIFIER
                    self.next = Token(type=type, value=str(value))
                return
            elif self.source[self.position] == " ":
                self.position += 1
                continue
            else:
                print(self.source[self.position])
                raise Exception("Incorrect value")

class ParserError(Exception):
    pass

class Parser:
    tokens = None

    def parseBlock(self):
        childrens = []
        while self.tokens.next.type != EOF:
            node = self.parseStatement()
            childrens.append(node)
        master = Block(None,childrens)
        return master
    
    def parseStatement(self):
        if self.tokens.next.type == END:
            self.tokens.selectNext()
            variable = NoOp("N",[])
            return variable
        elif self.tokens.next.type == IDENTIFIER:
            variable = Identifier(self.tokens.next.value,[])
            self.tokens.selectNext()
            if self.tokens.next.type == EQUAL:
                self.tokens.selectNext()
                variable = Assigment(EQUAL,[variable,self.parseExpression()])
            else:
                raise Exception("Code Incorrect")
        elif self.tokens.next.type == PRINT:
            self.tokens.selectNext()
            if self.tokens.next.type == PAR_IN:
                self.tokens.selectNext()
                variable = Println(PRINT,[self.parseExpression()])
                if self.tokens.next.type == PAR_OUT:
                    self.tokens.selectNext()
                    if self.tokens.next.type == END:
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code Incorrect")
                else:
                    raise Exception("Code is Incorrect")
        elif self.tokens.next.type == END:
            self.tokens.selectNext()
            variable = NoOp("N",[])
        else:
            raise Exception("Code Incorrect")
            
        return variable
    
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
        elif self.tokens.next.type == IDENTIFIER:
            node = Identifier(self.tokens.next.value,[])
            self.tokens.selectNext()
        else:
            raise Exception("Code Incorrect")
        
        return node
    
    def run(self, code):
        file = open(code,"r")
        new = file.read()
        file.close()
        filtered = PrePro(new).filter()
        identifier_table = SymbolTable()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        master_node = self.parseBlock()
        if self.tokens.next.type == EOF:
            a = master_node.Evaluate(identifier_table)
            return a
        else:
            raise Exception("Code Incorrect")

if __name__ == "__main__":
    chain = sys.argv[1]

    parser = Parser()

    final = parser.run(chain)
