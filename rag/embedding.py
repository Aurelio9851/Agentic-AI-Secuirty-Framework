from google import genai


class GeminiEmbedding:


    def __init__(self, api_key):

        self.client = genai.Client(
            api_key=api_key
        )


    def encode(self, text):

        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text
        )

        return response.embeddings[0].values