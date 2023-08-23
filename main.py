from dataclasses import asdict
import json
from formula_parser.evaluator import evaluate_token_nodes
from formula_parser.supported_functions import Functions
from formula_parser.types import TokenNode
from formula_parser.node_generator import get_token_nodes


formula = '{estimation} - {budget} * {loggedTime}'
tokenNodes = get_token_nodes(formula)

item = {
  "id": 1,
  "title": 'Sample',
  "estimation": 8,
  "budget": 3,
  "loggedTime": 2.2
}

def get_item_property(property_name):
  return item[property_name]

result = evaluate_token_nodes(tokenNodes, get_item_property) 

# print(json.dumps([asdict(x) for x in tokenNodes], indent=2, default=lambda x: str(x)))
# print(json.dumps(SupportedFunctions().__dict__, indent=2, default=lambda x: str(x)))

print(result)