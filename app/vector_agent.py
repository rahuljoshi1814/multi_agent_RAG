import chromadb
from chromadb.config import Settings

# Globals for lazy loading
model = None
collection = None

def init_vector_db():
    global model, collection
    if model is None or collection is None:
        from sentence_transformers import SentenceTransformer

        # Use lightweight model to reduce memory usage
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        # Initialize ChromaDB client
        client = chromadb.Client(Settings(anonymized_telemetry=False))
        collection = client.create_collection(name="rag_fallback")

        # Small knowledge base documents
        documents = [
            "Alice Smith spent the most in Q1 2023, totaling $15,000.",
            "Bob Johnson is our top customer in electronics category.",
            "In 2022, total sales were $275,000 across all departments.",
            "Managers are responsible for approving large purchases.",
            "Quarter 4 of 2023 saw a drop in clothing sales."
        ]

        # Add to collection with embedded vectors
        collection.add(
            documents=documents,
            ids=[f"doc{i}" for i in range(len(documents))],
            embeddings=model.encode(documents).tolist()
        )

def fallback_answer(question: str) -> str:
    init_vector_db()
    query_vector = model.encode([question]).tolist()[0]
    results = collection.query(query_embeddings=[query_vector], n_results=1)
    
    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0]  # Top match

    return "I'm sorry, I couldn’t find any relevant info."
