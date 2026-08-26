from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.retrieval.kb_loader import load_kb_chunks


class KBRetriever:
    def __init__(self, kb_dir: str = "knowledge-base"):
        self.chunks = load_kb_chunks(kb_dir)

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.matrix = self.vectorizer.fit_transform(
            chunk["text"] for chunk in self.chunks
        )

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Retrieve the most relevant KB chunks for a ticket/query.
        """

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]

        ranked_indices = scores.argsort()[::-1][:top_k]

        results = []

        for index in ranked_indices:
            chunk = self.chunks[index].copy()
            chunk["score"] = round(float(scores[index]), 4)
            results.append(chunk)

        return results