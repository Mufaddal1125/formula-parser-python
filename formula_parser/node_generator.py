from typing import List

from formula_parser.lexer import get_tokens
from .types import Token, TokenType, TokenNode
from .operator_precedence import apply_operator_precedence, fix_operators_at_the_beginning

def get_corresponding_bracket_end_index(tokens: List[Token], index: int):
    level = 0
    while True:
        if tokens[index].type == TokenType.BracketStart:
            level += 1
        elif tokens[index].type == TokenType.BracketEnd:
            level -= 1
        index += 1
        if not (level > 0 or index < len(tokens)):
            break
    return index

def build_token_node_tree(tokens: List[Token], level=0):
    # print(f'build_token_node_tree {tokens} {level}')

    nodes = []
    filtered_tokens = tokens if level else [token for token in tokens if token.type in meaningful_types]
    
    i = 0
    while i < len(filtered_tokens):
        token = filtered_tokens[i]
        if token.type in [TokenType.String, TokenType.Number, TokenType.ReferenceName]:
            add_node(nodes, TokenNode(token.type, token.value, []))
        elif token.type == TokenType.Operator:
            last_node = nodes.pop() if nodes else None
            nodes.append(TokenNode(token.type, token.value, [last_node] if last_node else []))
        elif token.type == TokenType.FunctionName:
            offset = 1 if filtered_tokens[i + 1].type == TokenType.BracketStart else 0
            next_i = get_corresponding_bracket_end_index(filtered_tokens, i + 1)
            inner_nodes = build_token_node_tree(filtered_tokens[i + 1 + offset:next_i - offset], level + 1)
            add_node(nodes, TokenNode(token.type, token.value, inner_nodes))
            i = next_i - offset
        elif token.type == TokenType.BracketStart:
            next_i = get_corresponding_bracket_end_index(filtered_tokens, i)
            inner_nodes = build_token_node_tree(filtered_tokens[i + 1:next_i], level + 1)
            add_node(nodes, TokenNode(TokenType.Group, '', inner_nodes))
            i = next_i - 1
        i += 1
    return nodes

def add_node(nodes: List[TokenNode], node: TokenNode):
    last_node = nodes[-1] if nodes else None
    if last_node and last_node.type == TokenType.Operator and len(last_node.innerNodes) < 2:
        last_node.innerNodes.append(node)
    else:
        nodes.append(node)

meaningful_types = [TokenType.String, TokenType.Number, TokenType.ReferenceName, TokenType.Operator, TokenType.FunctionName, TokenType.BracketStart, TokenType.BracketEnd]

def get_token_nodes(formula: str, skip_operator_precedence=False):
    # print('formula', formula)
    tokens = get_tokens(formula)
    if skip_operator_precedence:
        return build_token_node_tree(fix_operators_at_the_beginning(tokens))
    else:
        return build_token_node_tree(apply_operator_precedence(fix_operators_at_the_beginning(tokens)))
