"""
Document Search Tool (RAG)
Uses FAISS to search through ingested documentation
"""

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Configuration
FAISS_INDEX_PATH = "./faiss_index"

# Initialize embeddings (same as used in ingestion)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Load the vector store
try:
    vectorstore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
except Exception as e:
    print(f"⚠️  Warning: Could not load FAISS index: {e}")
    print("💡 Make sure you've run 'python ingest.py' first!")
    vectorstore = None


def search_documentation(query: str) -> str:
    """
    Search through documentation using vector similarity
    
    Args:
        query: The search query from the user
        
    Returns:
        Relevant documentation excerpts as a formatted string
    """
    if vectorstore is None:
        return "Error: Documentation database not initialized. Please run 'python ingest.py' first."
    
    try:
        # Search for relevant documents
        results = vectorstore.similarity_search(query, k=3)
        
        if not results:
            return "No relevant documentation found for your query."
        
        # Format the results
        formatted_results = []
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content.strip()
            
            formatted_results.append(
                f"--- Document {i} (from {source}) ---\n{content}\n"
            )
        
        response = "\n".join(formatted_results)
        print(f"📚 DocSearch found {len(results)} relevant documents")
        
        return response
    
    except Exception as e:
        return f"Error searching documentation: {str(e)}"


# Test function
if __name__ == "__main__":
    # Test the search
    test_query = "deployment guide"
    print(f"Testing search for: {test_query}\n")
    result = search_documentation(test_query)
    print(result)
