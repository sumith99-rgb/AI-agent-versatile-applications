from dataclasses import dataclass, field


@dataclass
class ToolCall:

    tool: str

    arguments: dict


@dataclass
class ExecutionPlan:

    thought: str = ""

    steps: list[ToolCall] = field(default_factory=list)