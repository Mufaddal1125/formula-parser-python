from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional, Union


@dataclass
class Token:
    type: str
    value: str


@dataclass
class TokenNode(Token):
    innerNodes: List["TokenNode"]


class TokenType(Enum):
    Number = ("Number",)
    String = ("String",)
    Whitespace = ("Whitespace",)
    Operator = ("Operator",)
    BracketStart = ("BracketStart",)
    BracketEnd = ("BracketEnd",)
    ReferenceBracketStart = ("ReferenceBracketStart",)
    ReferenceBracketEnd = ("ReferenceBracketEnd",)
    ReferenceName = ("ReferenceName",)
    FunctionName = ("FunctionName",)
    Comma = ("Comma",)
    QuoteStart = ("QuoteStart",)
    QuoteEnd = ("QuoteEnd",)
    EmptyStringAndQuoteEnd = ("EmptyStringAndQuoteEnd",)
    DoubleQuoteStart = ("DoubleQuoteStart",)
    DoubleQuoteEnd = ("DoubleQuoteEnd",)
    EmptyStringAndDoubleQuoteEnd = ("EmptyStringAndDoubleQuoteEnd",)
    Group = ("Group",)
    Error = "Error"


operator_allowed_after = [
    TokenType.Number,
    TokenType.BracketEnd,
    TokenType.ReferenceBracketEnd,
    TokenType.QuoteEnd,
    TokenType.DoubleQuoteEnd,
]


class ErrorType(Enum):
    UnexpectedOperator = ("UnexpectedOperator",)
    ValueRequiredAfterOperator = ("ValueRequiredAfterOperator",)
    OperatorRequiredBeforeNumber = ("OperatorRequiredBeforeNumber",)
    OperatorRequiredBeforeFunction = ("OperatorRequiredBeforeFunction",)
    OperatorRequiredBeforeQuote = ("OperatorRequiredBeforeQuote",)
    OperatorRequiredBeforeBracket = ("OperatorRequiredBeforeBracket",)
    OperatorRequiredBeforeReference = ("OperatorRequiredBeforeReference",)
    InvalidFunction = ("InvalidFunction",)
    InvalidCharacter = ("InvalidCharacter",)
    UnexpectedComma = ("UnexpectedComma",)
    UnexpectedBracket = ("UnexpectedBracket",)
    UnexpectedReferenceBracket = ("UnexpectedReferenceBracket",)
    ReferenceNameRequiredInBrackets = ("ReferenceNameRequiredInBrackets",)
    UnsupportedReferenceName = ("UnsupportedReferenceName",)
    UnclosedQuote = ("UnclosedQuote",)
    UnclosedDoubleQuote = ("UnclosedDoubleQuote",)
    UnclosedBracket = ("UnclosedBracket",)
    UnclosedReferenceBracket = ("UnclosedReferenceBracket",)
    CircularReference = ("CircularReference",)
    CircularReferenceToItself = ("CircularReferenceToItself",)
    DependsOnInvalid = ("DependsOnInvalid",)
    DependsOnCircular = "DependsOnCircular"


@dataclass
class ValidationError:
    token: Optional[Token]
    tokenIndex: Optional[int]
    errorType: ErrorType
    message: Optional[str]


@dataclass
class ExtendedFormulaEntry:
    referenceName: str
    referenceNameOrig: str
    formula: str
    tokens: List[Token]
    tokenNodes: List[TokenNode]
    validationErrors: List[ValidationError]
    order: float
    dependencies: List[str]

@dataclass
class LexerStream:
    match: Callable[[str, bool], Optional[str]]
    skip: Callable[[], None]
    prev: Optional[TokenType]