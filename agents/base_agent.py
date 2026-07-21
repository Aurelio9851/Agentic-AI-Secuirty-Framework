from google import genai
import os
import json
from pathlib import Path


PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "base_agent_prompt.txt"


def get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    return api_key


class BaseAgent:

    def __init__(
        self,
        name,
        role,
        tools,
        tool_descriptions,
        memory,
        capabilities
        #context_manager
    ):

        self.name = name
        self.role = role
        self.tools = tools
        self.tool_descriptions = tool_descriptions
        self.memory = memory
        #self.context_manager = context_manager
        self.capabilities = capabilities



        self.client = genai.Client(
            api_key=get_api_key()
        )


    def execute_tool(self, tool_name, args):

        if tool_name not in self.tools:
            return "Tool not available"


        try:

            return self.tools[tool_name](**args)

        except Exception as e:

            return f"Tool error: {str(e)}"
    
    def update_memory(self, action, result):

        pass

    

    def run(self, task, max_steps=10):

        step = 0

        while step < max_steps:

            step += 1
            
            #memory_state = self.context_manager.get_context(self.name)

            memory_state = self.memory.all()

            prompt_template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
            prompt = prompt_template.format(
                self_name=self.name,
                role=self.role,
                task=task,
                tool_descriptions=json.dumps(self.tool_descriptions, indent=2),
                memory_state=memory_state,
            )


            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )


            data = json.loads(response.text)


            print("\n🧠", data["reason"])


            if data["action"] == "final":

                return data["args"].get(
                    "answer",
                    data["args"].get(
                        "result",
                        "No response provided"
                    )
                )


            result = self.execute_tool(
                data["action"],
                data["args"]
            )


            print(
                "🔧 TOOL:",
                data["action"]
            )


            print(
                "📤 RESULT:",
                result
            )

            self.memory.append(
                "observations",
                {
                    "agent": self.name,
                    "tool": data["action"],
                    "result": result
                }
            )

            self.update_memory(
                data["action"],
                result
            )
        return "Step limit reached without a final response."