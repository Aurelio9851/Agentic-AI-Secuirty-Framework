from pathlib import Path
from .base_agent import BaseAgent
from tools.tool_registry import get_tool_specs


ROLE_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "search_agent_role.txt"


class SearchAgent(BaseAgent):

    def __init__(self, memory):

        super().__init__(

            name="SearchAgent",

            role=ROLE_TEMPLATE_PATH.read_text(encoding="utf-8"),

            tools={
                name: spec["function"]
                for name, spec in get_tool_specs(["list_files", "grep_file"]).items()
            },

            tool_descriptions={
                name: {
                    "description": spec["description"],
                    "args": spec["args"]
                }
                for name, spec in get_tool_specs(["list_files", "grep_file"]).items()
            },

            capabilities=[
                "repository structure exploration",
                "file search",
                "keyword search in code",
                "software component identification"
            ],

            memory=memory
        )

    
    def update_memory(self, action, result):

        if action == "list_files":

            self.memory.set(
                "files_found",
                result
            )


        elif action == "grep_file":

            self.memory.set(
                "search_results",
                result
            )