import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SemanticCache:

    def __init__(self, similarity_threshold=0.85):

        self.entries = []
        self.similarity_threshold = similarity_threshold

        self.hit_count = 0
        self.miss_count = 0

    def lookup(self, query_vector):

        if len(self.entries) == 0:
            self.miss_count += 1
            return None

        stored_vectors = [entry["vector"] for entry in self.entries]

        similarities = cosine_similarity([query_vector], stored_vectors)[0]

        best_index = np.argmax(similarities)
        best_score = similarities[best_index]

        if best_score >= self.similarity_threshold:

            self.hit_count += 1
            return {
                "entry": self.entries[best_index],
                "score": float(best_score)
            }

        self.miss_count += 1
        return None

    def add(self, query, vector, result, cluster):

        entry = {
            "query": query,
            "vector": vector,
            "result": result,
            "cluster": cluster
        }

        self.entries.append(entry)

    def stats(self):

        total_requests = self.hit_count + self.miss_count

        hit_rate = 0
        if total_requests > 0:
            hit_rate = self.hit_count / total_requests

        return {
            "total_entries": len(self.entries),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate
        }

    def clear(self):

        self.entries = []
        self.hit_count = 0
        self.miss_count = 0
