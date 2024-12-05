import re

# ====== Token types ======

TOKEN_TYPES = {
    "NOTE": r"note",
    "PLAY": r"play",
    "REPEAT": r"repeat",
    "MELODY": r"melody", 
    "CHORD": r"chord", 
    "SHARP": r"//",  
    "FLAT": r"--",
    "ASSIGN": r"=",
    "STRING": r"\"[A-Ga-g#]+\"",
    "LIST": r"\[.*?\]",
    "NUMBER": r"\d+",
    "IDENTIFIER": r"[a-zA-Z_]\w*",
    "OPEN_BLOCK": r"\{",         
    "CLOSE_BLOCK": r"\}", 
    "WHITESPACE": r"\s+",
    "OTHER": r"."
}

# ====== Lexer function ======

def lexer(code):
    tokens = []
    while code:
        match = None
        for token_type, pattern in TOKEN_TYPES.items():
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                lexeme = match.group(0)
                print(f"Debug: Matched {token_type} -> {lexeme}")  
                if token_type != "WHITESPACE":  
                    tokens.append((token_type, lexeme))
                code = code[len(lexeme):]
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[0]}")
    return tokens


# ====== Read the example D# file ====== 

with open("program.ds", "r") as file:
    dsharp_code = file.read()

# ====== Tokenize the code ======

tokens = lexer(dsharp_code)
for token in tokens:
    print(token)
