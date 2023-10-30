class SymbolTable:
    def __init__(self):
        self.table = dict()

    def getter(self, identifier):
        try:
            return self.table[identifier]
        except:
            raise Exception(f"{identifier} variable dont exist")
        
    def create(self, identifier, type):
        if identifier in self.table.keys():
            raise Exception("variable already exists")
        else:
            self.table[identifier] = (None,type)

    def setter(self, identifier, value):
        if identifier not in self.table.keys():
            raise Exception("variable not declared")
        else:
            # print(self.table[identifier])
            if (self.table[identifier][1] == value[1]):
                self.table[identifier] = value
            else:
                raise Exception("Type Mismatch")

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table: SymbolTable):
        pass


class BinOp(Node):
    def Evaluate(self, table: SymbolTable):
        var1 = self.children[0].Evaluate(table)
        var2 = self.children[1].Evaluate(table)
        if var1[1] == "int" and var2[1] == "int":
            if self.value == "+":
                return (var1[0] + var2[0],"int")
            elif self.value == "-":
                return (var1[0] - var2[0],"int")
            if self.value == "*":
                return (var1[0] * var2[0],"int")
            elif self.value == "/":
                return (var1[0] // var2[0],"int")
            elif self.value == "||":
                return (var1[0] | var2[0],"int")
            elif self.value == "&&":
                return (var1[0] & var2[0],"int")
            elif self.value == "==":
                return (var1[0] == var2[0],"int")
            elif self.value == ">":
                return (var1[0] > var2[0],"int")
            elif self.value == "<":
                return (var1[0] < var2[0],"int")
            else:
                raise Exception("Error")
        elif var1[1] == "str" and var2[1] == "str":
            if self.value == ".":
                return (var1[0]+var2[0],"str")
            else:
                raise Exception("Error")
        else:
            raise Exception("Error")

class UnOp(Node):
    def Evaluate(self, table: SymbolTable):
        var = self.children[0].Evaluate(table)
        if (var[1] == "int"):  
            if self.value == "+":
                return (1 * var[0] , var[1])
            elif self.value == "-":
                return (-1 * var[0],var[1])
            elif self.value == "!":
                return (not (var[0]), var[1])
            else:
                raise Exception("Error")
        else:
            raise Exception("Error")

class IntVal(Node):
    def Evaluate(self, table: SymbolTable):
        return (self.value,"int")
    
class StrVal(Node):
    def Evaluate(self, table: SymbolTable):
        return (self.value,"str")

class NoOp(Node):
    def Evaluate(self, table: SymbolTable):
        pass

class Identifier(Node):
    def Evaluate(self, table: SymbolTable):
        # print(table.getter(self.value))
        return table.getter(self.value)

class VarDec(Node):
    def Evaluate(self, table: SymbolTable):
        table.create(self.children[0],self.value)
        if len(self.children)>1:
            table.setter(self.children[0],self.children[1].Evaluate(table))

class Assigment(Node):
    def Evaluate(self, table: SymbolTable):
        table.setter(self.children[0].value, self.children[1].Evaluate(table))

class Println(Node):
    def Evaluate(self, table: SymbolTable):
        print(self.children[0].Evaluate(table)[0])
        
class Scanln(Node):
    # only work with int, for now
    def Evaluate(self, table: SymbolTable):
        return (int(input()),"int")

class Block(Node):
    def Evaluate(self, table: SymbolTable):
        for node in self.children:
            node.Evaluate(table)
            
class IFNode(Node):
    def Evaluate(self, table: SymbolTable):
        if self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        elif len(self.children) > 2:
            self.children[2].Evaluate(table)

class FORNode(Node):
    def Evaluate(self, table: SymbolTable):
        self.children[0].Evaluate(table)
        while self.children[1].Evaluate(table)[0]:
            self.children[2].Evaluate(table)
            self.children[3].Evaluate(table)