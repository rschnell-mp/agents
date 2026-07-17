"""Tests for the Tool and ToolRegistry classes."""

import pytest

from agent import Tool, ToolParameter, ToolRegistry


# ---------------------------------------------------------------------------
# Tool
# ---------------------------------------------------------------------------


def test_tool_run_executes_function():
    tool = Tool(
        name="greet",
        description="Greet someone",
        func=lambda name: f"Hello, {name}!",
        parameters=[ToolParameter("name", "string", "Name to greet")],
    )
    assert tool.run(name="World") == "Hello, World!"


def test_tool_schema_structure():
    tool = Tool(
        name="add",
        description="Add two numbers",
        func=lambda a, b: a + b,
        parameters=[
            ToolParameter("a", "number", "First operand"),
            ToolParameter("b", "number", "Second operand"),
        ],
    )
    schema = tool.schema()
    assert schema["name"] == "add"
    assert schema["description"] == "Add two numbers"
    assert "a" in schema["parameters"]["properties"]
    assert "b" in schema["parameters"]["properties"]
    assert "a" in schema["parameters"]["required"]
    assert "b" in schema["parameters"]["required"]


def test_tool_schema_optional_parameter():
    tool = Tool(
        name="greet",
        description="Greet someone",
        func=lambda name="World": f"Hello, {name}!",
        parameters=[ToolParameter("name", "string", "Name", required=False)],
    )
    schema = tool.schema()
    assert "name" not in schema["parameters"]["required"]


def test_tool_from_function_creates_parameters():
    def multiply(a: int, b: int) -> int:
        """Multiply two integers."""
        return a * b

    tool = Tool.from_function(multiply)
    assert tool.name == "multiply"
    assert len(tool.parameters) == 2
    assert tool.parameters[0].name == "a"
    assert tool.parameters[1].name == "b"


def test_tool_from_function_uses_docstring():
    def noop():
        """Does nothing."""

    tool = Tool.from_function(noop)
    assert "Does nothing" in tool.description


def test_tool_from_function_custom_description():
    def noop():
        pass

    tool = Tool.from_function(noop, description="Custom description")
    assert tool.description == "Custom description"


def test_tool_from_function_no_annotation_defaults_to_string():
    def func(x):
        return x

    tool = Tool.from_function(func)
    assert tool.parameters[0].type == "string"


# ---------------------------------------------------------------------------
# ToolRegistry
# ---------------------------------------------------------------------------


def test_registry_register_and_get():
    registry = ToolRegistry()
    tool = Tool(name="ping", description="Ping", func=lambda: "pong")
    registry.register(tool)
    assert registry.get("ping") is tool


def test_registry_get_missing_returns_none():
    registry = ToolRegistry()
    assert registry.get("nonexistent") is None


def test_registry_all_tools():
    registry = ToolRegistry()
    t1 = Tool(name="a", description="", func=lambda: None)
    t2 = Tool(name="b", description="", func=lambda: None)
    registry.register(t1)
    registry.register(t2)
    tools = registry.all_tools()
    assert len(tools) == 2
    assert t1 in tools
    assert t2 in tools


def test_registry_len():
    registry = ToolRegistry()
    assert len(registry) == 0
    registry.register(Tool(name="x", description="", func=lambda: None))
    assert len(registry) == 1


def test_registry_contains():
    registry = ToolRegistry()
    registry.register(Tool(name="foo", description="", func=lambda: None))
    assert "foo" in registry
    assert "bar" not in registry


def test_registry_schemas():
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="add",
            description="Add",
            func=lambda a, b: a + b,
            parameters=[
                ToolParameter("a", "int", "a"),
                ToolParameter("b", "int", "b"),
            ],
        )
    )
    schemas = registry.schemas()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "add"


def test_registry_register_overwrites_existing():
    registry = ToolRegistry()
    t1 = Tool(name="ping", description="v1", func=lambda: "v1")
    t2 = Tool(name="ping", description="v2", func=lambda: "v2")
    registry.register(t1)
    registry.register(t2)
    assert registry.get("ping") is t2
