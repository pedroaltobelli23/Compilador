import sys
import re


PLUS = "+"
MINUS = "-"
TIMES = "*"
DIV = "/"
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
            elif self.source[self.position] == " ":
                self.position += 1
                continue
            else:
                raise Exception("Incorrect value")


class ParserError(Exception):
    pass


class Parser:
    tokens = None
    total = 0

    def parseExpression(self):
        # start at the parseTerm function
        self.total += self.parseTerm()
        while self.tokens.next.type == PLUS or self.tokens.next.type == MINUS:
            if self.tokens.next.type == PLUS:
                left = self.parseTerm()
                self.total += left

            if self.tokens.next.type == MINUS:
                left = self.parseTerm()
                self.total -= left

        if self.tokens.next.type == EOF:
            return self.total
        else:
            print(self.tokens.next.type)
            raise Exception("Code don't make sense")

    def parseTerm(self):
        self.tokens.selectNext()
        first_token = self.tokens.next
        # checking if first token is INT
        if first_token.type == INT:
            totalTerm = int(first_token.value)
            self.tokens.selectNext()
            while self.tokens.next.type == TIMES or self.tokens.next.type == DIV:
                if self.tokens.next.type == TIMES:
                    self.tokens.selectNext()
                    if self.tokens.next.type == INT:
                        totalTerm *= int(self.tokens.next.value)
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code don't make sense")
                if self.tokens.next.type == DIV:
                    self.tokens.selectNext()
                    if self.tokens.next.type == INT:
                        totalTerm //= int(self.tokens.next.value)
                        self.tokens.selectNext()
                    else:
                        raise Exception("Code don't make sense")
            if (
                self.tokens.next.type == PLUS
                or self.tokens.next.type == MINUS
                or self.tokens.next.type == EOF
            ):
                return totalTerm
            else:
                raise Exception("Code donn't make sense")
        else:
            raise Exception("Code don't make sense")

    def run(self, code):
        self.tokens = Tokenizer(code)
        return self.parseExpression()


if __name__ == "__main__":
    chain = sys.argv[1]

    # # cleaning string
    # for char in raw_chain:
    #     if char != " ":
    #         chain += char

    parser = Parser()

    final = parser.run(chain)
    print(final)
