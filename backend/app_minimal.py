"""
Infra-Chat Backend API - Minimal Version (Without FAISS)
Works on Python 3.13 + Windows without numpy/FAISS issues
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Load documentation index
DOCS_INDEX = None
DOCS_INDEX_PATH = Path("./docs_index.json")

try:
    if DOCS_INDEX_PATH.exists():
        with open(DOCS_INDEX_PATH, 'r', encoding='utf-8') as f:
            DOCS_INDEX = json.load(f)
        print(f"✅ Loaded {DOCS_INDEX['metadata']['total_docs']} documents from index")
    else:
        print(f"⚠️  No docs index found. Run 'python ingest_minimal.py' first!")
except Exception as e:
    print(f"⚠️  Error loading docs index: {e}")

# Fallback documentation
SAMPLE_DOCS = {
    "deployment": "To deploy to AWS: 1) Set up an EC2 instance, 2) Configure security groups, 3) Deploy your application using Docker or direct installation.",
    "troubleshooting": "Common issues: Check API keys in .env file, verify AWS credentials, ensure backend is running on port 5000, check CORS settings.",
    "aws-setup": "AWS Setup: Create an IAM user with appropriate permissions, generate access keys, configure AWS CLI with 'aws configure', test connection."
}

def search_docs(query):
    """Search through indexed documentation"""
    if not DOCS_INDEX:
        return None
    
    query_lower = query.lower()
    matches = []
    
    for doc in DOCS_INDEX.get('documents', []):
        content = doc.get('content', '').lower()
        if any(word in content for word in query_lower.split()):
            matches.append({
                'source': doc['file_name'],
                'snippet': doc['content'][:300] + '...' if len(doc['content']) > 300 else doc['content']
            })
    
    return matches[:2]  # Return top 2 matches

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'message': 'Infra-Chat API is running (minimal mode - FAISS disabled due to numpy compatibility)'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - simplified version without AI agent
    Returns helpful responses based on documentation search
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Try to search indexed documentation first
        doc_matches = search_docs(user_message)
        
        if doc_matches:
            response = "Based on the documentation:\n\n"
            for match in doc_matches:
                response += f"📄 From {match['source']}:\n{match['snippet']}\n\n"
        else:
            # Fallback to keyword matching
            user_message_lower = user_message.lower()
            response = ""
            
            if 'deploy' in user_message_lower or 'deployment' in user_message_lower:
                response = SAMPLE_DOCS['deployment']
            elif 'troubleshoot' in user_message_lower or 'error' in user_message_lower or 'problem' in user_message_lower:
                response = SAMPLE_DOCS['troubleshooting']
            elif 'aws' in user_message_lower or 'cloud' in user_message_lower:
                response = SAMPLE_DOCS['aws-setup']
            elif 'help' in user_message_lower:
                response = "I can help with: deployment, troubleshooting, and AWS setup. Ask me anything about these topics!"
            else:
                response = "I'm currently running in minimal mode. Try asking about: deployment, troubleshooting, or AWS setup."
        
        return jsonify({
            'response': response,
            'mode': 'minimal',
            'note': 'AI agent disabled - using simple keyword matching'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred processing your request'
        }), 500

if __name__ == '__main__':
    print("\n🚀 Starting Infra-Chat Backend (Minimal Mode)")
    print("=" * 60)
    print("⚠️  Running in MINIMAL MODE - AI features disabled")
    print("   Reason: Python 3.13 + numpy compatibility issue")
    print("   ")
    print("✅ API Endpoints Available:")
    print("   - GET  /api/health  (Health check)")
    print("   - POST /api/chat    (Simple keyword-based chat)")
    print("=" * 60)
    print(f"🌐 Server running on http://127.0.0.1:5000")
    print("🔗 Frontend should connect to this address")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
