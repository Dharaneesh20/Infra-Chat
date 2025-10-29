"""
Document Ingestion Script - Minimal Version
Works on Python 3.13 + Windows without numpy/FAISS issues
Processes documentation into simple JSON format for keyword search
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DOCS_DIR = Path("./docs")
OUTPUT_FILE = "./docs_index.json"

def load_documents_from_directory(docs_dir: Path):
    """
    Load all markdown and text files from the docs directory
    
    Args:
        docs_dir: Path to the documentation directory
        
    Returns:
        List of document dictionaries
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
                    
                    # Create a document dictionary
                    doc = {
                        "content": content,
                        "source": str(file_path.relative_to(docs_dir)),
                        "file_name": file_path.name,
                        "file_type": file_path.suffix
                    }
                    documents.append(doc)
                    print(f"✅ Loaded: {file_path.name}")
            
            except Exception as e:
                print(f"❌ Error loading {file_path.name}: {e}")
    
    return documents

def create_simple_index(documents):
    """
    Create a simple keyword-based index
    
    Args:
        documents: List of document dictionaries
        
    Returns:
        Dictionary index for quick keyword lookup
    """
    index = {
        "documents": documents,
        "metadata": {
            "total_docs": len(documents),
            "indexed_at": str(Path.cwd()),
            "mode": "simple_keyword"
        }
    }
    
    return index

def main():
    """Main ingestion pipeline"""
    print("\n🚀 Starting Document Ingestion (Minimal Mode)...")
    print("=" * 60)
    print("⚠️  Running in MINIMAL MODE - Vector embeddings disabled")
    print("   Reason: Python 3.13 + numpy compatibility issue")
    print("   Creating simple keyword-based index instead")
    print("=" * 60)
    print()
    
    # Step 1: Load documents
    print(f"📂 Loading documents from {DOCS_DIR}...\n")
    documents = load_documents_from_directory(DOCS_DIR)
    
    if not documents:
        print("\n⚠️  No documents found!")
        print(f"💡 Add some .md or .txt files to {DOCS_DIR} directory")
        return
    
    print(f"\n✅ Loaded {len(documents)} documents\n")
    
    # Step 2: Create simple index
    print("📝 Creating keyword index...")
    index = create_simple_index(documents)
    
    # Step 3: Save to JSON
    print(f"💾 Saving index to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Success! Indexed {len(documents)} documents")
    print(f"💾 Index stored at: {OUTPUT_FILE}")
    print("\n✅ You can now run 'python app_minimal.py' to start the chat API!")
    print("\n💡 To get full AI features with vector embeddings:")
    print("   Option 1: Use Python 3.11 instead of 3.13")
    print("   Option 2: Wait for numpy to fix Python 3.13 Windows support")
    print()

if __name__ == "__main__":
    main()
