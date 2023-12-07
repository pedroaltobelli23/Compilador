import re

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