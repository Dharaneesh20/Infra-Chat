# Deployment Guide

## Application Deployment Process

### Overview
This document outlines the deployment process for our application across different environments.

## Environments

### Development
- **Purpose**: Feature development and testing
- **URL**: https://dev.myapp.com
- **Branch**: `develop`
- **Auto-deploy**: On every push

### Staging
- **Purpose**: Pre-production testing
- **URL**: https://staging.myapp.com
- **Branch**: `staging`
- **Deploy**: Manual approval required

### Production
- **Purpose**: Live user traffic
- **URL**: https://myapp.com
- **Branch**: `main`
- **Deploy**: Manual approval + automated tests

## Deployment Steps

### 1. Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Database migrations ready
- [ ] Environment variables configured
- [ ] Backup current production data
- [ ] Notify team of deployment window

### 2. Backend Deployment

#### Using Docker
```bash
# Build the image
docker build -t myapp-backend:latest .

# Tag for registry
docker tag myapp-backend:latest registry.example.com/myapp-backend:v1.2.3

# Push to registry
docker push registry.example.com/myapp-backend:v1.2.3

# Deploy to ECS/Kubernetes
kubectl apply -f k8s/deployment.yaml
```

#### Using PM2 (Node.js)
```bash
# Install dependencies
npm install --production

# Start with PM2
pm2 start ecosystem.config.js --env production

# Save PM2 configuration
pm2 save
```

### 3. Frontend Deployment

#### React Application
```bash
# Install dependencies
npm install

# Build production bundle
npm run build

# Deploy to S3 + CloudFront
aws s3 sync build/ s3://myapp-frontend --delete
aws cloudfront create-invalidation --distribution-id XXXXX --paths "/*"
```

### 4. Database Migration

```bash
# Backup database first
pg_dump myapp_prod > backup_$(date +%Y%m%d).sql

# Run migrations
npm run migrate:up

# Verify migration
npm run migrate:status
```

### 5. Post-Deployment Verification

#### Health Checks
```bash
# Check API health
curl https://api.myapp.com/health

# Check frontend
curl https://myapp.com

# Check database connection
psql -h db.example.com -U myapp -c "SELECT 1"
```

#### Smoke Tests
- Login functionality
- Core user workflows
- API response times
- Database queries

## Rollback Procedure

### If deployment fails:

1. **Immediate Rollback**
```bash
# Kubernetes
kubectl rollout undo deployment/myapp-backend

# Docker
docker service update --rollback myapp-backend

# PM2
pm2 reload ecosystem.config.js --env production
```

2. **Database Rollback**
```bash
# Rollback migration
npm run migrate:down

# Restore from backup
psql myapp_prod < backup_20240101.sql
```

3. **Notify Team**
- Post in #deployments channel
- Update status page
- Document incident

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run build
      - name: Deploy
        run: ./deploy.sh production
```

## Monitoring

### Key Metrics
- **Response Time**: < 200ms (p95)
- **Error Rate**: < 0.1%
- **CPU Usage**: < 70%
- **Memory Usage**: < 80%

### Alerts
- High error rate (> 1% for 5 minutes)
- Slow response times (> 500ms for 5 minutes)
- Service down (health check fails)

## Security

### SSL/TLS Configuration
- Use Let's Encrypt for certificates
- Enable HTTPS redirect
- Configure HSTS headers
- Update certificates before expiry

### Secret Management
- Store secrets in AWS Secrets Manager
- Never commit secrets to git
- Rotate secrets quarterly
- Use different secrets per environment

## Troubleshooting

### Common Issues

#### Deployment Stuck
- Check Docker/Kubernetes logs
- Verify resource limits
- Check network connectivity

#### Database Connection Errors
- Verify security groups
- Check connection string
- Confirm database is running

#### High Memory Usage
- Check for memory leaks
- Review application logs
- Scale horizontally if needed

## Emergency Contacts

- **On-call Engineer**: Slack @oncall
- **DevOps Team**: #devops channel
- **Database Admin**: dba@example.com

## Documentation Links
- [Architecture Diagram](https://wiki.example.com/architecture)
- [API Documentation](https://api.myapp.com/docs)
- [Runbook](https://wiki.example.com/runbook)
