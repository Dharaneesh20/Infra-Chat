# Quick Setup Guide

Follow these steps to get Infra-Chat running in minutes!

## ⚡ Quick Start (5 minutes)

### 1️⃣ Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Open .env and add your GOOGLE_API_KEY
# Get one free at: https://makersuite.google.com/app/apikey

# Ingest documentation
python ingest.py

# Start the backend
python app.py
```

✅ Backend should now be running on http://localhost:5000

### 2️⃣ Frontend Setup

Open a **new terminal** window:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Start the frontend
npm start
```

✅ Frontend should open automatically at http://localhost:3000

### 3️⃣ Test It Out!

Try these sample queries:
- "Show me the deployment guide"
- "What are the troubleshooting steps?"
- "List my EC2 instances" (requires AWS credentials)

---

## 🔧 Configuration

### Google Gemini API Key (Required)

1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `backend/.env`:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### AWS Credentials (Optional)

To enable cloud queries:

1. Create read-only IAM user in AWS
2. Add to `backend/.env`:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=us-east-1
   ```

---

## 📝 Common Issues

### "Module not found" errors
```powershell
# Backend
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### Backend won't start
- Check if Python 3.9+ is installed: `python --version`
- Make sure virtual environment is activated
- Verify .env file exists with GOOGLE_API_KEY

### Frontend shows connection error
- Ensure backend is running on port 5000
- Check browser console for errors
- Verify VITE_API_URL in frontend/.env

### ChromaDB errors
```powershell
cd backend
python ingest.py
```

---

## 🎯 Next Steps

1. **Add Your Documentation**: Place `.md` or `.txt` files in `backend/docs/`
2. **Re-ingest**: Run `python ingest.py` to update the knowledge base
3. **Customize**: Edit welcome message in `frontend/src/components/ChatWindow.tsx`
4. **Deploy**: See README.md for deployment options

---

## 📞 Need Help?

- Check the full README.md
- Review backend/docs/troubleshooting.md
- Open an issue on GitHub

**Happy Hacking! 🚀**
