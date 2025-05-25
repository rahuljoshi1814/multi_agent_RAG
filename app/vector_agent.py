import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Use Sentence Transformer for vector embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB client (local, in-memory)
client = chromadb.Client(Settings(anonymized_telemetry=False))

# Collection = knowledge base
collection = client.create_collection(name="rag_fallback")

# Add your fallback docs here (small text chunks)
documents = [
    "Alice Smith spent the most in Q1 2023, totaling $15,000.",
    "Bob Johnson is our top customer in electronics category.",
    "In 2022, total sales were $275,000 across all departments.",
    "Managers are responsible for approving large purchases.",
    "Quarter 4 of 2023 saw a drop in clothing sales."
]

collection.add(
    documents=documents,
    ids=[f"doc{i}" for i in range(len(documents))],
    embeddings=model.encode(documents).tolist()
)

# Fallback search function
def fallback_answer(question: str) -> str:
    query_vector = model.encode([question]).tolist()[0]
    results = collection.query(query_embeddings=[query_vector], n_results=1)
    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0]  # top result
    return "I'm sorry, I couldn’t find any relevant info."

