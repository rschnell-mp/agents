"""Entry point for the custom agent interactive REPL.

Run with::

    python main.py

Type ``quit`` or ``exit`` to stop the REPL.
Tool calls follow the format::

    <tool_name> | {"arg1": "value1", ...}

For example::

    add | {"a": 10, "b": 32}
    upper | {"text": "hello world"}
"""

import sys

from agent import Agent
from agent.builtin_tools import BUILTIN_TOOLS


def main() -> None:
    agent = Agent(
        name="CustomAgent",
        system_prompt="You are a helpful assistant.",
        tools=BUILTIN_TOOLS,
    )

    print("=== Custom Agent REPL ===")
    print("Available tools:", ", ".join(t.name for t in agent.registry.all_tools()))
    print("Format: <tool_name> | {\"arg\": value}  — or just type text for a direct answer.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"quit", "exit", ""}:
            print("Goodbye!")
            break

        try:
            result = agent.run(user_input)
            print(f"Agent: {result}\n")
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}\n", file=sys.stderr)


if __name__ == "__main__":
    main()
