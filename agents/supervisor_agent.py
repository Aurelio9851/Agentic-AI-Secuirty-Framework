from google import genai
import json
import os
from pathlib import Path


PROMPT_TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "prompts" / "supervisor_prompt.txt"


def get_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    return api_key


class SupervisorAgent:


    def __init__(
        self,
        agents,
        planner,
        memory
    ):

        self.agents = agents
        self.planner = planner
        self.memory = memory


        self.client = genai.Client(
            api_key=get_api_key()
        )



    def evaluate_result(
        self,
        task,
        plan,
        decisions,
        result
    ):


        prompt_template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
        prompt = prompt_template.format(
            task=task,
            decisions=json.dumps(decisions, indent=2),
            plan=json.dumps(plan, indent=2),
            result=result,
        )


        response = self.client.models.generate_content(

            model="gemini-3.1-flash-lite",

            contents=prompt,

            config={
                "response_mime_type":"application/json"
            }

        )


        return json.loads(
            response.text
        )



    def run(
        self,
        task,
        max_iterations=5
    ):


        iteration = 0

        results = []
        decisions = []


        while iteration < max_iterations:


            iteration += 1


            print(
                f"\n🔄 ITERATION {iteration}"
            )



            print(
                "\n📝 CREATING PLAN"
            )


            plan = self.planner.create_plan(

                task,

                self.memory

            )



            print(
                json.dumps(
                    plan,
                    indent=2
                )
            )



            replan = False



            print(
                "\n🚀 EXECUTING PLAN"
            )



            for step in plan:


                agent_name = step["agent"]

                agent_task = step["task"]



                if agent_name == "final":

                    return results



                print(
                    f"\n▶ {agent_name}"
                )



                if agent_name not in self.agents:

                    print(
                        "Agent not found"
                    )

                    continue



                agent = self.agents[agent_name]



                result = agent.run(
                    agent_task
                )


                print(
                    "\n📤 RESULT:"
                )

                print(result)



                results.append(

                    {
                        "agent":agent_name,
                        "result":result
                    }

                )


                # save to memory

                self.memory.append(

                    "agent_results",

                    {
                        "agent":agent_name,
                        "result":result
                    }

                )



                # evaluation

                decision = self.evaluate_result(

                    task,

                    plan,

                    decisions,

                    result

                )

                decisions.append({
                    "plan": plan,
                    "result": result,
                    "decision": decision
                })


                print(
                    "\n🧐 DECISION:"
                )

                print(decision)



                if decision["replan"]:


                    print(
                        "\n♻️ REPLANNING REQUIRED"
                    )


                    replan = True

                    break



            if not replan:

                print(
                    "\n✅ Plan completed"
                )

                return results



        return {
            "error":
            "Maximum number of replanning iterations reached",
            "results":results
        }