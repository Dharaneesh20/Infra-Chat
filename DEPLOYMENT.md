# Deployment Guide for Infra-Chat

## 🚀 Deployment Options

### Option 1: Docker Deployment (Recommended)

#### Dockerfiles

**backend/Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Build application
COPY . .
RUN npm run build

# Production image
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    volumes:
      - ./backend/chroma_db:/app/chroma_db
      - ./backend/docs:/app/docs
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Usage:**
```bash
# Create .env file
cp .env.example .env

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

---

### Option 2: AWS Deployment

#### Using AWS Elastic Beanstalk

**1. Install EB CLI:**
```bash
pip install awsebcli
```

**2. Initialize:**
```bash
cd backend
eb init -p python-3.11 infra-chat-api
```

**3. Create environment:**
```bash
eb create infra-chat-prod
```

**4. Deploy:**
```bash
eb deploy
```

#### Using AWS ECS (Container)

**1. Build and push to ECR:**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t infra-chat-backend ./backend

# Tag
docker tag infra-chat-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/infra-chat-backend:latest

# Push
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/infra-chat-backend:latest
```

**2. Create ECS task definition and service**

---

### Option 3: Heroku Deployment

#### Backend

**1. Create Procfile:**
```
web: python app.py
```

**2. Deploy:**
```bash
heroku create infra-chat-api
heroku config:set GOOGLE_API_KEY=your_key
git subtree push --prefix backend heroku main
```

#### Frontend

**1. Build:**
```bash
npm run build
```

**2. Deploy to Netlify/Vercel:**
```bash
# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod
```

---

### Option 4: Azure Deployment

#### Using Azure App Service

**1. Create App Service:**
```bash
az webapp up --name infra-chat-backend --runtime "PYTHON:3.11"
```

**2. Configure:**
```bash
az webapp config appsettings set --name infra-chat-backend --settings GOOGLE_API_KEY=your_key
```

---

### Option 5: Kubernetes Deployment

#### Kubernetes Manifests

**backend-deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: infra-chat-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: infra-chat-backend
  template:
    metadata:
      labels:
        app: infra-chat-backend
    spec:
      containers:
      - name: backend
        image: your-registry/infra-chat-backend:latest
        ports:
        - containerPort: 5000
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: infra-chat-secrets
              key: google-api-key
---
apiVersion: v1
kind: Service
metadata:
  name: infra-chat-backend
spec:
  selector:
    app: infra-chat-backend
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f backend-deployment.yaml
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Set strong, unique API keys
- [ ] Enable HTTPS/TLS
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for your domain
- [ ] Set up rate limiting
- [ ] Configure proper IAM roles (AWS)
- [ ] Enable logging and monitoring
- [ ] Set up backup strategy
- [ ] Configure firewall rules
- [ ] Use read-only credentials for cloud APIs

---

## 📊 Monitoring

### CloudWatch (AWS)
```bash
# Install CloudWatch agent
pip install boto3 watchtower
```

### Application Insights (Azure)
```bash
pip install applicationinsights
```

### Custom Metrics
```python
# Add to app.py
from prometheus_client import Counter, Histogram

chat_requests = Counter('chat_requests_total', 'Total chat requests')
response_time = Histogram('response_time_seconds', 'Response time')
```

---

## 🔄 CI/CD Example

**GitHub Actions (.github/workflows/deploy.yml):**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "infra-chat-api"
          heroku_email: "your@email.com"
          appdir: "backend"

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build
        run: |
          cd frontend
          npm install
          npm run build
      
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v2.0
        with:
          publish-dir: './frontend/dist'
          production-deploy: true
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---

## 🆘 Troubleshooting Deployment

### Common Issues

**Port already in use:**
```bash
# Change port in app.py or use PORT env variable
export PORT=8080
```

**Out of memory:**
```bash
# Increase container memory
docker run -m 512m ...
```

**SSL certificate errors:**
```bash
# Use Let's Encrypt
certbot --nginx -d yourdomain.com
```

---

## 📈 Scaling Strategy

### Horizontal Scaling
- Use load balancer (ALB, NGINX)
- Multiple backend instances
- Shared vector database (Pinecone)
- Centralized session store (Redis)

### Vertical Scaling
- Increase instance size
- Add more CPU/RAM
- Use faster storage (SSD)

---

**Need help deploying? Check the main README or open an issue!**
