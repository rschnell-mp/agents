"""Built-in example tools shipped with the custom agent framework."""

from __future__ import annotations

import operator
from typing import Union

from .tools import Tool, ToolParameter

Number = Union[int, float]


def _add(a: float, b: float) -> float:
    return operator.add(a, b)


def _subtract(a: float, b: float) -> float:
    return operator.sub(a, b)


def _multiply(a: float, b: float) -> float:
    return operator.mul(a, b)


def _divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return operator.truediv(a, b)


def _echo(text: str) -> str:
    return text


def _upper(text: str) -> str:
    return text.upper()


def _lower(text: str) -> str:
    return text.lower()


def _length(text: str) -> int:
    return len(text)


_NUMBER_PARAMS = [
    ToolParameter("a", "number", "First operand"),
    ToolParameter("b", "number", "Second operand"),
]

add_tool = Tool(
    name="add",
    description="Add two numbers together.",
    func=_add,
    parameters=_NUMBER_PARAMS,
)

subtract_tool = Tool(
    name="subtract",
    description="Subtract b from a.",
    func=_subtract,
    parameters=_NUMBER_PARAMS,
)

multiply_tool = Tool(
    name="multiply",
    description="Multiply two numbers.",
    func=_multiply,
    parameters=_NUMBER_PARAMS,
)

divide_tool = Tool(
    name="divide",
    description="Divide a by b.",
    func=_divide,
    parameters=_NUMBER_PARAMS,
)

echo_tool = Tool(
    name="echo",
    description="Return the input text unchanged.",
    func=_echo,
    parameters=[ToolParameter("text", "string", "Text to echo")],
)

upper_tool = Tool(
    name="upper",
    description="Convert text to uppercase.",
    func=_upper,
    parameters=[ToolParameter("text", "string", "Text to convert")],
)

lower_tool = Tool(
    name="lower",
    description="Convert text to lowercase.",
    func=_lower,
    parameters=[ToolParameter("text", "string", "Text to convert")],
)

length_tool = Tool(
    name="length",
    description="Return the character count of a string.",
    func=_length,
    parameters=[ToolParameter("text", "string", "Text to measure")],
)

#: All built-in tools, ready to pass to :class:`~agent.Agent`.
BUILTIN_TOOLS = [
    add_tool,
    subtract_tool,
    multiply_tool,
    divide_tool,
    echo_tool,
    upper_tool,
    lower_tool,
    length_tool,
]
