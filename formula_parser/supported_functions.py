from dataclasses import dataclass
import json
import math


def _element_at(array, index, default=None):
    """Returns the element at the given index or the default value if the index is out of bounds."""
    if index < len(array):
        return array[index]
    return default

def to_number_string(n):
    return str(round(n, 10))


def param_as_boolean_is_set(param):
    param = (param or "").lower()
    return param and param != "0" and param != "false" and param != "no"


def strip_last_zeroes_after_dot(param):
    if "." in param:
        return param.rstrip("0").rstrip(".")
    return param


def compare(params, operator):
    if len(params) < 2:
        return "0"
    p0 = float(params[0]) if params[0].replace(".", "", 1).isdigit() else params[0]
    p1 = float(_element_at(params, 1)) if _element_at(params, 1).replace(".", "", 1).isdigit() else _element_at(params, 1)
    if "=" in operator and p0 == p1:
        return "1"
    if "<" in operator and p0 < p1:
        return "1"
    if ">" in operator and p0 > p1:
        return "1"
    return "0"


def execute_operator(operator, parameters):
    # supported_operators = {
    #     "&": lambda params: "".join(params),
    #     "+": lambda params: str(sum(map(float, params))),
    #     "-": lambda params: str(float(params[0]) - sum(map(float, params[1:]))),
    #     "/": lambda params: str(
    #         float(params[0]) / (float(_element_at(params, 1)) if float(_element_at(params, 1)) != 0 else 1)
    #     ),
    #     "*": lambda params: str(math.prod(map(float, params))),
    #     "^": lambda params: to_number_string(float(params[0]) ** float(_element_at(params, 1))),
    #     "<": lambda params: compare(params, "<"),
    #     "<=": lambda params: compare(params, "<="),
    #     "=": lambda params: compare(params, "="),
    #     ">=": lambda params: compare(params, ">="),
    #     ">": lambda params: compare(params, ">"),
    # }
    if Operators.is_supported(operator):
        return Operators.call_method(operator, parameters)
    return ""


def execute_function(name, parameters):
    name = name.lower()
    if Functions.is_supported(name):
        return Functions.call_method(name, parameters)
    return ""


@dataclass
class Operators:
    @classmethod
    def is_supported(cls, operator):
        return operator in cls.supported_operators
    
    @classmethod
    def call_method(cls, operator, params):
        return getattr(cls(), cls.supported_operators[operator])(params)

    @classmethod
    @property
    def supported_operators(cls):
        return {
            "&": cls._and,
            "+": cls._plus,
            "-": cls._minus,
            "/": cls._divide,
            "*": cls._multiply,
            "^": cls._pow,
            "<": cls._lt,
            "<=": cls._lte,
            "=": cls._eq,
            ">=": cls._gte,
            ">": cls._gt,
        }

    def _and(self, params):
        return "".join(params)
    
    def _plus(self, params):
        return str(sum(map(float, params)))
    
    def _minus(self, params):
        return str(float(params[0]) - sum(map(float, params[1:])))
    
    def _divide(self, params):
        return str(
            float(params[0]) / (float(_element_at(params, 1)) if float(_element_at(params, 1)) != 0 else 1)
        )
    
    def _multiply(self, params):
        return str(math.prod(map(float, params)))
    
    def _pow(self, params):
        return to_number_string(float(params[0]) ** float(_element_at(params, 1)))
    
    def _lt(self, params):
        return compare(params, "<")
    
    def _lte(self, params):
        return compare(params, "<=")
    
    def _eq(self, params):
        return compare(params, "=")
    
    def _gte(self, params):
        return compare(params, ">=")
    
    def _gt(self, params):
        return compare(params, ">")
    

@dataclass
class Functions:

    @classmethod
    def is_supported(cls, name):
        return name.lower() in cls.__dict__

    @classmethod
    def call_method(cls, name, params):
        return getattr(cls(), name)(params)

    def uppercase(self, params):
        return "".join(param.upper() for param in params)

    def lowercase(self, params):
        return "".join(param.lower() for param in params)

    def concatenate(self, params):
        return "".join(params)

    def round(self, params):
        if params:
            out = format(float(params[0] or ""), f".{int(_element_at(params, 1) or 0)}f")
            if self.param_as_boolean_is_set(_element_at(params, 2)):
                return out
            return self.strip_last_zeroes_after_dot(out)
        return str(float("nan"))

    def ceil(self, params):
        if params:
            mult = 10 ** int(_element_at(params, 1) or 0)
            out = format(
                math.ceil(float(params[0]) * mult) / mult, f".{int(_element_at(params, 1) or 0)}f"
            )
            if self.param_as_boolean_is_set(_element_at(params, 2)):
                return out
            return self.strip_last_zeroes_after_dot(out)
        return str(float("nan"))

    def floor(self, params):
        if params:
            mult = 10 ** int(_element_at(params, 1) or 0)
            out = format(
                math.floor(float(params[0]) * mult) / mult, f".{int(_element_at(params, 1) or 0)}f"
            )
            if self.param_as_boolean_is_set(_element_at(params, 2)):
                return out
            return self.strip_last_zeroes_after_dot(out)
        return str(float("nan"))

    def add(self, params):
        result = 0
        for param in params:
            if param.replace(".", "", 1).isdigit():
                result += float(param)
            else:
                return str(float("nan"))
        return str(result)

    def multiply(self, params):
        result = 1
        for param in params:
            if param.replace(".", "", 1).isdigit():
                result *= float(param)
            else:
                return str(float("nan"))
        return str(result)

    def subtract(self, params):
        if params:
            first = float(params[0])
            rest = self.add(params[1:])
            if not math.isnan(first) and not math.isnan(rest):
                return str(first - float(rest))
        return str(float("nan"))

    def divide(self, params):
        if params:
            first = float(params[0])
            rest = self.multiply(params[1:])
            if not math.isnan(first) and not math.isnan(rest) and float(rest) != 0:
                return str(first / float(rest))
        return str(float("nan"))

    def pow(self, params):
        if params:
            return self.to_number_string(float(params[0]) ** float(_element_at(params, 1)))
        return str(float("nan"))

    def max(self, params):
        if params:
            params_float = [
                float(param) for param in params if param.replace(".", "", 1).isdigit()
            ]
            if params_float:
                return str(max(params_float))
        return str(float("nan"))

    def min(self, params):
        if params:
            params_float = [
                float(param) for param in params if param.replace(".", "", 1).isdigit()
            ]
            if params_float:
                return str(min(params_float))
        return str(float("nan"))

    def lt(self, params):
        return self.compare(params, "<")

    def lte(self, params):
        return self.compare(params, "<=")

    def eq(self, params):
        return self.compare(params, "=")

    def gte(self, params):
        return self.compare(params, ">=")

    def gt(self, params):
        return self.compare(params, ">")

    def param_as_boolean_is_set(self, param):
        param = (param or "").lower()
        return param and param != "0" and param != "false" and param != "no"

    def strip_last_zeroes_after_dot(self, param):
        if "." in param:
            return param.rstrip("0").rstrip(".")
        return param

    def compare(self, params, operator):
        if len(params) < 2:
            return "0"
        p0 = float(params[0]) if params[0].replace(".", "", 1).isdigit() else params[0]
        p1 = float(_element_at(params, 1)) if _element_at(params, 1, '').replace(".", "", 1).isdigit() else _element_at(params, 1)
        if "=" in operator and p0 == p1:
            return "1"
        if "<" in operator and p0 < p1:
            return "1"
        if ">" in operator and p0 > p1:
            return "1"
        return "0"
    

def function_is_supported(name):
    return name.lower() in Functions.__dict__
