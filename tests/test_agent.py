"""Tests for the core Agent class."""

import pytest

from agent import Agent, AgentError, AgentStep, Tool, ToolParameter
from agent.builtin_tools import (
    BUILTIN_TOOLS,
    add_tool,
    divide_tool,
    echo_tool,
    length_tool,
    lower_tool,
    multiply_tool,
    subtract_tool,
    upper_tool,
)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_agent_default_name():
    agent = Agent()
    assert agent.name == "CustomAgent"


def test_agent_custom_name():
    agent = Agent(name="Marvin")
    assert agent.name == "Marvin"


def test_agent_registers_tools_at_construction():
    agent = Agent(tools=[echo_tool, add_tool])
    assert "echo" in agent.registry
    assert "add" in agent.registry


def test_agent_repr_contains_name():
    agent = Agent(name="Tester", tools=[echo_tool])
    assert "Tester" in repr(agent)


# ---------------------------------------------------------------------------
# add_tool
# ---------------------------------------------------------------------------


def test_add_tool_makes_tool_available():
    agent = Agent()
    agent.add_tool(echo_tool)
    assert "echo" in agent.registry


def test_tool_schemas_returns_all_schemas():
    agent = Agent(tools=[add_tool, echo_tool])
    schemas = agent.tool_schemas()
    names = {s["name"] for s in schemas}
    assert {"add", "echo"} == names


# ---------------------------------------------------------------------------
# step – no tool match (final answer)
# ---------------------------------------------------------------------------


def test_step_no_tool_returns_input_as_final_answer():
    agent = Agent()
    step = agent.step("hello there")
    assert step.final_answer == "hello there"
    assert step.action is None


def test_step_records_history():
    agent = Agent()
    agent.step("some text")
    roles = [m.role for m in agent.history]
    assert "user" in roles
    assert "assistant" in roles


# ---------------------------------------------------------------------------
# step – tool execution
# ---------------------------------------------------------------------------


def test_step_executes_matching_tool():
    agent = Agent(tools=[add_tool])
    step = agent.step('add | {"a": 3.0, "b": 4.0}')
    assert step.action == "add"
    assert step.observation == "7.0"


def test_step_records_tool_observation_in_history():
    agent = Agent(tools=[echo_tool])
    agent.step('echo | {"text": "hi"}')
    tool_messages = [m for m in agent.history if m.role == "tool"]
    assert len(tool_messages) == 1
    assert tool_messages[0].content == "hi"
    assert tool_messages[0].tool_name == "echo"


def test_step_invalid_json_raises_agent_error():
    agent = Agent(tools=[add_tool])
    with pytest.raises(AgentError, match="Invalid JSON"):
        agent.step("add | not-valid-json")


def test_step_tool_error_raises_agent_error():
    broken_tool = Tool(
        name="broken",
        description="Always fails",
        func=lambda: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    agent = Agent(tools=[broken_tool])
    with pytest.raises(AgentError, match="boom"):
        agent.step("broken")


# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------


def test_run_returns_final_answer_for_plain_text():
    agent = Agent()
    result = agent.run("just text")
    assert result == "just text"


def test_run_with_tool_call():
    agent = Agent(tools=[multiply_tool])
    result = agent.run('multiply | {"a": 6.0, "b": 7.0}')
    assert result == "42.0"


def test_run_raises_when_max_iterations_exceeded():
    """An agent that always produces an observation (never a final answer) must
    eventually raise AgentError."""
    loop_tool = Tool(
        name="loop",
        description="Returns another loop call",
        func=lambda: 'loop | {}',
    )
    agent = Agent(tools=[loop_tool], max_iterations=3)
    with pytest.raises(AgentError, match="max_iterations"):
        agent.run("loop")


# ---------------------------------------------------------------------------
# reset
# ---------------------------------------------------------------------------


def test_reset_clears_history():
    agent = Agent()
    agent.run("hello")
    assert len(agent.history) > 0
    agent.reset()
    assert len(agent.history) == 0


# ---------------------------------------------------------------------------
# Built-in tools
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tool,kwargs,expected",
    [
        (add_tool, {"a": 1.0, "b": 2.0}, "3.0"),
        (subtract_tool, {"a": 10.0, "b": 3.0}, "7.0"),
        (multiply_tool, {"a": 4.0, "b": 5.0}, "20.0"),
        (divide_tool, {"a": 9.0, "b": 3.0}, "3.0"),
        (echo_tool, {"text": "hello"}, "hello"),
        (upper_tool, {"text": "hello"}, "HELLO"),
        (lower_tool, {"text": "WORLD"}, "world"),
        (length_tool, {"text": "abc"}, "3"),
    ],
)
def test_builtin_tool(tool, kwargs, expected):
    agent = Agent(tools=[tool])
    result = agent.run(f"{tool.name} | {__import__('json').dumps(kwargs)}")
    assert result == expected


def test_divide_by_zero_raises_agent_error():
    agent = Agent(tools=[divide_tool])
    with pytest.raises(AgentError, match="divide by zero"):
        agent.run('divide | {"a": 1, "b": 0}')


def test_all_builtin_tools_registered():
    agent = Agent(tools=BUILTIN_TOOLS)
    assert len(agent.registry) == len(BUILTIN_TOOLS)
