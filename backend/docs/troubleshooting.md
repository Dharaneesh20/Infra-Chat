# Troubleshooting Guide

## Common Issues and Solutions

### Application Issues

#### 1. Application Won't Start

**Symptoms:**
- Server fails to start
- Port already in use error
- Module not found errors

**Solutions:**

**Check if port is already in use:**
```bash
# Windows
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <process_id> /F

# Linux/Mac
lsof -i :5000
kill -9 <pid>
```

**Missing dependencies:**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

**Environment variables not set:**
```bash
# Check if .env exists
cat .env

# Copy from example if needed
cp .env.example .env
```

#### 2. Database Connection Failed

**Symptoms:**
- "Connection refused" errors
- Timeout errors
- Authentication failed

**Solutions:**

**Verify database is running:**
```bash
# PostgreSQL
pg_isready -h localhost -p 5432

# MySQL
mysqladmin ping -h localhost

# Check Docker container
docker ps | grep postgres
```

**Check connection string:**
```bash
# Format: postgresql://user:password@host:port/database
echo $DATABASE_URL
```

**Test connection manually:**
```bash
# PostgreSQL
psql -h localhost -U myuser -d mydb

# MySQL
mysql -h localhost -u myuser -p mydb
```

#### 3. API Returns 500 Errors

**Symptoms:**
- Internal server error
- No detailed error message
- Stack traces in logs

**Solutions:**

**Check application logs:**
```bash
# Flask
tail -f app.log

# Docker
docker logs -f container_name

# PM2
pm2 logs
```

**Common causes:**
- Unhandled exceptions
- Database query errors
- Missing environment variables
- Insufficient permissions

**Enable debug mode:**
```python
# Flask
app.run(debug=True)
```

### AI/LLM Issues

#### 4. Gemini API Errors

**Symptoms:**
- "API key not valid" error
- Rate limit exceeded
- Quota exceeded

**Solutions:**

**Verify API key:**
```bash
# Check if key is set
echo $GOOGLE_API_KEY

# Test the key
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$GOOGLE_API_KEY"
```

**Rate limiting:**
- Wait before retrying
- Implement exponential backoff
- Consider upgrading API tier

**Quota exceeded:**
- Check usage in [Google AI Studio](https://makersuite.google.com/)
- Request quota increase
- Implement caching to reduce calls

#### 5. Vector Search Not Working

**Symptoms:**
- "No relevant documents found"
- ChromaDB errors
- Slow search performance

**Solutions:**

**Re-run ingestion:**
```bash
cd backend
python ingest.py
```

**Check ChromaDB:**
```python
# In Python console
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Check number of documents
print(vectorstore._collection.count())
```

**Performance issues:**
- Increase chunk size
- Add more relevant documents
- Adjust similarity threshold

### Cloud Integration Issues

#### 6. AWS Boto3 Errors

**Symptoms:**
- "No credentials found"
- "Access Denied" errors
- Region errors

**Solutions:**

**Configure credentials:**
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Or use AWS CLI
aws configure
```

**Verify IAM permissions:**
```bash
# Test EC2 access
aws ec2 describe-instances

# Test S3 access
aws s3 ls
```

**Common IAM policies needed:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "s3:List*",
        "s3:Get*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Frontend Issues

#### 7. CORS Errors

**Symptoms:**
- "Access to fetch blocked by CORS policy"
- Network errors in browser console

**Solutions:**

**Backend (Flask):**
```python
from flask_cors import CORS
CORS(app)
```

**Check backend is running:**
```bash
# Should return JSON
curl http://localhost:5000/api/health
```

**Verify frontend API URL:**
```typescript
// Should point to backend
const API_URL = 'http://localhost:5000';
```

#### 8. React Build Fails

**Symptoms:**
- TypeScript errors
- Module not found
- Out of memory errors

**Solutions:**

**Clear cache:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Increase memory:**
```bash
# Linux/Mac
export NODE_OPTIONS="--max-old-space-size=4096"

# Windows
set NODE_OPTIONS=--max-old-space-size=4096

npm run build
```

**Check TypeScript errors:**
```bash
npm run type-check
```

### Performance Issues

#### 9. Slow Response Times

**Symptoms:**
- API takes > 5 seconds
- Frontend feels sluggish
- High CPU usage

**Solutions:**

**Profile the application:**
```python
# Add timing
import time
start = time.time()
# ... your code ...
print(f"Took {time.time() - start:.2f}s")
```

**Optimize database queries:**
- Add indexes
- Use connection pooling
- Cache frequent queries

**Implement caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(param):
    # ...
```

#### 10. High Memory Usage

**Symptoms:**
- Application crashes
- Out of memory errors
- Slow performance

**Solutions:**

**Monitor memory:**
```bash
# Check Python process
ps aux | grep python

# Docker container
docker stats container_name
```

**Common causes:**
- Large file uploads
- Memory leaks
- Too many cached embeddings

**Solutions:**
- Implement pagination
- Clear caches periodically
- Use streaming for large responses

## Getting Help

### Debug Checklist
1. ✅ Check logs for errors
2. ✅ Verify environment variables
3. ✅ Test each component individually
4. ✅ Check network connectivity
5. ✅ Review recent changes

### Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LangChain Docs](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [AWS Boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Contact
- **Slack**: #infra-chat-support
- **Email**: support@example.com
- **GitHub Issues**: [Create an issue](https://github.com/yourorg/infra-chat/issues)
