"""
Document Ingestion Script
This script runs once to load all documentation into FAISS.
It splits documents into chunks, creates embeddings, and stores them for RAG.
"""

# Suppress numpy warnings on Python 3.13 + Windows
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configuration
DOCS_DIR = Path("./docs")
FAISS_INDEX_PATH = "./faiss_index"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents_from_directory(docs_dir: Path):
    """
    Load all markdown and text files from the docs directory
    
    Args:
        docs_dir: Path to the documentation directory
        
    Returns:
        List of Document objects
    """
    documents = []
    
    if not docs_dir.exists():
        print(f"⚠️  Warning: {docs_dir} does not exist!")
        return documents
    
    # Find all markdown and text files
    file_patterns = ["*.md", "*.txt"]
    
    for pattern in file_patterns:
        for file_path in docs_dir.rglob(pattern):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Create a Document object with metadata
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": str(file_path.relative_to(docs_dir)),
                            "file_name": file_path.name,
                            "file_type": file_path.suffix
                        }
                    )
                    documents.append(doc)
                    print(f"✅ Loaded: {file_path.name}")
            
            except Exception as e:
                print(f"❌ Error loading {file_path.name}: {e}")
    
    return documents


def split_documents(documents):
    """
    Split documents into smaller chunks for better retrieval
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of split Document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"📄 Split into {len(chunks)} chunks")
    
    return chunks


def create_vector_store(chunks):
    """
    Create embeddings and store in FAISS
    
    Args:
        chunks: List of document chunks
        
    Returns:
        FAISS vector store instance
    """
    # Initialize embeddings with Google Gemini
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create FAISS index from documents
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    # Save to disk
    vectorstore.save_local(FAISS_INDEX_PATH)
    
    return vectorstore


def main():
    """Main ingestion pipeline"""
    print("🚀 Starting Document Ingestion...\n")
    
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("❌ Error: GOOGLE_API_KEY not found!")
        print("📝 Please copy .env.example to .env and add your API key")
        print("🔑 Get a free key: https://makersuite.google.com/app/apikey")
        return
    
    # Step 1: Load documents
    print(f"📂 Loading documents from {DOCS_DIR}...\n")
    documents = load_documents_from_directory(DOCS_DIR)
    
    if not documents:
        print("\n⚠️  No documents found!")
        print(f"💡 Add some .md or .txt files to {DOCS_DIR} directory")
        return
    
    print(f"\n✅ Loaded {len(documents)} documents\n")
    
    # Step 2: Split into chunks
    print("✂️  Splitting documents into chunks...\n")
    chunks = split_documents(documents)
    
    # Step 3: Create embeddings and store
    print("\n🧠 Creating embeddings and storing in FAISS...")
    print("⏳ This may take a moment...\n")
    
    vectorstore = create_vector_store(chunks)
    
    print(f"\n🎉 Success! Ingested {len(chunks)} chunks into FAISS")
    print(f"💾 Database stored at: {FAISS_INDEX_PATH}")
    print("\n✅ You can now run 'python app.py' to start the chat API!")


if __name__ == "__main__":
    main()
