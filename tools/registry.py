class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, tool):

        self.tools[tool.name] = tool

        print(f"Registered Tool -> {tool.name}")

    def execute(self, tool_name, arguments):

        tool = self.tools.get(tool_name)

        if tool is None:

            raise Exception(
                f"Tool '{tool_name}' not found."
            )

        return tool.execute(arguments)

    def list_tools(self):

        return list(self.tools.keys())