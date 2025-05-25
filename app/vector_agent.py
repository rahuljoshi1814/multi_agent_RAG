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

        # Avoid creating the collection again if it already exists
        try:
            collection = client.get_collection("rag_fallback")
        except:
            collection = client.create_collection(name="rag_fallback")

        # Fallback document list
        documents = [
            "Alice Smith spent the most in Q1 2023, totaling $15,000.",
            "Bob Johnson is our top customer in electronics category.",
            "In 2022, total sales were $275,000 across all departments.",
            "Top spender in the first quarter was Alice.",
            "Managers are responsible for approving large purchases.",
            "Quarter 4 of 2023 saw a drop in clothing sales."
        ]

        # Make sure all documents are non-empty
        clean_docs = [doc for doc in documents if doc.strip() != ""]

        # Add documents safely
        collection.add(
            documents=clean_docs,
            ids=[f"doc{i}" for i in range(len(clean_docs))],
            embeddings=model.encode(clean_docs).tolist()
        )

def fallback_answer(question: str) -> str:
    init_vector_db()
    query_vector = model.encode([question]).tolist()[0]
    results = collection.query(query_embeddings=[query_vector], n_results=1)

    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0]  # Return top match

    return "I'm sorry, I couldn’t find any relevant info."
