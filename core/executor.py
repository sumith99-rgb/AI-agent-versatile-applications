from tools.registry import ToolRegistry


class Executor:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, plan):

        results = []

        steps = plan.get("steps", [])

        for step in steps:

            tool = step.get("tool")

            arguments = step.get("arguments", {})

            result = self.registry.execute(
                tool,
                arguments
            )

            results.append({
                "tool": tool,
                "result": result
            })

        return results