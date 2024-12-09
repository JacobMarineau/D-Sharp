#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <vector>
#include <regex>
#include <iostream>
#include <unordered_map>

enum class TokenType {
    NOTE, PLAY, REPEAT, MELODY, CHORD, SHARP, FLAT,
    ASSIGN, STRING, LIST, NUMBER, IDENTIFIER,
    OPEN_BLOCK, CLOSE_BLOCK, WHITESPACE, OTHER
};

struct Token {
    TokenType type;
    std::string lexeme;
};

class Lexer {
public:
    explicit Lexer(const std::string& code);
    std::vector<Token> tokenize();

private:
    std::string code;
    size_t current = 0;

    bool is_at_end() const;
    Token match_token();
    static const std::unordered_map<TokenType, std::string> TOKEN_PATTERNS;
};

#endif
