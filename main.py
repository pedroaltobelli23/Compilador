import sys
import re
from abstractsyntaxtree import (
    Node,
    BinOp,
    UnOp,
    IntVal,
    SymbolTable,
    Identifier,
    Assigment,
    Println,
    Block,
    NoOp,
    Scanln,
    IFNode,
    FORNode,
    VarDec,
    StrVal,
)

PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
INT = "INTEGER"
STR = "STRING"
VAR = "var"
T_INT = "int"
T_STRING = "string"
PAR_IN = "("
PAR_OUT = ")"
BRA_IN = "{"
BRA_OUT = "}"
SEMICOLUMN = ";"
IDENTIFIER = "IDENTIFIER"
EQUAL = "="
NOT = "!"
CONCAT = "."
PRINT = "Println"
SCAN = "Scanln"
AND = "&&"
COMPARE = "=="
OR = "||"
GT = ">"
LT = "<"
IF = "if"
ELSE = "else"
FOR = "for"
END = "\n"
EOF = "End of File"


class PrePro:
    def __init__(self, source):
        self.source = source

    def filter(self):
        with open(self.source, "r") as input_file:
            code = input_file.read()

        code = re.sub(r"//.*", "", code)

        lines = code.split("\n")

        if re.search(r"\d\s+\d", code):
            raise Exception("Two numbers can't be separeted only by a space")
        
        code = "\n".join([line.lstrip("\t") for line in lines])
        
        return code


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
        if self.position >= len(self.source):  # Checking if is EOF
            self.next = Token(type=EOF, value="EOF")
            return

        while self.position < len(self.source):
            if self.position >= len(self.source):
                self.next = Token(EOF, " ")
                return
            if re.match("[0-9]", self.source[self.position]):  # Checking if is number
                val = ""
                while self.position < len(self.source):
                    if re.match(r"[0-9]", self.source[self.position]):
                        val += self.source[self.position]
                        self.position += 1
                    else:
                        self.next = Token(type=INT, value=int(val))
                        return
                self.next = Token(type=INT, value=int(val))
                return
            elif self.source[self.position] == '"': # checking if is string
                string_value = ""
                self.position+=1
                while (self.position < len(self.source)):
                    if self.source[self.position] != '"':
                        string_value+=self.source[self.position]
                        self.position+=1
                    else:
                        self.position+=1
                        self.next = Token(type=STR, value=str(string_value))
                        return
                raise Exception("String Incorrect")
            elif self.source[self.position] == "+":  # Checking if is plus
                self.next = Token(type=PLUS, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "-":  # Checking if is minus
                self.next = Token(type=MINUS, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "*":  # Checking if is times
                self.next = Token(type=TIMES, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "/":  # Checking if is division
                self.next = Token(type=DIV, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "(":  # Checking if is parentheses open
                self.next = Token(type=PAR_IN, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == ")":  # Checking if is parentheses close
                self.next = Token(type=PAR_OUT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "{":  # Checking if is bracket open
                self.next = Token(type=BRA_IN, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "}":  # Checking if is bracket close
                self.next = Token(type=BRA_OUT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "\n":  # Checking if is end
                self.next = Token(type=END, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == ";":  # Checking if is semicolumn
                self.next = Token(type=SEMICOLUMN, value=self.source[self.position])
                self.position += 1
                return
            elif re.match(
                "[a-zA-Z]", self.source[self.position]
            ):  # Checking if is IDENTIFIER
                val = ""
                while self.position < len(self.source) and re.match(
                    r"[a-zA-Z1-9_]", self.source[self.position]
                ):
                    val += self.source[self.position]
                    self.position += 1
                if val == PRINT:
                    self.next = Token(type=PRINT, value=str(val))
                elif val == SCAN:
                    self.next = Token(type=SCAN, value=str(val))
                elif val == IF:
                    self.next = Token(type=IF, value=str(val))
                elif val == ELSE:
                    self.next = Token(type=ELSE, value=str(val))
                elif val == FOR:
                    self.next = Token(type=FOR, value=str(val))
                elif val == VAR:
                    self.next = Token(type=VAR, value=str(val))
                elif val == T_INT:
                    self.next = Token(type=T_INT, value=str(val))
                elif val == T_STRING:
                    self.next = Token(type=T_STRING, value=str(val))
                else:
                    self.next = Token(type=IDENTIFIER, value=str(val))
                
                return
            elif self.source[self.position] == ">":  # Checking if is >
                self.next = Token(type=GT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "<":  # Checking if is <
                self.next = Token(type=LT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "!":  # Checking if is !
                self.next = Token(type=NOT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == ".":  # Checking if is .
                self.next = Token(type=CONCAT, value=self.source[self.position])
                self.position += 1
                return
            elif self.source[self.position] == "|":  # Checking if is ||
                self.position += 1
                if self.source[self.position] == "|":
                    self.next = Token(type=OR, value=self.source[self.position])
                    self.position += 1
                    return
                else:
                    raise Exception("| is not valid, try ||")
            elif self.source[self.position] == "=":  # Checking if is =
                self.position += 1
                if self.source[self.position] == "=": # Checking if is ==
                    self.next = Token(type=COMPARE, value=self.source[self.position])
                    self.position += 1
                else:
                    self.next = Token(type=EQUAL, value=self.source[self.position - 1])
                return
            elif self.source[self.position] == "&":  # Checking if is &&
                self.position += 1
                if self.source[self.position] == "&":
                    self.next = Token(type=AND, value=self.source[self.position])
                    self.position += 1
                    return
                else:
                    raise Exception("& is not valid, try &&")
            elif self.source[self.position] == " ":  # jumping spaces
                self.position += 1
                continue
            else:
                raise Exception("Not a Token")


class ParserError(Exception):
    pass


class Parser:
    tokens = None

    def parseProgram(self):
        childrens = []
        while self.tokens.next.type != EOF:
            childrens.append(self.parseStatement())
        return childrens

    def parseBlock(self):
        childrens = []
        if self.tokens.next.type == BRA_IN:
            self.tokens.selectNext()
            if self.tokens.next.type == END:
                self.tokens.selectNext()
                while self.tokens.next.type != BRA_OUT:
                    node = self.parseStatement()
                    childrens.append(node)
                self.tokens.selectNext()
        master = Block("Block", childrens)
        return master

    def parseBoolExpression(self):
        node = self.parseBoolTerm()

        while self.tokens.next.type == OR:
            self.tokens.selectNext()
            node = BinOp(OR, [node, self.parseBoolTerm()])

        if self.tokens.next.type == INT:
            raise Exception("Code Incorrect")

        return node

    def parseBoolTerm(self):
        node = self.parseRelExpression()

        while self.tokens.next.type == AND:
            self.tokens.selectNext()
            node = BinOp(AND, [node, self.parseRelExpression()])

        if self.tokens.next.type == INT:
            raise Exception("Code Incorrect")
        return node

    def parseRelExpression(self):
        node = self.parseExpression()
        while (
            self.tokens.next.type == COMPARE
            or self.tokens.next.type == GT
            or self.tokens.next.type == LT
        ):
            if self.tokens.next.type == COMPARE:
                self.tokens.selectNext()
                node = BinOp(COMPARE, [node, self.parseExpression()])
            elif self.tokens.next.type == GT:
                self.tokens.selectNext()
                node = BinOp(GT, [node, self.parseExpression()])
            elif self.tokens.next.type == LT:
                self.tokens.selectNext()
                node = BinOp(LT, [node, self.parseExpression()])

        if self.tokens.next.type == INT:
            raise Exception("Code Incorrect")

        return node

    def parseStatement(self):
        # print(self.tokens.next.type)
        if self.tokens.next.type == IDENTIFIER:
            variable = Identifier(self.tokens.next.value, [])
            self.tokens.selectNext()
            if self.tokens.next.type == EQUAL:
                self.tokens.selectNext()
                variable = Assigment(EQUAL, [variable, self.parseBoolExpression()])
            else:
                raise Exception("Not supported operation")
        elif self.tokens.next.type == PRINT:
            self.tokens.selectNext()
            if self.tokens.next.type == PAR_IN:
                self.tokens.selectNext()
                variable = Println(PRINT, [self.parseBoolExpression()])
                if self.tokens.next.type == PAR_OUT:
                    self.tokens.selectNext()
                    if self.tokens.next.type == END or self.tokens.next.type == EOF:
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code Incorrect")
                else:
                    # print(self.tokens.next.type)
                    raise Exception("Code is Incorrect")
        elif self.tokens.next.type == VAR:
            self.tokens.selectNext()
            if self.tokens.next.type == IDENTIFIER:
                name = self.tokens.next.value
                self.tokens.selectNext()
                if self.tokens.next.type in [T_INT,T_STRING]:
                    variable_type = self.tokens.next.type
                    self.tokens.selectNext()
                    if self.tokens.next.type == EQUAL:
                        self.tokens.selectNext()
                        variable = VarDec(variable_type,[name,self.parseBoolExpression()])
                    elif self.tokens.next.type == EOF or self.tokens.next.type == END:
                        variable = VarDec(variable_type,[name])
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code is Incorrect")
        elif self.tokens.next.type == IF:
            self.tokens.selectNext()
            condition_node = self.parseBoolExpression()
            node = self.parseBlock()
            if self.tokens.next.type == END or self.tokens.next.type == EOF:
                variable = IFNode(IF, [condition_node, node])
            else:
                if self.tokens.next.type == ELSE:
                    self.tokens.selectNext()
                    variable = IFNode(IF, [condition_node, node, self.parseBlock()])
                    if self.tokens.next.type == END:
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code Incorrect")
                else:
                    raise Exception("Code Incorrect")
        elif self.tokens.next.type == FOR:
            self.tokens.selectNext()
            if self.tokens.next.type == IDENTIFIER:
                variable = Identifier(self.tokens.next.value, [])
                self.tokens.selectNext()
                if self.tokens.next.type == EQUAL:
                    self.tokens.selectNext()
                    a = Assigment(EQUAL, [variable, self.parseBoolExpression()]) # for init
                    if self.tokens.next.type == SEMICOLUMN:
                        self.tokens.selectNext()
                        b = self.parseBoolExpression() # for condition
                        if self.tokens.next.type == SEMICOLUMN:
                            self.tokens.selectNext()
                            if self.tokens.next.type == IDENTIFIER:
                                variable = Identifier(self.tokens.next.value, [])
                                self.tokens.selectNext()
                                if self.tokens.next.type == EQUAL:
                                    self.tokens.selectNext()
                                    c = Assigment(EQUAL, [variable, self.parseBoolExpression()]) # for increment
                                    block = self.parseBlock()
                                    variable = FORNode(IF,[a,b,block,c])
                                    if self.tokens.next.type == END or self.tokens.next.type == EOF:
                                        self.tokens.selectNext()
                                    else:
                                        raise Exception("Code Incorrect")
                                else:
                                    raise Exception("Not supported operation")
                            else:
                                raise Exception("for assignment ; condition; expression {block}")
                        else:
                            raise Exception("for assignment ; condition; expression {block}")
                    else:
                        raise Exception("for assignment ; condition; expression {block}")  
                else:
                    raise Exception("for assignment ; condition; expression {block}")
        elif self.tokens.next.type == END:
            self.tokens.selectNext()
            variable = NoOp("NoOp", [])
        else:
            # print(self.tokens.next.type)
            raise Exception("Code Incorrect")
        
        return variable

    def parseExpression(self):
        node = self.parseTerm()
        while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS or self.tokens.next.type==CONCAT:
            if self.tokens.next.type == PLUS:
                self.tokens.selectNext()
                node = BinOp(PLUS, [node, self.parseTerm()])
            elif self.tokens.next.type == MINUS:
                self.tokens.selectNext()
                node = BinOp(MINUS, [node, self.parseTerm()])
            elif self.tokens.next.type == CONCAT:
                self.tokens.selectNext()
                node = BinOp(CONCAT, [node, self.parseTerm()])

        if self.tokens.next.type == INT or self.tokens.next.type == STR:
            raise Exception("Code Incorrect")

        return node

    def parseTerm(self):
        node = self.parseFactor()
        while self.tokens.next.type == TIMES or self.tokens.next.type == DIV:
            if self.tokens.next.type == TIMES:
                self.tokens.selectNext()
                node = BinOp(TIMES, [node, self.parseFactor()])
            elif self.tokens.next.type == DIV:
                self.tokens.selectNext()
                node = BinOp(DIV, [node, self.parseFactor()])
            else:
                raise Exception("Code Incorrect")

        return node

    def parseFactor(self):
        node = 0
        if self.tokens.next.type == INT:  # Number
            node = IntVal(self.tokens.next.value, [])
            self.tokens.selectNext()
            if self.tokens.next.type == INT:
                raise Exception("Code Incorrect")
        elif self.tokens.next.type == STR: # String
            node = StrVal(self.tokens.next.value, [])
            self.tokens.selectNext()
        elif self.tokens.next.type == IDENTIFIER:  # Identifier
            node = Identifier(self.tokens.next.value, [])
            self.tokens.selectNext()
        elif self.tokens.next.type == PLUS:  # Plus signal
            self.tokens.selectNext()
            node = UnOp(PLUS, [self.parseFactor()])
        elif self.tokens.next.type == MINUS:  # Minus signal
            self.tokens.selectNext()
            node = UnOp(MINUS, [self.parseFactor()])
        elif self.tokens.next.type == NOT:  # Not signal
            self.tokens.selectNext()
            node = UnOp(NOT, [self.parseFactor()])
        elif self.tokens.next.type == PAR_IN:  # Parenteshis open
            self.tokens.selectNext()
            node = self.parseBoolExpression()
            if self.tokens.next.type == PAR_OUT:
                self.tokens.selectNext()
            else:
                raise Exception("Code Incorrect")
        elif self.tokens.next.type == SCAN:
            self.tokens.selectNext()
            if self.tokens.next.type == PAR_IN:
                self.tokens.selectNext()
                node = Scanln(SCAN,[])
                if self.tokens.next.type != PAR_OUT:
                    raise Exception("Code Incorrect")
                self.tokens.selectNext()
        else:
            print(self.tokens.next.type)
            print(self.tokens.next.value)
            raise Exception("Code Incorrect")

        return node

    def run(self, code):
        filtered = PrePro(code).filter()
        identifier_table = SymbolTable()
        self.tokens = Tokenizer(filtered)
        self.tokens.selectNext()
        list_of_nodes = self.parseProgram()
        # print("Resposta: ")
        if self.tokens.next.type == EOF:
            for node in list_of_nodes:
                node.Evaluate(identifier_table)
            # print("Table")
            # print(identifier_table.table)
        else:
            raise Exception("Code Incorrect")


if __name__ == "__main__":
    chain = sys.argv[1]
    
    parser = Parser()
    
    final = parser.run(chain)
