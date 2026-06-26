from tools.registry import ToolRegistry
from tools.memory_tool import MemoryTool
from core.executor import Executor

print("Loading Registry...")

# Create Registry
registry = ToolRegistry()

# Register Tools
registry.register(
    MemoryTool()
)

print("Available Tools:")
print(registry.list_tools())

# Create Executor
executor = Executor(
    registry
)

# Fake AI Plan
plan = {
    "steps": [
        {
            "tool": "memory",
            "arguments": {
                "name": "Sumith",
                "city": "Chennai"
            }
        }
    ]
}

print("\nExecuting Plan...\n")

results = executor.execute(
    plan
)

print("Execution Results:\n")

print(results)