from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        return self.model.encode(chunks, show_progress_bar=True)

    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query])[0]

