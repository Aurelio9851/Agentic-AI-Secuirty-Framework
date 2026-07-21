import chromadb


class VectorStore:


    def __init__(self):

        self.client = chromadb.Client()


        self.collection = (
            self.client
            .get_or_create_collection(
                "codebase"
            )
        )


    def add_document(
        self,
        id,
        text,
        embedding
    ):


        self.collection.add(

            ids=[id],

            documents=[text],

            embeddings=[embedding]

        )



    def search(
        self,
        embedding,
        k=3
    ):


        result = self.collection.query(

            query_embeddings=[
                embedding
            ],

            n_results=k

        )


        return result["documents"][0]