from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="hr_documents",
            embedding_function=self.embedding_function
        )

    def add_documents(self, docs):
        for doc in docs:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[{"source": doc["source"], "title": doc["title"]}],
                ids=[doc["chunk_id"]]
            )

    def similarity_search(self, query, k=3):
        return self.collection.query(query_texts=[query], n_results=k)
