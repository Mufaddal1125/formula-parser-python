### JS
# import { type TokenNode, TokenType } from './types'
# import { executeFunction, executeOperator } from './supportedFunctions'

# export function evaluateTokenNodes (tokenNodes: TokenNode[], getPropertyValue: (v: string) => string): string {
#   let result = ''
#   for (const node of tokenNodes) {
#     result += evaluateNode(node, getPropertyValue)
#   }
#   return result
# }

# function evaluateNode (node: TokenNode, getPropertyValue: (v: string) => string): string {
#   if (node.type === TokenType.Operator) {
#     const parameters = node.innerNodes.map((x) => evaluateNode(x, getPropertyValue))
#     return executeOperator(node.value, parameters)
#   } else if (node.type === TokenType.FunctionName) {
#     const parameters = node.innerNodes.map((x) => evaluateNode(x, getPropertyValue))
#     return executeFunction(node.value, parameters)
#   } else if (node.type === TokenType.ReferenceName) {
#     return getPropertyValue(node.value)
#   } else if (node.type === TokenType.String) {
#     return node.value
#   } else if (node.type === TokenType.Number) {
#     return node.value
#   } else if (node.type === TokenType.Group) {
#     return node.innerNodes.reduce((out, childNode) => out + evaluateNode(childNode, getPropertyValue), '')
#   }
#   return ''
# }

from typing import Callable, List
from .types import TokenNode, TokenType
from .supported_functions import execute_function, execute_operator

def evaluate_token_nodes(tokenNodes: List[TokenNode], get_property_value: Callable[[str], str]):
    result = ''
    for node in tokenNodes:
        result += evaluate_node(node, get_property_value)
    return result


def evaluate_node(node: TokenNode, get_property_value: Callable[[str], str]):
    if node.type == TokenType.Operator:
        parameters = [evaluate_node(x, get_property_value) for x in node.innerNodes]
        return execute_operator(node.value, parameters)
    elif node.type == TokenType.FunctionName:
        parameters = [evaluate_node(x, get_property_value) for x in node.innerNodes]
        return execute_function(node.value, parameters)
    elif node.type == TokenType.ReferenceName:
        return get_property_value(node.value)
    elif node.type == TokenType.String:
        return node.value
    elif node.type == TokenType.Number:
        return node.value
    elif node.type == TokenType.Group:
        return ''.join([str(evaluate_node(childNode, get_property_value)) for childNode in node.innerNodes])
    return ''