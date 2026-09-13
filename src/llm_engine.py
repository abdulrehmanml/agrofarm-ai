import logging
from google import genai
from google.genai import types

from src.config import GEMINI_API_KEY
from src.rag_engine import RAGEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class LLMEngine:
    """Orchestrates communication with the Gemini LLM for answer generation."""
    
    def __init__(self):
        if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            raise ValueError("Invalid Gemini API Key. Please update src/config.py")
            
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # Using gemini-2.5-flash as the fast, cost-effective default for RAG tasks
        self.model_id = "gemini-2.5-flash"
        logging.info("LLM Engine successfully initialized.")

    def generate_answer(self, query: str, context_docs: list[str], field_data: dict = None) -> str:
            """Generates a response based on the provided RAG context and live field data."""
            context_text = "\n\n".join(context_docs)
            
            # Inject live telemetry if a field is selected
            field_context = ""
            if field_data and "error" not in field_data:
                field_context = f"""
    Current Field Conditions:
    - Crop: {field_data.get('crop')} (Stage: {field_data.get('growth_stage')})
    - Soil Moisture: {field_data.get('soil_moisture_pct')}%
    - Days since last irrigated: {field_data.get('last_irrigated_days_ago')}
    - NPK Levels: {field_data.get('N')}/{field_data.get('P')}/{field_data.get('K')}, pH: {field_data.get('ph')}
    """
    
            prompt = f"""You are AgroFarm AI, an expert agronomy advisor. 
    Answer the user's question using ONLY the provided knowledge base context and the current field conditions. If the answer is not in the context, state that you do not have enough information. Do not guess.
    
    {field_context}
    
    Knowledge Base Context:
    {context_text}
    
    Question:
    {query}
    """
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2, # Low temperature ensures factual, grounded RAG responses
                    )
                )
                return response.text
            except Exception as e:
                logging.error(f"Failed to generate LLM response: {e}")
                return "I'm sorry, I encountered an error while communicating with the AI model."

if __name__ == "__main__":
    # Integration test: Combining RAG retrieval with LLM generation
    print("Testing full RAG -> LLM pipeline...")
    rag = RAGEngine()
    llm = LLMEngine()
    
    test_query = "What is the recommended irrigation schedule for wheat during the tillering stage?"
    print(f"\nQuery: {test_query}")
    
    docs = rag.retrieve_context(test_query)
    print(f"Retrieved {len(docs)} documents.")
    
    answer = llm.generate_answer(test_query, docs)
    print(f"\nGenerated Answer:\n{answer}")