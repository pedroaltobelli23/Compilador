class SymbolTable:
    def __init__(self):
        self.table = dict()
        self.id = 1

    def getter(self, identifier):
        try:
            return self.table[identifier]
        except:
            raise Exception(f"{identifier} variable dont exist")
        
    def create(self, identifier, type):
        if identifier in self.table.keys():
            raise Exception("variable already exists")
        else:
            self.table[identifier] = (None,type,self.id)
            self.id+=1

    def setter(self, identifier, value):
        if identifier not in self.table.keys():
            raise Exception("variable not declared")
        else:
            # print(self.table[identifier])
            if (self.table[identifier][1] == value[1]):
                self.table[identifier] = (value[0],value[1],self.table[identifier][2])
                # print(self.table[identifier])
            else:
                raise Exception("Type Mismatch")