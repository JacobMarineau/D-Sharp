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
            return self.assignment("Note")
        elif self.match("MELODY"):
            return self.assignment("Melody")
        elif self.match("CHORD"):
            return self.assignment("Chord")
        elif self.match("PLAY"):
            return self.play_statement()
        elif self.peek()[1] == "notation":  
            return self.script_statement()
        elif self.match("REPEAT"):
            return self.repeat_statement()
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")


    def assignment(self, type_):
        name = self.match("IDENTIFIER")
        if not name:
            raise SyntaxError(f"Expected an identifier for {type_}, but found {self.peek()}.")

        self.match("ASSIGN")
        value = self.match("STRING", "LIST")
        if not value:
            raise SyntaxError(f"Expected a value (STRING or LIST) after '=', but found {self.peek()}.")

        self.match("OTHER")  # Consume ';'
        return {"type": type_, "name": name[1], "value": eval(value[1])}


    def play_statement(self):
        target_type = None

        # Check if the target is a specific type (e.g., CHORD, MELODY)
        if self.match("CHORD"):
            target_type = "Chord"
        elif self.match("MELODY"):
            target_type = "Melody"

        # Match the actual identifier for the target (e.g., a variable name)
        target = self.match("IDENTIFIER")
        if not target:
            raise SyntaxError(f"Expected an identifier after 'play', found {self.peek()}.")

        modifier = None
        operation = []

        # Handle sharp (//) or flat (--)
        if self.match("SHARP"):
            modifier = "sharp"
        elif self.match("FLAT"):
            modifier = "flat"

        # Handle operations like 'base + 2' or 'base - 4'
        while self.peek()[1] in {"+", "-"}:
            op = self.advance()  # Consume '+' or '-'
            semitones = self.match("NUMBER")
            if not semitones:
                raise SyntaxError(f"Expected a number after '{op[1]}', found {self.peek()}.")
            operation.append({"operator": op[1], "value": int(semitones[1])})

        # Verify and consume the semicolon
        semicolon = self.match("OTHER")
        if not semicolon or semicolon[1] != ";":
            raise SyntaxError(f"Expected ';' at the end of 'play' statement, found {self.peek()}.")

        # Debug: Log consumption of semicolon
        print(f"Debug: Successfully consumed semicolon after 'play' statement.")

        return {
            "type": "Play",
            "target": target[1],
            "target_type": target_type,
            "modifier": modifier,
            "operation": operation,
        }



    def repeat_statement(self):
        times = self.match("NUMBER")
        self.match("IDENTIFIER")  # Consume "times"
        self.match("OPEN_BLOCK")
        body = []
        while not self.match("CLOSE_BLOCK"):
            body.append(self.statement())
        return {"type": "Repeat", "times": int(times[1]), "body": body}

    def script_statement(self):
        self.match("IDENTIFIER")  # Consume 'notation'
        name = self.match("IDENTIFIER")
        if not name:
            raise SyntaxError(f"Expected a notation name, found {self.peek()}.")

        print(f"Debug: Parsing notation '{name[1]}'")

        args = []
        if self.match("OTHER") and self.peek()[1] == "(":
            self.advance()  # Consume '('
            while True:
                arg_type = self.match("NOTE", "IDENTIFIER")
                if not arg_type:
                    raise SyntaxError(f"Expected argument type, found {self.peek()}.")

                arg_name = self.match("IDENTIFIER")
                if not arg_name:
                    raise SyntaxError(f"Expected argument name, found {self.peek()}.")

                args.append({"type": arg_type[1], "name": arg_name[1]})

                if self.peek()[1] == ")":  # End of arguments
                    self.advance()  # Consume ')'
                    break
                elif self.peek()[1] == ",":
                    self.match("OTHER")  # Consume ','

            print(f"Debug: Completed parsing arguments: {args}")

        # Debugging tokens leading up to '{'
        print(f"Debug: Tokens ahead before '{{': {self.tokens[self.current:self.current+5]}")

        # Skip WHITESPACE only
        while self.peek()[0] == "WHITESPACE":
            print(f"Debug: Skipping whitespace before '{{'.")
            self.advance()

        # Expect '{' to open the notation body
        if not self.match("OPEN_BLOCK"):
            raise SyntaxError(f"Expected '{{' to start notation body, found {self.peek()}.")

        body = []
        while not self.match("CLOSE_BLOCK"):
            print(f"Debug: Parsing body statement. Next token: {self.peek()}")
            if self.peek()[0] == "PLAY":
                body.append(self.play_statement())  # Parse play statements correctly
            else:
                body.append(self.statement())

        print(f"Debug: Completed parsing notation '{name[1]}'.")
        return {"type": "Notation", "name": name[1], "arguments": args, "body": body}

    def advance(self):
        token = self.tokens[self.current]
        self.current += 1
        print(f"Debug: Consumed token {token}")  # Track each token
        return token


# Parse tokens from the lexer
if __name__ == "__main__":
    with open("program.ds", "r") as file:
        dsharp_code = file.read()

    tokens = lexer.lexer(dsharp_code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
