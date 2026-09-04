from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.schemas.rag import RAGChunk


class EmbeddingService:
    _vectorizer: TfidfVectorizer = None
    _chunk_matrix = None
    _indexed_chunks: List[RAGChunk] = []

    @classmethod
    def index_chunks(cls, chunks: List[RAGChunk]):
        """Fits TF-IDF vectorizer over the statutory chunk corpus."""
        cls._indexed_chunks = chunks
        corpus = [c.text for c in chunks]
        cls._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=2500,
        )
        cls._chunk_matrix = cls._vectorizer.fit_transform(corpus)

    @classmethod
    def compute_similarity(cls, query: str, top_k: int = 5) -> List[Tuple[RAGChunk, float]]:
        """Computes dense cosine similarity between query and indexed chunks."""
        if cls._vectorizer is None or cls._chunk_matrix is None:
            return []

        query_vec = cls._vectorizer.transform([query])
        sims = cosine_similarity(query_vec, cls._chunk_matrix)[0]

        top_indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(sims[idx])
            if score > 0.05:  # Relevance cutoff
                results.append((cls._indexed_chunks[idx], round(score, 4)))

        return results
