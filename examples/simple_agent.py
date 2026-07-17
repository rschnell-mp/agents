"""Simple example showing how to use the custom agent framework.

Run with::

    python examples/simple_agent.py
"""

from agent import Agent, Tool, ToolParameter
from agent.builtin_tools import BUILTIN_TOOLS


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def main() -> None:
    # 1. Create a custom tool using Tool.from_function
    temp_tool = Tool.from_function(
        celsius_to_fahrenheit,
        description="Convert a temperature from Celsius to Fahrenheit.",
    )

    # 2. Build an agent with built-in tools plus our custom tool
    agent = Agent(
        name="MathAndUtilityAgent",
        system_prompt=(
            "You are a helpful assistant with access to arithmetic "
            "and text-manipulation tools."
        ),
        tools=BUILTIN_TOOLS + [temp_tool],
        max_iterations=5,
    )

    print(f"Agent: {agent}\n")
    print("Available tools:")
    for schema in agent.tool_schemas():
        print(f"  - {schema['name']}: {schema['description']}")

    print("\n--- Running examples ---\n")

    examples = [
        'add | {"a": 3, "b": 4}',
        'multiply | {"a": 6, "b": 7}',
        'upper | {"text": "hello, world"}',
        'length | {"text": "custom agent"}',
        'celsius_to_fahrenheit | {"celsius": 100}',
        "echo | {\"text\": \"I am a custom agent!\"}",
    ]

    for prompt in examples:
        result = agent.run(prompt)
        print(f"  Input : {prompt}")
        print(f"  Output: {result}\n")


if __name__ == "__main__":
    main()
