#include "lexer.h"

const std::unordered_map<TokenType, std::string> Lexer::TOKEN_PATTERNS = {
    {TokenType::NOTE, R"(note)"},
    {TokenType::PLAY, R"(play)"},
    {TokenType::REPEAT, R"(repeat)"},
    {TokenType::MELODY, R"(melody)"},
    {TokenType::CHORD, R"(chord)"},
    {TokenType::SHARP, R"(//)"},
    {TokenType::FLAT, R"(--)"},
    {TokenType::ASSIGN, R"(=)"},
    {TokenType::STRING, R"("[A-Ga-g#]+")"},
    {TokenType::LIST, R"(\[.*?\])"},
    {TokenType::NUMBER, R"(\d+)"},
    {TokenType::IDENTIFIER, R"([a-zA-Z_]\w*)"},
    {TokenType::OPEN_BLOCK, R"(\{)"},
    {TokenType::CLOSE_BLOCK, R"(\})"},
    {TokenType::WHITESPACE, R"(\s+)"},
    {TokenType::OTHER, R"(.)"}};

Lexer::Lexer(const std::string &src) : code(src) {}

bool Lexer::is_at_end() const
{
    return current >= code.length();
}

Token Lexer::match_token()
{
    for (const auto &[type, pattern] : TOKEN_PATTERNS)
    {
        std::smatch match;
        std::string remaining = code.substr(current);

        if (std::regex_search(remaining, match, std::regex(pattern, std::regex_constants::match_continuous)))
        {
            std::string lexeme = match.str(0);
            current += lexeme.length();

            std::cout << "Debug: Matched " << lexeme << "\n";
            return {type, lexeme};
        }
    }
    return {TokenType::OTHER, std::string(1, code[current++])};
}

std::vector<Token> Lexer::tokenize()
{
    std::vector<Token> tokens;
    while (!is_at_end())
    {
        Token token = match_token();
        if (token.type != TokenType::WHITESPACE)
        {
            tokens.push_back(token);
        }
    }
    return tokens;
}
