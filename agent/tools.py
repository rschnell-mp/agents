"""Tool definitions for the custom agent framework."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolParameter:
    """Describes a single parameter of a tool."""

    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class Tool:
    """Represents a callable tool that an agent can use.

    Example::

        def add(a: int, b: int) -> int:
            return a + b

        tool = Tool(
            name="add",
            description="Add two integers",
            func=add,
            parameters=[
                ToolParameter("a", "int", "First operand"),
                ToolParameter("b", "int", "Second operand"),
            ],
        )
    """

    name: str
    description: str
    func: Callable[..., Any]
    parameters: List[ToolParameter] = field(default_factory=list)

    def run(self, **kwargs: Any) -> Any:
        """Execute the tool with the given keyword arguments."""
        return self.func(**kwargs)

    def schema(self) -> Dict[str, Any]:
        """Return a JSON-schema-style description of this tool."""
        props: Dict[str, Any] = {}
        required: List[str] = []
        for param in self.parameters:
            props[param.name] = {"type": param.type, "description": param.description}
            if param.required:
                required.append(param.name)
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {"type": "object", "properties": props, "required": required},
        }

    @classmethod
    def from_function(cls, func: Callable[..., Any], description: str = "") -> "Tool":
        """Create a Tool by inspecting a Python function's signature."""
        sig = inspect.signature(func)
        params: List[ToolParameter] = []
        for pname, p in sig.parameters.items():
            annotation = p.annotation
            if annotation is inspect.Parameter.empty:
                type_name = "string"
            else:
                type_name = getattr(annotation, "__name__", str(annotation))
            has_default = p.default is not inspect.Parameter.empty
            params.append(
                ToolParameter(
                    name=pname,
                    type=type_name,
                    description=pname,
                    required=not has_default,
                )
            )
        return cls(
            name=func.__name__,
            description=description or (func.__doc__ or func.__name__),
            func=func,
            parameters=params,
        )


class ToolRegistry:
    """Registry that stores and looks up tools by name."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Add a tool to the registry."""
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Return the tool with the given name, or *None* if not found."""
        return self._tools.get(name)

    def all_tools(self) -> List[Tool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def schemas(self) -> List[Dict[str, Any]]:
        """Return the JSON-schema-style descriptions of all tools."""
        return [t.schema() for t in self._tools.values()]

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return name in self._tools
