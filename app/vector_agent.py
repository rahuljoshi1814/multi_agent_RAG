import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import os

# Globals for lazy loading
model = None
collection = None

def init_vector_db():
    global model, collection

    if model is None:
        # Load lightweight embedding model
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

    if collection is None:
        # Persistent vector DB storage
        persist_dir = "./chromadb_store"
        os.makedirs(persist_dir, exist_ok=True)

        client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            persist_directory=persist_dir
        ))

        try:
            collection = client.get_collection("rag_fallback")
        except:
            collection = client.create_collection(name="rag_fallback")

            # Predefined fallback documents
            documents = [
                "Alice Smith spent the most in Q1 2023, totaling $15,000.",
                "Bob Johnson is our top customer in electronics category.",
                "In 2022, total sales were $275,000 across all departments.",
                "Top spender in the first quarter was Alice.",
                "Managers are responsible for approving large purchases.",
                "Quarter 4 of 2023 saw a drop in clothing sales."
            ]

            clean_docs = [doc for doc in documents if doc.strip()]
            embeddings = model.encode(clean_docs).tolist()
            ids = [str(uuid.uuid4()) for _ in clean_docs]

            collection.add(documents=clean_docs, ids=ids, embeddings=embeddings)
            client.persist()  # Save the collection to disk

def fallback_answer(question: str) -> str:
    init_vector_db()
    query_vector = model.encode([question]).tolist()[0]

    results = collection.query(query_embeddings=[query_vector], n_results=1)

    if results["documents"] and results["documents"][0]:
        return f"Fallback answer: {results['documents'][0][0]}"

    return "I'm sorry, I couldn’t find any relevant information in fallback memory."
