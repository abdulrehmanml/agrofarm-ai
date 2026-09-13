import pickle
import logging
from pathlib import Path
from typing import List

import chromadb

# Import paths from our centralized config
from src.config import VECTORSTORE_PATH, VECTORIZER_PATH

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class RAGEngine:
    """Handles semantic search and retrieval from the ChromaDB vector store."""
    
    def __init__(self, vectorstore_path: Path = VECTORSTORE_PATH, vectorizer_path: Path = VECTORIZER_PATH):
        self.collection_name = "agronomy_knowledge"
        
        try:
            # Initialize ChromaDB client and load the TF-IDF vectorizer
            self.client = chromadb.PersistentClient(path=str(vectorstore_path))
            self.collection = self.client.get_collection(name=self.collection_name)
            
            with open(vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)
                
            logging.info("RAG Engine successfully initialized.")
        except Exception as e:
            logging.error(f"Critical Error initializing RAG Engine: {e}")
            raise

    def retrieve_context(self, query: str, top_k: int = 3) -> List[str]:
        """Vectorizes the query and retrieves top_k relevant text chunks."""
        try:
            query_vector = self.vectorizer.transform([query]).toarray().tolist()
            
            results = self.collection.query(
                query_embeddings=query_vector,
                n_results=top_k
            )
            
            # Extract and return the flat list of documents
            if results and results.get("documents"):
                return results["documents"][0]
            return []
            
        except Exception as e:
            logging.error(f"Search retrieval failed: {e}")
            return []

if __name__ == "__main__":
    # Quick test to verify it works independently
    engine = RAGEngine()
    
    print("\nRAG System Ready! (Type 'exit' to quit)")
    
    while True:
        user_query = input("\nAsk your question: ")
        
        if user_query.lower() == 'exit':
            print("Exiting...")
            break
            
        docs = engine.retrieve_context(user_query)
        print(f"Retrieved {len(docs)} documents.")