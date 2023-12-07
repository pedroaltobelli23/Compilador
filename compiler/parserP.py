import sys
import re
from compiler.prepro import PrePro
from compiler.tokenizer import *
from compiler.abstractsyntaxtree import (
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
        if self.tokens.next.type == EOF:
            for node in list_of_nodes:
                node.Evaluate(identifier_table)
            new_file = code.replace("go","asm")
            f = open(new_file,"w")
            f.write(Node.endcode())
            f.close()
        else:
            raise Exception("Code Incorrect")