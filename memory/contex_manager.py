class ContextManager:


    def __init__(self, memory):

        self.memory = memory



    def get_context(self, agent_name):

        data = self.memory.all()


        if agent_name == "SearchAgent":

            return {
                "task_history":
                data.get("observations", [])
            }


        elif agent_name == "CodeAgent":

            return {
                "files_found":
                data.get("files_found", [])
            }


        elif agent_name == "SecurityAgent":

            return {
                "files_found":
                data.get("files_found", []),

                "code_analysis":
                data.get("code_analysis", [])
            }


        elif agent_name == "ReporterAgent":

            return data


        return {}