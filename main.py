import sys
from compiler.parserP import Parser

if __name__ == "__main__":
    chain = sys.argv[1]
    
    parser = Parser()
    
    final = parser.run(chain)
