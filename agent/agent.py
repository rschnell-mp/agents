"""Core Agent class for the custom agent framework."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .tools import Tool, ToolRegistry

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """A single message in the conversation history."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str
    tool_name: Optional[str] = None


@dataclass
class AgentStep:
    """Records one step of the agent execution loop."""

    thought: str
    action: Optional[str] = None  # tool name, or None for final answer
    action_input: Dict[str, Any] = field(default_factory=dict)
    observation: Optional[str] = None
    final_answer: Optional[str] = None


class AgentError(Exception):
    """Raised when the agent encounters an unrecoverable error."""


class Agent:
    """A tool-calling agent that follows a Thought → Action → Observation loop.

    The agent does **not** require an external LLM to function; instead it
    exposes a :py:meth:`step` method that callers (or sub-classes) can drive
    with any reasoning backend.  A built-in :py:meth:`run` method provides a
    simple synchronous loop suitable for testing and scripting.

    Parameters
    ----------
    name:
        Human-readable name for this agent.
    system_prompt:
        Instructions passed to the agent at the start of every conversation.
    tools:
        Optional list of :class:`~agent.tools.Tool` instances to register.
    max_iterations:
        Hard cap on how many tool-call rounds the loop may execute.

    Example::

        from agent import Agent, Tool, ToolRegistry

        def greet(name: str) -> str:
            return f"Hello, {name}!"

        agent = Agent(name="Greeter", system_prompt="You greet users.")
        agent.add_tool(Tool.from_function(greet, description="Greet a user by name"))
        result = agent.run("greet Alice")
        print(result)
    """

    def __init__(
        self,
        name: str = "CustomAgent",
        system_prompt: str = "You are a helpful assistant.",
        tools: Optional[List[Tool]] = None,
        max_iterations: int = 10,
    ) -> None:
        self.name = name
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.registry = ToolRegistry()
        self.history: List[Message] = []

        for tool in tools or []:
            self.add_tool(tool)

    # ------------------------------------------------------------------
    # Tool management
    # ------------------------------------------------------------------

    def add_tool(self, tool: Tool) -> None:
        """Register a tool with this agent."""
        self.registry.register(tool)
        logger.debug("Registered tool '%s'", tool.name)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear conversation history."""
        self.history.clear()

    def step(self, user_input: str) -> AgentStep:
        """Process *user_input* and return the next :class:`AgentStep`.

        This is the main extension point for sub-classes that want to plug in
        a real LLM.  The default implementation uses a simple rule-based
        dispatcher: it looks for a tool whose name appears in *user_input* and
        calls it with any JSON arguments found after a ``|`` separator.

        The format expected (when driving via :py:meth:`run`) is::

            <tool_name> | {"arg1": "value1", ...}

        If no tool name is found, the input itself becomes the final answer.
        """
        self.history.append(Message(role="user", content=user_input))

        parts = user_input.split("|", 1)
        candidate = parts[0].strip()

        tool = self.registry.get(candidate)
        if tool is None:
            # No matching tool – treat the whole input as the final answer.
            answer = user_input
            self.history.append(Message(role="assistant", content=answer))
            return AgentStep(thought="No tool matched; returning input as answer.", final_answer=answer)

        # Parse optional JSON arguments.
        action_input: Dict[str, Any] = {}
        if len(parts) == 2:
            raw_args = parts[1].strip()
            try:
                action_input = json.loads(raw_args)
            except json.JSONDecodeError as exc:
                raise AgentError(f"Invalid JSON arguments for tool '{candidate}': {exc}") from exc

        thought = f"Using tool '{tool.name}' with args {action_input}."
        logger.info(thought)

        try:
            observation = str(tool.run(**action_input))
        except Exception as exc:
            raise AgentError(f"Tool '{tool.name}' raised an error: {exc}") from exc

        self.history.append(
            Message(role="tool", content=observation, tool_name=tool.name)
        )
        return AgentStep(
            thought=thought,
            action=tool.name,
            action_input=action_input,
            observation=observation,
        )

    def run(self, user_input: str) -> str:
        """Run the agent loop on *user_input* and return the final answer.

        The loop continues until a step produces a ``final_answer`` or until
        ``max_iterations`` is reached.

        Parameters
        ----------
        user_input:
            The initial user message.

        Returns
        -------
        str
            The final answer produced by the agent.

        Raises
        ------
        AgentError
            If the maximum number of iterations is exceeded without a final
            answer, or if a tool raises an unexpected error.
        """
        current_input = user_input
        for iteration in range(self.max_iterations):
            agent_step = self.step(current_input)
            logger.debug("Iteration %d: %s", iteration, agent_step)

            if agent_step.final_answer is not None:
                return agent_step.final_answer

            # Use the observation as input to the next iteration so the caller
            # can chain tool calls when sub-classing and overriding step().
            assert agent_step.observation is not None
            current_input = agent_step.observation

        raise AgentError(
            f"Agent '{self.name}' exceeded max_iterations={self.max_iterations} "
            "without producing a final answer."
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def tool_schemas(self) -> List[Dict[str, Any]]:
        """Return JSON-schema descriptions of all registered tools."""
        return self.registry.schemas()

    def __repr__(self) -> str:
        return (
            f"Agent(name={self.name!r}, tools={list(self.registry._tools)}, "
            f"max_iterations={self.max_iterations})"
        )
