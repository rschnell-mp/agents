# agents

A lightweight, extensible **custom agent framework** written in Python.

The framework follows a **Thought → Action → Observation** loop (inspired by
ReAct) and lets you attach any Python callable as a *tool*.

---

## Features

- `Agent` class with a configurable reasoning loop
- `Tool` / `ToolRegistry` system — wrap any Python function as a tool
- `Tool.from_function()` — auto-generates parameter metadata from type hints
- Eight **built-in tools** ready to use: `add`, `subtract`, `multiply`,
  `divide`, `echo`, `upper`, `lower`, `length`
- Clean separation between the agent loop and the reasoning backend — drop in
  any LLM by overriding `Agent.step()`

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Quick start

```python
from agent import Agent, Tool
from agent.builtin_tools import BUILTIN_TOOLS

agent = Agent(
    name="MathAgent",
    system_prompt="You are a helpful math assistant.",
    tools=BUILTIN_TOOLS,
)

# Tool calls use the format: <tool_name> | {"arg": value}
result = agent.run('add | {"a": 3, "b": 4}')
print(result)  # "7.0"
```

### Add a custom tool

```python
from agent import Agent, Tool

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32

tool = Tool.from_function(celsius_to_fahrenheit)

agent = Agent(name="WeatherAgent", tools=[tool])
result = agent.run('celsius_to_fahrenheit | {"celsius": 100}')
print(result)  # "212.0"
```

---

## Interactive REPL

```bash
python main.py
```

---

## Example script

```bash
python examples/simple_agent.py
```

---

## Running the tests

```bash
pytest
```

---

## Project layout

```
agents/
├── agent/
│   ├── __init__.py        # Public API
│   ├── agent.py           # Agent class + AgentStep
│   ├── builtin_tools.py   # Ready-to-use built-in tools
│   └── tools.py           # Tool, ToolParameter, ToolRegistry
├── examples/
│   └── simple_agent.py    # Runnable example
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
├── main.py                # Interactive REPL
└── requirements.txt
```
