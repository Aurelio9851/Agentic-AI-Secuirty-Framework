
class RAGTool:

    def __init__(self, rag):

        self.rag = rag

    def search_codebase(self, query):

        return self.rag.retrieve(query)

