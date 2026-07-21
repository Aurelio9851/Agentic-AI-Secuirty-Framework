from memory.shared_memory import SharedMemory

from agents.search_agent import SearchAgent
from agents.code_agent import CodeAgent
from agents.security_agent import SecurityAgent
from agents.reporter_agent import ReporterAgent

from agents.planner import PlannerAgent
from agents.supervisor_agent import SupervisorAgent
from rag.rag import CodebaseRAG
from tools.rag_tool import RAGTool
import os


def main():

    PATH_PROJECT_TO_ANALYZE= "./"
    memory = SharedMemory()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY before running this script")

    rag = CodebaseRAG(api_key)
    rag.index_repository(PATH_PROJECT_TO_ANALYZE)

    rag_tool = RAGTool(rag)


    search = SearchAgent(memory)

    code = CodeAgent(memory, rag_tool)

    security = SecurityAgent(memory, rag_tool)

    reporter = ReporterAgent(memory)



    agents = {

        "SearchAgent": search,

        "CodeAgent": code,

        "SecurityAgent": security,

        "ReporterAgent": reporter

    }



    planner = PlannerAgent(
        agents
    )


    supervisor = SupervisorAgent(

        agents,

        planner,

        memory
    )



    result = supervisor.run(

        """
        Analyze the security of the application in {PATH_PROJECT_TO_ANALYZE} and provide a report with recommendations for improvement.
        """

    )


    print("\n===== RISULTATO =====")

    print(result)



if __name__=="__main__":

    main()