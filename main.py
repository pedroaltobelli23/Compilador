import sys
import re


PLUS = "+"
MINUS = "-"
INT = "INTEGER"
EOF = "End of File"


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
                        self.next = Token(type=type, value=value)
                        return
                type = INT
                self.next = Token(type=type, value=value)
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
        self.tokens.selectNext()  # get first token
        # print(self.tokens.next.value)
        first_token = self.tokens.next
        total = 0
        # checking if first token is INT
        if first_token.type == INT:
            total = int(first_token.value)
            self.tokens.selectNext()
            # print(self.tokens.next.value)
            while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS:
                if self.tokens.next.type == PLUS:
                    self.tokens.selectNext()
                    if self.tokens.next.type == INT:
                        total += int(self.tokens.next.value)
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code don't make sense")
                if self.tokens.next.type == MINUS:
                    self.tokens.selectNext()
                    if self.tokens.next.type == INT:
                        total -= int(self.tokens.next.value)
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code don't make sense")
                return total
            else:
                # if self.tokens.next.type == EOF:
                #     return total
                # else:
                raise Exception("Code don't make sense")
        else:
            raise Exception("Code don't make sense")

    def run(self, code):
        self.tokens = Tokenizer(code)
        return self.parseExpression()


if __name__ == "__main__":
    # source = "input.txt"

    # raw_chain = ""
    # with open(source,"r") as f:
    #     raw_chain = f.read()

    # chain = ""
    # for char in raw_chain:
    #     if char != ' ':
    #         chain += char

    # with open(source,'w') as f:
    #     f.write(chain)

    chain = sys.argv[1]

    # # cleaning string
    # for char in raw_chain:
    #     if char != " ":
    #         chain += char

    parser = Parser()

    final = parser.run(chain)
    print(final)

    # a = Tokenizer(chain)
    # a.selectNext()
    # print(a.next.value)
    # a.selectNext()
    # print(a.next.value)
    # a.selectNext()
    # print(a.next.value)
