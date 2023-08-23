
from formula_parser.types import LexerStream, TokenType


def getNextToken(lexer_stream: LexerStream):
    # print('getNextToken')
    def match_and_return(pattern, token_type):
        matched = lexer_stream.match(pattern, True)
        if matched is not None:
            return token_type

    prev = lexer_stream.prev

    if prev != TokenType.QuoteStart and lexer_stream.match(r'^"', True):
        if prev == TokenType.String:
            return TokenType.DoubleQuoteEnd
        elif prev == TokenType.DoubleQuoteStart:
            return TokenType.EmptyStringAndDoubleQuoteEnd
        else:
            return TokenType.DoubleQuoteStart

    if lexer_stream.match(r"^'", True):
        if prev == TokenType.String:
            return TokenType.QuoteEnd
        elif prev == TokenType.QuoteStart:
            return TokenType.EmptyStringAndQuoteEnd
        else:
            return TokenType.QuoteStart

    if prev == TokenType.DoubleQuoteStart:
        if lexer_stream.match(r'^([^"\\]|\\.)*(?=")', False):
            lexer_stream.match(r'^([^"\\]|\\.)*(?=")', True)
            return TokenType.String
        else:
            lexer_stream.match(r'^([^"\\]|\\.)*', True)
            return TokenType.String

    if prev == TokenType.QuoteStart:
        if lexer_stream.match(r"^([^'\\]|\\.)*(?=')", False):
            lexer_stream.match(r"^([^'\\]|\\.)*(?=')", True)
            return TokenType.String
        else:
            lexer_stream.match(r"^([^'\\]|\\.)*", True)
            return TokenType.String

    number_regex = r"^\d*\.\d+"
    if lexer_stream.match(number_regex, True):
        return TokenType.Number

    if prev == TokenType.ReferenceBracketStart:
        if lexer_stream.match(r"^[^{}]+(?=\})", False):
            lexer_stream.match(r"^[^{}]+(?=\})", True)
            return TokenType.ReferenceName
        elif lexer_stream.match(r"^[^{}]+", False):
            lexer_stream.match(r"^[^{}]+", True)
            return TokenType.ReferenceName

    rest = [
        (r"^(<=|==|>=)", TokenType.Operator),
        (r"^[+\-*/^<=>&]", TokenType.Operator),
        (r"^[a-zA-Z][a-zA-Z0-9]*(?=\s*\()", TokenType.FunctionName),
        (r"^\(", TokenType.BracketStart),
        (r"^\)", TokenType.BracketEnd),
        (r"^{", TokenType.ReferenceBracketStart),
        (r"^}", TokenType.ReferenceBracketEnd),
        (r"^,", TokenType.Comma),
        (r"^\s+", TokenType.Whitespace),
    ]

    for pattern, token_type in rest:
        matched_token = match_and_return(pattern, token_type)
        if matched_token:
            return matched_token

    lexer_stream.skip()
    return TokenType.Error