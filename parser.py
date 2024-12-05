import lexer 

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        ast = {"type": "Program", "body": []}
        while not self.is_at_end():
            ast["body"].append(self.statement())
        return ast

    def is_at_end(self):
        return self.current >= len(self.tokens)

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.tokens[self.current]
        self.current += 1
        return token

    def match(self, *token_types):
        if not self.is_at_end() and self.peek()[0] in token_types:
            return self.advance()
        return None

    def statement(self):
        if self.match("NOTE"):
            return self.assignment()
        elif self.match("PLAY"):
            return self.play_statement()
        elif self.match("REPEAT"):
            return self.repeat_statement()
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def assignment(self):
        name = self.match("IDENTIFIER")
        self.match("ASSIGN")
        value = self.match("STRING", "LIST")
        self.match("OTHER")  # Consume ';'
        return {"type": "Assignment", "name": name[1], "value": value[1]}

    def play_statement(self):
        target = self.match("IDENTIFIER")
        self.match("OTHER")  # Consume ';'
        return {"type": "Play", "target": target[1]}

    def repeat_statement(self):
        times = self.match("NUMBER")
        self.match("IDENTIFIER")  # Consume "times"
        self.match("OPEN_BLOCK")
        body = []
        while not self.match("CLOSE_BLOCK"):
            body.append(self.statement())
        return {"type": "Repeat", "times": int(times[1]), "body": body}

# Parse tokens from the lexer
if __name__ == "__main__":
    with open("program.ds", "r") as file:
        dsharp_code = file.read()

    tokens = lexer.lexer(dsharp_code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
