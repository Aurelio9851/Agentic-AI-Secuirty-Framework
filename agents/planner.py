from google import genai
import json
import os
from pathlib import Path


PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "planner_prompt.txt"


def get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    return api_key


class PlannerAgent:


    def __init__(
        self,
        agents
    ):

        self.agents = agents

        self.client = genai.Client(
            api_key=get_api_key()
        )


    def build_agent_catalog(self):

        catalog = {}

        for name, agent in self.agents.items():

            catalog[name] = {

                "role": agent.role,

                "capabilities": agent.capabilities

            }

        return catalog



    def create_plan(
        self,
        task,
        memory
    ):


        context = memory.all()
        agent_catalog = self.build_agent_catalog()

        prompt_template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
        prompt = prompt_template.format(
            task=task,
            memory_context=json.dumps(context, indent=2),
            agent_catalog=json.dumps(agent_catalog, indent=2),
        )

        response = self.client.models.generate_content(

            model="gemini-3.1-flash-lite",

            contents=prompt,

            config={
                "response_mime_type":"application/json"
            }

        )


        try:

            plan = json.loads(
                response.text
            )


            return plan


        except Exception as e:

            print(
                "Planner parsing error:",
                e
            )


            return [
                {
                    "agent":"final",
                    "task":"Error generating the plan"
                }
            ]