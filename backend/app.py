"""
Infra-Chat Backend API
A Flask application that provides an AI-powered chat interface with access to
documentation and cloud infrastructure.
"""

# Suppress numpy warnings on Python 3.13 + Windows
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool

# Import our custom tools
from tools.doc_search import search_documentation
from tools.cloud_search import search_aws_resources
from tools.google_search import google_search

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Define tools for the AI agent
tools = [
    Tool(
        name="DocumentSearch",
        func=search_documentation,
        description="""
        Use this tool to search through the team's documentation and README files.
        Input should be a clear question or search query about documentation, 
        setup guides, troubleshooting steps, or any written team knowledge.
        Example: "find the deployment guide" or "how to setup the database"
        """
    ),
    Tool(
        name="CloudSearch",
        func=search_aws_resources,
        description="""
        Use this tool to get real-time information about AWS cloud infrastructure.
        You can query EC2 instances, S3 buckets, and other AWS resources.
        Input should specify what AWS resource you want to query.
        Example: "list all EC2 instances" or "show S3 buckets" or "get instances tagged prod"
        """
    ),
    Tool(
        name="GoogleSearch",
        func=google_search,
        description="""
        Use this tool for general web searches when the user asks about topics
        not covered in documentation or cloud infrastructure.
        Input should be a search query.
        Example: "what is kubernetes" or "latest AWS pricing"
        """
    )
]

# Create the agent prompt
agent_prompt = PromptTemplate.from_template("""
You are Infra-Chat, an intelligent assistant that helps engineers by combining information 
from team documentation, live cloud infrastructure, and general knowledge.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

When answering questions:
1. Analyze what the user is asking for
2. Use the appropriate tools to gather information
3. Combine the information into a helpful, well-formatted response
4. If you use multiple tools, synthesize the results clearly

Always be helpful, concise, and provide actionable information.

Question: {input}

Thought: {agent_scratchpad}
""")

# Create the agent
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Infra-Chat API is running",
        "version": "1.0.0"
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that processes user messages and returns AI responses
    
    Expected JSON body:
    {
        "message": "user's question or command"
    }
    
    Returns:
    {
        "response": "AI assistant's response",
        "success": true/false
    }
    """
    try:
        # Get the user's message
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "No message provided"
            }), 400
        
        # Process the message through the AI agent
        print(f"\n🤖 Processing: {user_message}")
        
        result = agent_executor.invoke({"input": user_message})
        response_text = result.get('output', 'I apologize, but I could not generate a response.')
        
        print(f"✅ Response generated: {response_text[:100]}...")
        
        return jsonify({
            "success": True,
            "response": response_text
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """
    Upload and ingest new documentation (Tier 2 feature)
    
    Expected: multipart/form-data with 'file' field
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file provided"
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "Empty filename"
            }), 400
        
        # Only accept markdown and text files
        if not (file.filename.endswith('.md') or file.filename.endswith('.txt')):
            return jsonify({
                "success": False,
                "error": "Only .md and .txt files are supported"
            }), 400
        
        # Save the file temporarily
        file_content = file.read().decode('utf-8')
        
        # TODO: Implement live ingestion (Tier 2)
        # For now, just acknowledge receipt
        
        return jsonify({
            "success": True,
            "message": f"File '{file.filename}' uploaded successfully",
            "note": "Live ingestion coming in Tier 2!"
        })
    
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Check for required API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  WARNING: GOOGLE_API_KEY not found in environment!")
        print("📝 Please copy .env.example to .env and add your API key")
        print("🔑 Get a free API key: https://makersuite.google.com/app/apikey")
    
    print("🚀 Starting Infra-Chat Backend...")
    print("📍 Running on http://localhost:5000")
    print("📚 Make sure you've run 'python ingest.py' first!")
    
    app.run(debug=True, port=5000)
