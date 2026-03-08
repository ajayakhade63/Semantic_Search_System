Semantic Search System with Fuzzy Clustering and Semantic Cache

Overview

This project implements a lightweight semantic search system using the 20 Newsgroups dataset, which contains around 20,000 documents across 20 overlapping topic categories.

The system demonstrates how to combine:

Transformer-based embeddings
Vector similarity search
Fuzzy clustering
A custom semantic cache
A FastAPI service

The goal is to enable semantic query matching, allowing the system to recognize queries with similar meaning even when phrased differently.

For example:
"space shuttle launch"
"launch of a space shuttle"

These queries are treated as semantically similar, enabling efficient cache reuse and improved search performance.

System Architecture
The system follows this pipeline:
User Query
   ↓
FastAPI Endpoint
   ↓
Query Embedding (Sentence Transformer)
   ↓
Semantic Cache Lookup
   ↓
Cache Hit → Return cached result
Cache Miss → Perform Vector Search
   ↓
FAISS Vector Database
   ↓
Fuzzy Clustering Analysis
   ↓
Return Result + Cache Storage

Project Structure

semantic-search-system
│
├── app
│   ├── api
│   │   └── main.py
│   │
│   ├── cache
│   │   ├── semantic_cache.py
│   │   └── cache_stats.py
│   │
│   ├── clustering
│   │   ├── fuzzy_cluster.py
│   │   └── cluster_analysis.py
│   │
│   ├── data
│   │   ├── loader.py
│   │   └── preprocessing.py
│   │
│   ├── embeddings
│   │   └── embedding_model.py
│   │
│   ├── config.py
│   └── main.py
│
├── dataset
├── notebooks
├── Dockerfile
├── requirements.txt
└── README.md

Dataset
The project uses the 20 Newsgroups dataset.
This dataset contains discussion posts across topics such as:
politics
sports
religion
technology
science
The dataset is noisy and includes headers, routing information, and formatting artifacts, which are handled during preprocessing.

Key Components
1. Text Preprocessing
Before generating embeddings, the dataset is cleaned using:
lowercasing
whitespace normalization
removal of punctuation and special characters
This improves embedding quality.

2. Transformer Embeddings
The system uses Sentence Transformers from Hugging Face.
Model used:
all-MiniLM-L6-v2
Reasons for choosing this model:
lightweight and fast
produces 384-dimensional embeddings
strong performance for semantic similarity tasks
widely used in search and retrieval systems
Each document is converted into a semantic vector representation.

3. Vector Database (FAISS)
To enable efficient similarity search, embeddings are stored using FAISS.
FAISS allows fast nearest-neighbor search in high-dimensional embedding space.
When a query is received:
The query is converted into an embedding
FAISS retrieves the most similar document vectors

5. Fuzzy Clustering
The dataset topics overlap significantly, so hard clustering is not appropriate.
Instead, the system uses Fuzzy C-Means clustering.
Unlike traditional clustering, fuzzy clustering assigns probabilistic cluster membership.
Example:
Document A
Cluster 3 → 0.62
Cluster 8 → 0.28
Cluster 1 → 0.10

This better reflects the real semantic structure of the dataset.
The clustering logic is implemented in:
app/clustering/fuzzy_cluster.py
Cluster analysis utilities are provided in:
cluster_analysis.py

5. Semantic Cache (No Redis)
Traditional caches like Redis rely on exact key matching.
Example:
"space shuttle launch"
But semantic queries can be phrased differently:
"launch of a space shuttle"
To solve this problem, this project implements a custom semantic cache from first principles.
Each cache entry stores:
query text
embedding vector
result
cluster ID

When a new query arrives:
Convert query to embedding
Compare with cached embeddings using cosine similarity
If similarity exceeds threshold → cache hit
Otherwise → compute result and store it
The similarity threshold is configurable.
This approach enables semantic caching without Redis or any external caching middleware.
FastAPI Service

The system is exposed via a FastAPI API service.

Endpoint: Query
POST /query
Request:
{
  "query": "space shuttle launch"
}
Response:
{
  "query": "...",
  "cache_hit": true,
  "matched_query": "...",
  "similarity_score": 0.91,
  "result": "...",
  "dominant_cluster": 3
}
Cache Statistics
GET /cache/stats

Example response:
{
  "total_entries": 42,
  "hit_count": 17,
  "miss_count": 25,
  "hit_rate": 0.405
}
Clear Cache
DELETE /cache

Resets cache entries and statistics.

Running the Project
1. Create Virtual Environment
python -m venv venv
venv\Scripts\activate
2. Install Dependencies
pip install -r requirements.txt
3. Start the API Service
uvicorn app.main:app --reload
4. Open Swagger UI
http://127.0.0.1:8000/docs

Swagger provides an interactive interface for testing the API.

Docker Support (Optional)

A Dockerfile is included to containerize the FastAPI service.

Build image:

docker build -t semantic-search-system .

Run container:

docker run -p 8000:8000 semantic-search-system

Then access:

http://localhost:8000/docs
Key Design Decisions
Why Sentence Transformers?

Efficient semantic embeddings

Small model size

Strong performance for similarity search

Why FAISS?

Optimized for vector search

Efficient nearest neighbor retrieval

Scales well for large datasets

Why Fuzzy Clustering?

Documents may belong to multiple semantic topics, so fuzzy clustering captures topic overlap better than hard clustering.

Why Custom Semantic Cache?

Traditional caches cannot detect semantically equivalent queries.
This system uses vector similarity to detect similar queries, enabling more intelligent caching.

Conclusion

This project demonstrates how to build a semantic search system with intelligent caching using modern NLP techniques.

Key features include:

transformer-based semantic embeddings

vector similarity search

fuzzy clustering

custom semantic caching

FastAPI deployment

The system highlights how semantic understanding can improve search and caching behavior in real-world applications.
