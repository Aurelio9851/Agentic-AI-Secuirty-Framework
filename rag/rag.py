from .embedding import GeminiEmbedding
from .vector_store import VectorStore
import os



class CodebaseRAG:


    def __init__(self, api_key):

        self.embedder = GeminiEmbedding(
            api_key
        )

        self.store = VectorStore()



    def index_repository(self, path):


        counter = 0


        for root, dirs, files in os.walk(path):


            for file in files:


                if file.endswith(
                    (
                        ".py",
                        ".java",
                        ".js",
                        ".ts"
                    )
                ):


                    filepath = os.path.join(
                        root,
                        file
                    )


                    with open(
                        filepath,
                        "r",
                        errors="ignore"
                    ) as f:

                        content = f.read()



                    embedding = (
                        self.embedder
                        .encode(content)
                    )


                    self.store.add_document(

                        str(counter),

                        content,

                        embedding

                    )


                    counter += 1



        print(
            f"Indexed {counter} documents"
        )



    def retrieve(self, query):


        embedding = (
            self.embedder
            .encode(query)
        )


        return self.store.search(
            embedding
        )