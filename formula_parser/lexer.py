import re
from formula_parser.types import LexerStream, Token
from formula_parser.tokenizer import getNextToken
from formula_parser.types import TokenType


def get_tokens(formula):
    # print('get_tokens')
    return process_token_stream(formula)


def process_token_stream(formula):
    # print('process_token_stream')
    tokens = []
    position = 0

    def skip(amount=1):
        nonlocal position
        position += amount

    def match(pattern, move=False, take=0):
        nonlocal position
        match_obj = re.match(pattern, formula[position:])
        if match_obj:
            if move:
                position += len(match_obj.group(take) or '')
            return match_obj.group(take)

    prev = None

    while position < len(formula):
        starting_position = position
        token_type = getNextToken(lexer_stream=LexerStream(match, skip, prev))
        if starting_position == position:
            raise Exception('Tokenizer did not move forward')
        
        if token_type == TokenType.EmptyStringAndDoubleQuoteEnd:
            token = Token(TokenType.String, '')
            tokens.append(token)
            token_type = TokenType.DoubleQuoteEnd
        elif token_type == TokenType.EmptyStringAndQuoteEnd:
            token = Token(TokenType.String, '')
            tokens.append(token)
            token_type = TokenType.QuoteEnd
        
        token = Token(token_type, formula[starting_position:position])
        tokens.append(token)

        if token_type != TokenType.Whitespace:
            prev = token_type
    
    return tokens
