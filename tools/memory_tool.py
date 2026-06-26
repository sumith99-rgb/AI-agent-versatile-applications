from tools.base_tool import BaseTool
from ai.memory import MemoryManager


class MemoryTool(BaseTool):

    @property
    def name(self):
        return "memory"

    def execute(self, arguments):

        memory = MemoryManager()

        for key, value in arguments.items():

            memory.set_user(
                key,
                value
            )

        return {
            "status": "success",
            "saved": arguments
        }