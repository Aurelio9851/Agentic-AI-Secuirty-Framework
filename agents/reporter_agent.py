from pathlib import Path
from .base_agent import BaseAgent


ROLE_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "reporter_agent_role.txt"


class ReporterAgent(BaseAgent):


    def __init__(self, memory):

        super().__init__(


            name="ReporterAgent",


            role=ROLE_TEMPLATE_PATH.read_text(encoding="utf-8"),


            tools={},


            tool_descriptions={},

            memory=memory,

            capabilities=[

                "technical report generation",

                "summary of agent results",

                "findings organization"

            ]

        )