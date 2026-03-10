from fastapi import FastAPI
from pydantic import BaseModel

from app.embeddings.embedding_model import EmbeddingModel
from app.cache.semantic_cache import SemanticCache

app = FastAPI()

model = EmbeddingModel()
cache = SemanticCache()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
def query_system(request: QueryRequest):

    query = request.query
    query_vector = model.encode_query(query)

    hit = cache.lookup(query_vector)

    if hit:
        entry = hit["entry"]

        return {
            "query": query,
            "cache_hit": True,
            "matched_query": entry["query"],
            "similarity_score": hit["score"],
            "result": entry["result"],
            "dominant_cluster": entry["cluster"]
        }

    result = "Computed search result"

    cache.add(query, query_vector, result, cluster=0)

    return {
        "query": query,
        "cache_hit": False,
        "matched_query": None,
        "similarity_score": 0,
        "result": result,
        "dominant_cluster": 0
    }


@app.get("/cache/stats")
def cache_stats():
    return cache.stats()


@app.delete("/cache")
def clear_cache():
    cache.clear()
    return {"message": "cache cleared"}
