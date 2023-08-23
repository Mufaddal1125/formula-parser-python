from typing import List
from .types import Token, TokenType, TokenNode

def apply_operator_precedence(tokens: List[Token]):
    # print('apply_operator_precedence')

    new_tokens = []

    operator_groups = ['^', '*/', '+-', '<=>=']
    operator_tokens = [token for token in tokens if token.type == TokenType.Operator]
    comma_exists = any(token.type == TokenType.Comma for token in tokens)
    max_brackets_count = len(operator_groups) + (1 if comma_exists else 0)

    for token in tokens:
        if token.type == TokenType.Operator:
            bracket_count = next((i for i, group in enumerate(operator_groups) if token.value in group), None)
            around_with_brackets(new_tokens, token, bracket_count)
        elif token.type == TokenType.Comma:
            around_with_brackets(new_tokens, token, len(operator_groups))
        elif token.type in [TokenType.BracketStart, TokenType.BracketEnd]:
            add_brackets(new_tokens, max_brackets_count, token.type)
        else:
            new_tokens.append(token)

    add_brackets(new_tokens, max_brackets_count, TokenType.BracketStart, True)
    add_brackets(new_tokens, max_brackets_count, TokenType.BracketEnd)

    return new_tokens

def fix_operators_at_the_beginning(tokens: List[Token]):
    # print('fix_operators_at_the_beginning')

    new_tokens = []
    prev_token = None

    for token in tokens:
        if token.type == TokenType.Operator and token.value in '+-':
            if not prev_token or prev_token.type in [TokenType.BracketStart, TokenType.Comma, TokenType.Operator]:
                new_tokens.append(Token(TokenType.Number, '0'))
        new_tokens.append(token)
        if token.type != TokenType.Whitespace:
            prev_token = token

    return new_tokens

def add_brackets(tokens: List[Token], count: int, type: str, to_start=False):
    bracket_type = ')' if type == TokenType.BracketEnd else '('
    for _ in range(count):
        if to_start:
            tokens.insert(0, Token(type, bracket_type))
        else:
            tokens.append(Token(type, bracket_type))

def around_with_brackets(tokens: List[Token], token: Token, count: int):
    add_brackets(tokens, count, TokenType.BracketEnd)
    tokens.append(token)
    add_brackets(tokens, count, TokenType.BracketStart)
