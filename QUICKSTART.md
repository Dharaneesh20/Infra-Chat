# 🚀 Infra-Chat Quickstart Guide

## ✅ Prerequisites Check

Before starting, verify you have:
- ✅ Python 3.11+ installed (3.13 works with minimal mode)
- ✅ Node.js 18+ and npm installed
- ✅ Git initialized in the project

### Quick Verification:
```powershell
python --version    # Should show 3.11 or higher
node --version      # Should show 18.0.0 or higher
npm --version       # Should show 9.0.0 or higher
git --version       # Should show 2.0.0 or higher
```

---

## 🎯 Complete Setup & Run (5 Minutes)

### Step 1: Backend Setup

```powershell
# Navigate to backend directory
cd d:\Infra-Chat\backend

# Activate virtual environment (if exists)
# If venv doesn't exist, create it first: python -m venv venv
venv\Scripts\Activate.ps1

# Install Python dependencies (if not already done)
pip install -r requirements.txt

# Create .env file with your API keys
Copy-Item .env.example .env
notepad .env  # Add your API keys
```

**Edit `.env` file:**
```env
# Required for AI mode (optional for minimal mode)
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional - for AWS features
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
```

**Get Google API Key (Free):**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy and paste into `.env`

---

### Step 2: Index Documentation

```powershell
# Still in d:\Infra-Chat\backend

# Option A: Minimal mode (Python 3.13 compatible)
python ingest_minimal.py

# Option B: Full AI mode (Python 3.11 required)
python ingest.py
```

**Expected output:**
```
🚀 Starting Document Ingestion...
✅ Loaded: aws-setup.md
✅ Loaded: deployment.md
✅ Loaded: troubleshooting.md
🎉 Success! Indexed 3 documents
```

---

### Step 3: Start Backend Server

```powershell
# Choose based on your Python version:

# Option A: Minimal mode (Python 3.13 - no numpy issues)
python app_minimal.py

# Option B: Full AI mode (Python 3.11 - with Gemini AI)
python app.py
```

**Expected output:**
```
🚀 Starting Infra-Chat Backend
============================================================
✅ API Endpoints Available:
   - GET  /api/health  (Health check)
   - POST /api/chat    (Chat interface)
============================================================
🌐 Server running on http://127.0.0.1:5000
```

**✅ Backend is ready when you see:** `Running on http://127.0.0.1:5000`

---

### Step 4: Start Frontend (New Terminal)

Open a **NEW PowerShell terminal** and run:

```powershell
# Navigate to frontend directory
cd d:\Infra-Chat\frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**✅ Frontend is ready when you see:** `http://localhost:5173/`

---

## 🧪 Testing Your Application

### Test 1: Health Check

Open browser or use curl:
```powershell
# PowerShell
Invoke-RestMethod http://localhost:5000/api/health

# Or visit in browser
# http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "Infra-Chat API is running"
}
```

---

### Test 2: Chat API

Test the chat endpoint:
```powershell
$body = @{
    message = "How do I deploy to AWS?"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/chat `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Expected response:**
```json
{
  "response": "Based on the documentation:\n\n📄 From deployment.md:\nTo deploy to AWS...",
  "mode": "minimal"
}
```

---

### Test 3: Frontend Interface

1. **Open browser:** http://localhost:5173/

2. **You should see:**
   - Clean chat interface
   - Input box at the bottom
   - "Infra-Chat" title

3. **Test queries:**
   ```
   "How do I deploy to AWS?"
   "Show me troubleshooting steps"
   "Help with AWS setup"
   "What are the deployment options?"
   ```

4. **Expected behavior:**
   - Your message appears on the right
   - AI response appears on the left
   - Typing indicator shows while processing
   - Smooth animations

---

## 🔍 Troubleshooting

### Issue: Backend won't start

**Error:** `numpy crashes` or `FAISS not found`

**Solution:**
```powershell
# Use minimal mode instead
cd d:\Infra-Chat\backend
python app_minimal.py
```

---

### Issue: "GOOGLE_API_KEY not found"

**Error:** `No API key configured`

**Solution:**
```powershell
# 1. Check if .env exists
cd d:\Infra-Chat\backend
Test-Path .env  # Should return True

# 2. If False, create it
Copy-Item .env.example .env

# 3. Edit and add your key
notepad .env
# Add: GOOGLE_API_KEY=your_actual_key_here
```

