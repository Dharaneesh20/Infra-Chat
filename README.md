# Infra-Chat 🤖☁️

> A conversational AI assistant with read-only access to your live cloud infrastructure and documentation, providing intelligent, combined answers.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)](https://www.typescriptlang.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm
- **Google Gemini API Key** ([Get one free](https://makersuite.google.com/app/apikey))
- **(Optional)** AWS credentials for cloud integration

### Installation

#### 1. Clone & Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

#### 2. Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
```

#### 3. Ingest Documentation (One-time)

```bash
cd backend
python ingest.py
```

This will process all markdown files in `backend/docs/` and store them in FAISS vector index.

#### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# App opens on http://localhost:3000
```

---

## 🎯 Features

### Tier 1: Core MVP ✅
- **🧠 AI-Powered Chat**: Natural language interface powered by Google Gemini
- **📚 Document Search (RAG)**: Intelligent search across your team's documentation using vector embeddings
- **☁️ Live Cloud Integration**: Real-time queries to AWS infrastructure (read-only)
- **🔗 Multi-Tool Agent**: LangChain-powered agent that intelligently combines data from multiple sources

### Tier 2: Impressive Features 🚧
- **📤 Live Document Upload**: Upload new documentation and query it instantly
- **⚡ Streaming Responses**: Real-time token-by-token responses like ChatGPT
- **🎨 Beautiful UI**: Modern, responsive chat interface built with React + TypeScript

### Tier 3: Future Vision 🔮
- **🏗️ Microservices Architecture**: Spring Boot (auth), Node.js (chat), Flask (AI)
- **🌐 Multi-Cloud Support**: Azure, GCP, and GitHub integrations
- **🔐 Enterprise Security**: SSO integration with role-based access control

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                    │
│                   http://localhost:3000                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (Flask + Python)                   │
│                   http://localhost:5000                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           LangChain AI Agent (Brain)                 │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │  │
│  │  │   Tool 1   │  │   Tool 2   │  │   Tool 3     │  │  │
│  │  │ DocSearch  │  │CloudSearch │  │GoogleSearch  │  │  │
│  │  │   (RAG)    │  │ (AWS API)  │  │  (Optional)  │  │  │
│  │  └─────┬──────┘  └─────┬──────┘  └──────┬───────┘  │  │
│  └────────┼───────────────┼─────────────────┼──────────┘  │
└───────────┼───────────────┼─────────────────┼─────────────┘
            ▼               ▼                 ▼
    ┌──────────────┐ ┌────────────┐  ┌──────────────┐
    │    FAISS     │ │ AWS Boto3  │  │ Google API   │
    │  (Vectors)   │ │  (EC2,S3)  │  │   (Search)   │
    └──────────────┘ └────────────┘  └──────────────┘
                         ▲
                         │
                  ┌──────┴────────┐
                  │ Google Gemini │
                  │  LLM API      │
                  └───────────────┘
```

---

## 📁 Project Structure

```
Infra-Chat/
├── backend/                    # Flask backend (Python)
│   ├── app.py                 # Main Flask application
│   ├── ingest.py              # One-time doc ingestion script
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── docs/                 # Sample documentation to ingest
│   │   ├── aws-setup.md
│   │   ├── deployment.md
│   │   └── troubleshooting.md
│   ├── tools/                # AI Agent tools
│   │   ├── doc_search.py     # RAG document search
│   │   ├── cloud_search.py   # AWS API integration
│   │   └── google_search.py  # Web search tool
│   └── faiss_index/          # FAISS vector index (auto-generated)
│
├── frontend/                  # React frontend (TypeScript)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx    # Main chat interface
│   │   │   ├── MessageList.tsx   # Message display
│   │   │   └── InputBox.tsx      # User input
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tsconfig.json
│
└── README.md                  # This file
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | React + TypeScript | Modern, type-safe, industry standard |
| **Backend** | Flask (Python) | Fastest way to build AI/RAG backends |
| **AI Framework** | LangChain | Easy orchestration of LLM + tools |
| **LLM** | Google Gemini API | Powerful, free tier available |
| **Vector DB** | FAISS | Fast, efficient, runs locally (no compiler needed) |
| **Cloud API** | AWS Boto3 | Official AWS Python SDK |

---

## 🎓 Demo Scenarios

### Scenario 1: Combined Query
**User:** "What EC2 instances are tagged 'prod' and where's the setup guide?"

**Agent Actions:**
1. 🔧 Calls `CloudSearch` → Gets live AWS EC2 list
2. 📚 Calls `DocSearch` → Retrieves setup guide from docs
3. 🤖 Sends both to Gemini → Generates combined answer

**Response:** 
```
You have 3 EC2 instances tagged 'prod':
- i-abc123 (t2.micro) - Running
- i-def456 (t3.small) - Running  
- i-ghi789 (t2.small) - Stopped

For the setup guide, here's what you need to know:
[... relevant sections from your docs ...]
```

### Scenario 2: Live Document Upload
1. Upload new `project-x-readme.md`
2. Ask: "Tell me about Project X"
3. Bot instantly knows the content! ✨

---

## 🔒 Security Notes

- **Read-Only Access**: AWS keys should have read-only IAM permissions
- **No Credentials in Code**: All secrets in `.env` (gitignored)
- **Future**: Add SSO + role-based access control

---

## 🚧 Development Roadmap

- [ ] **Phase 1**: Core MVP (Chat + RAG + AWS)
- [ ] **Phase 2**: Live upload + streaming responses
- [ ] **Phase 3**: Multi-cloud support (Azure, GCP)
- [ ] **Phase 4**: Microservices architecture
- [ ] **Phase 5**: Enterprise security (SSO, RBAC)

---

## 🤝 Contributing

This is a hackathon project! Feel free to:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

MIT License - feel free to use this in your portfolio!

---

## 👨‍💻 Interview Talking Points

**"Where would you take this next?"**

1. **Microservices Split:**
   - Spring Boot: User auth + team management
   - Node.js: Real-time chat with WebSockets
   - Flask: Dedicated AI inference service

2. **Multi-Cloud:**
   - Add Azure Resource Manager APIs
   - Add GCP Cloud APIs
   - Add GitHub integration (commits, PRs)

3. **Enterprise Security:**
   - SSO integration (Okta, Azure AD)
   - Role-based access (dev vs admin queries)
   - Audit logging for compliance

4. **Scalability:**
   - Replace FAISS with Pinecone/Weaviate (cloud vector DB)
   - Add Redis caching layer
   - Kubernetes deployment

---

## 🎉 Built With Love for Hackathons

This project showcases:
- ✅ Modern full-stack development (React + Flask)
- ✅ AI/ML integration (LangChain + Gemini)
- ✅ Cloud infrastructure knowledge (AWS)
- ✅ Production-ready architecture thinking
- ✅ Clean, maintainable code

**Perfect for your portfolio and technical interviews!** 🚀

---

## 📧 Contact

Questions? Open an issue or reach out!


