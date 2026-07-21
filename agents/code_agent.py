from pathlib import Path
from .base_agent import BaseAgent
from tools.tool_registry import get_tool_specs


ROLE_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "code_agent_role.txt"


class CodeAgent(BaseAgent):

    def __init__(self, memory, rag):

        super().__init__(

            name="CodeAgent",

            role=ROLE_TEMPLATE_PATH.read_text(encoding="utf-8"),

            tools={
                name: spec["function"]
                for name, spec in get_tool_specs(["read_file", "list_directory"], rag_tool=rag).items()
            } | {"search_codebase": get_tool_specs(["search_codebase"], rag_tool=rag)["search_codebase"]["function"]},

            tool_descriptions={
                **{
                    name: {
                        "description": spec["description"],
                        "args": spec["args"]
                    }
                    for name, spec in get_tool_specs(["read_file", "list_directory"], rag_tool=rag).items()
                },
                **{
                    name: {
                        "description": spec["description"],
                        "args": spec["args"]
                    }
                    for name, spec in get_tool_specs(["search_codebase"], rag_tool=rag).items()
                }
            },

            capabilities=[

                    "source code analysis",

                    "software architecture understanding",

                    "application flow identification",

                    "implementation explanation"

            ],

            memory=memory

        )