---

### Issue: Frontend can't connect to backend

**Error:** `Network Error` or `CORS Error`

**Solution:**
```powershell
# 1. Verify backend is running
Invoke-RestMethod http://localhost:5000/api/health

# 2. Check frontend .env (should be empty or not exist)
cd d:\Infra-Chat\frontend
# Vite automatically uses http://localhost:5000 for /api routes

# 3. Restart both servers
# Kill with Ctrl+C and restart
```

---

### Issue: Port already in use

**Error:** `Port 5000 is already in use`

**Solution:**
```powershell
# Option 1: Find and kill process
Get-Process -Name python | Stop-Process -Force

# Option 2: Use different port
# Edit app_minimal.py line: app.run(port=5001)
```

---

## 📦 Testing with Git Repository

### Clone and Setup

If someone else wants to run your project:

```powershell
# 1. Clone repository
git clone <your-repo-url>
cd Infra-Chat

# 2. Backend setup
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with API keys

# 3. Frontend setup
cd ..\frontend
npm install

# 4. Run (2 terminals)
# Terminal 1:
cd backend
python app_minimal.py

# Terminal 2:
cd frontend
npm run dev
```

---

## 🎯 Sample Test Scenarios

### Scenario 1: Deployment Query
**Input:** "How do I deploy my application to AWS?"

**Expected:** Response with deployment steps from `deployment.md`

---

### Scenario 2: Troubleshooting Query
**Input:** "My app is not working, help me troubleshoot"

**Expected:** Response with troubleshooting guide from `troubleshooting.md`

---

### Scenario 3: AWS Setup Query
**Input:** "How do I set up AWS credentials?"

**Expected:** Response with AWS setup instructions from `aws-setup.md`

---

### Scenario 4: General Help
**Input:** "What can you help me with?"

**Expected:** List of available topics and capabilities

---

## 📊 Success Checklist

Before presenting/demoing, verify:

- [ ] Backend health check returns 200 OK
- [ ] Frontend loads at http://localhost:5173
- [ ] Chat interface is visible
- [ ] Can send a message and receive response
- [ ] Documentation search returns relevant snippets
- [ ] No console errors in browser (F12)
- [ ] Both terminals show servers running
- [ ] Git repository has all commits

---

## 🚀 Quick Commands Reference

```powershell
# Backend (Terminal 1)
cd d:\Infra-Chat\backend
python app_minimal.py

# Frontend (Terminal 2)
cd d:\Infra-Chat\frontend
npm run dev

# Test health
Invoke-RestMethod http://localhost:5000/api/health

# View in browser
start http://localhost:5173
```

---

## 🎥 Demo Script

1. **Show Project Structure:**
   ```powershell
   tree /F d:\Infra-Chat
   ```

2. **Start Backend:**
   - Show terminal with server running
   - Test health endpoint

3. **Start Frontend:**
   - Open browser to http://localhost:5173
   - Show clean UI

4. **Demo Chat:**
   - Type: "How do I deploy to AWS?"
   - Show response appears
   - Highlight documentation snippets

5. **Show Code:**
   - Open `app_minimal.py` - show Flask endpoints
   - Open `ChatWindow.tsx` - show React component
   - Open `docs_index.json` - show indexed documents

6. **Show Documentation:**
   - Open `README.md` - show architecture
   - Open `PYTHON313_NOTES.md` - explain tech choices

---

## 💡 Tips for Presentation

**Talking Points:**
1. "Full-stack application with React + Flask"
2. "Document search using keyword matching"
3. "RESTful API design"
4. "Responsive chat interface"
5. "Built with production-ready patterns"

**If Asked About:**
- **AI Features:** "Used minimal mode for Python 3.13 compatibility, can upgrade to full AI with Python 3.11"
- **Scalability:** "Can add vector embeddings, Redis caching, load balancers"
- **Security:** "Environment variables for keys, CORS configured, input validation"

---

## 📝 Additional Resources

- **Architecture:** See `README.md`
- **Setup:** See `SETUP.md`
- **Demo:** See `DEMO.md`
- **Python 3.13:** See `PYTHON313_NOTES.md`
- **Deployment:** See `DEPLOYMENT.md`

---

**Need help?** Check the documentation files or open an issue on GitHub!

**Ready to start?** Run the commands above and you'll be chatting in 5 minutes! 🚀
