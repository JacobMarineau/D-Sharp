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
        print(f"Debug: Consumed token {token}")
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
            try:
                return self.play_statement()
            except SyntaxError as e:
                print(f"Debug: Skipping invalid play statement. Error: {e}")
                self.advance()
                return None
        elif self.peek()[1] == "notation":
            return self.script_statement()
        elif self.match("REPEAT"):
            return self.repeat_statement()
        else:
            print(f"Debug: Unexpected token {self.peek()}. Skipping...")
            self.advance()
            return None



    def assignment(self, type_):
        name = self.match("IDENTIFIER")
        if not name:
            raise SyntaxError(f"Expected an identifier for {type_}, but found {self.peek()}.")

        self.match("ASSIGN")
        value = self.match("STRING", "LIST")
        if not value:
            raise SyntaxError(f"Expected a value (STRING or LIST) after '=', but found {self.peek()}.")

        self.match("OTHER")
        return {"type": type_, "name": name[1], "value": eval(value[1])}

    def play_statement(self):
        target_type = None
        if self.match("CHORD"):
            target_type = "Chord"
        elif self.match("MELODY"):
            target_type = "Melody"

        target = self.match("IDENTIFIER")
        if not target:
            current_token = self.peek()
            if current_token[0] == "PLAY":
                print(f"Debug: Found misplaced 'play' keyword. Skipping...")
                self.advance()
                return None
            raise SyntaxError(f"Expected an identifier after 'play', found {current_token}.")

        modifier = None
        if self.match("SHARP"):
            modifier = "sharp"
        elif self.match("FLAT"):
            modifier = "flat"

        operation = []
        while not self.is_at_end() and self.peek()[1] in {"+", "-"}:
            op = self.advance()
            semitones = self.match("NUMBER")
            if not semitones:
                raise SyntaxError(f"Expected a number after '{op[1]}', found {self.peek()}.")
            operation.append({"operator": op[1], "value": int(semitones[1])})

        semicolon = self.match("OTHER")
        if not semicolon or semicolon[1] != ";":
            raise SyntaxError(f"Expected ';' at the end of 'play' statement, found {self.peek()}.")

        return {
            "type": "Play",
            "target": target[1],
            "target_type": target_type,
            "modifier": modifier,
            "operation": operation,
        }
    
    def parse_notation_body(self):
        body = []
        while not self.check("CLOSE_BLOCK") and not self.is_at_end():
            try:
                stmt = self.statement()
                if stmt is not None:
                    body.append(stmt)
            except SyntaxError as e:
                print(f"Debug: {str(e)}. Skipping token {self.peek()}.")
                self.advance()  
        self.consume("CLOSE_BLOCK", "Expected '}' to close notation block.")
        return body
    
    def notation_statement(self):
        name = self.consume("IDENTIFIER", "Expected notation name after 'notation'.")
        self.consume("OTHER", "Expected '(' after notation name.")
        args = self.parse_arguments()
        self.consume("OTHER", "Expected ')' after notation arguments.")
        self.consume("OPEN_BLOCK", "Expected '{' to open notation body.")
        body = self.parse_notation_body()
        return {
            "type": "Notation",
            "name": name[1],
            "arguments": args,
            "body": body,
        }



    def script_statement(self):
        self.match("IDENTIFIER")
        name = self.match("IDENTIFIER")
        if not name:
            raise SyntaxError(f"Expected a notation name, found {self.peek()}.")

        args = []
        if self.match("OTHER") and self.peek()[1] == "(":
            self.advance()
            while True:
                arg_type = self.match("NOTE", "IDENTIFIER")
                if not arg_type:
                    raise SyntaxError(f"Expected argument type, found {self.peek()}.")
                arg_name = self.match("IDENTIFIER")
                if not arg_name:
                    raise SyntaxError(f"Expected argument name, found {self.peek()}.")

                args.append({"type": arg_type[1], "name": arg_name[1]})
                if self.peek()[1] == ")":
                    self.advance()
                    break
                elif self.peek()[1] == ",":
                    self.match("OTHER")

        if not self.match("OPEN_BLOCK"):
            raise SyntaxError(f"Expected '{{' to start notation body, found {self.peek()}.")

        body = []
        while not self.match("CLOSE_BLOCK"):
            try:
                body.append(self.statement())
            except SyntaxError as e:
                print(f"Debug: Skipping invalid statement in notation body. Error: {e}")
                self.advance()

        return {"type": "Notation", "name": name[1], "arguments": args, "body": body}

    def repeat_statement(self):
        times = self.match("NUMBER")
        self.match("IDENTIFIER")
        self.match("OPEN_BLOCK")
        body = []
        while not self.match("CLOSE_BLOCK"):
            body.append(self.statement())
        return {"type": "Repeat", "times": int(times[1]), "body": body}

    def script_statement(self):
        self.match("IDENTIFIER") 
        name = self.match("IDENTIFIER")
        if not name:
            raise SyntaxError(f"Expected a notation name, found {self.peek()}.")

        print(f"Debug: Parsing notation '{name[1]}' with initial tokens: {self.tokens[self.current:self.current+5]}")

        args = []
        if self.peek()[1] == "(":
            self.advance()  
            while True:
                arg_type = self.match("NOTE", "IDENTIFIER")
                if not arg_type:
                    raise SyntaxError(f"Expected argument type, found {self.peek()}.")

                arg_name = self.match("IDENTIFIER")
                if not arg_name:
                    raise SyntaxError(f"Expected argument name, found {self.peek()}.")

                args.append({"type": arg_type[1], "name": arg_name[1]})

                if self.peek()[1] == ")":  
                    self.advance()  
                    break
                elif self.peek()[1] == ",":
                    self.match()  
                else:
                    raise SyntaxError(f"Expected ',' or ')', found {self.peek()}.")

            print(f"Debug: Completed parsing arguments: {args}, next tokens: {self.tokens[self.current:self.current+5]}")

        while self.peek()[0] == "WHITESPACE":
            self.advance()

        print(f"Debug: Tokens before '{{': {self.tokens[self.current:self.current+5]}")

        if not self.match("OPEN_BLOCK"):
            raise SyntaxError(f"Expected '{{' to start notation body, found {self.peek()}.")

        body = []
        while not self.match("CLOSE_BLOCK"):
            print(f"Debug: Parsing body statement. Next token: {self.peek()}")
            if self.peek()[0] == "PLAY":
                body.append(self.play_statement())
            else:
                body.append(self.statement())

        print(f"Debug: Completed parsing notation '{name[1]}'.")
        return {"type": "Notation", "name": name[1], "arguments": args, "body": body}

if __name__ == "__main__":
    with open("program.ds", "r") as file:
        dsharp_code = file.read()

    tokens = lexer.lexer(dsharp_code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
