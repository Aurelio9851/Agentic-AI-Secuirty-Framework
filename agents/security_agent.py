from pathlib import Path
from .base_agent import BaseAgent
from tools.tool_registry import get_tool_specs


ROLE_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "security_agent_role.txt"


class SecurityAgent(BaseAgent):


    def __init__(self, memory, rag):


        super().__init__(

            name="SecurityAgent",

            role=ROLE_TEMPLATE_PATH.read_text(encoding="utf-8"),

            tools={
                name: spec["function"]
                for name, spec in get_tool_specs(["read_file", "security_scan"], rag_tool=rag).items()
            } | {"search_codebase": get_tool_specs(["search_codebase"], rag_tool=rag)["search_codebase"]["function"]},

            tool_descriptions={
                **{
                    name: {
                        "description": spec["description"],
                        "args": spec["args"]
                    }
                    for name, spec in get_tool_specs(["read_file", "security_scan"], rag_tool=rag).items()
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

                "application security analysis",

                "OWASP vulnerability research",

                "authentication analysis",

                "security configuration review"

            ],

            memory=memory

        )