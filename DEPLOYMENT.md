# 🚀 Ultimate MCP System - Deployment Guide

## 📋 Deployment Options

### Option 1: Docker (Recommended)

**Best for**: Production deployment, consistent environments

#### Quick Start
```bash
# Clone repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Build and start all servers
docker-compose up -d

# Check status
docker-compose ps
```

#### Access URLs
- Master Orchestrator: http://localhost:7860
- N8N Automation: http://localhost:7862
- Agent Builder: http://localhost:7863
- Local Control: http://localhost:7864
- N8N Instance: http://localhost:5678 (admin/admin)

#### Stop Services
```bash
docker-compose down
```

#### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f orchestrator
docker-compose logs -f agent-builder
```

---

### Option 2: Google Cloud Run

**Best for**: Serverless deployment, auto-scaling

#### Prerequisites
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Single Service Deployment
```bash
# Deploy Master Orchestrator
gcloud run deploy ultimate-mcp-orchestrator \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key

# Deploy Agent Builder
gcloud run deploy ultimate-mcp-agent-builder \
  --source ./backend/mcp_servers/agent_builder \
  --region us-central1 \
  --allow-unauthenticated
```

#### Multi-Service with Cloud Run (separate services)
```bash
# Create services.yaml
# See docs/deployment/cloudrun-services.yaml

gcloud run services replace services.yaml
```

#### Considerations
- ⚠️ Each MCP server needs separate Cloud Run service
- ⚠️ Additional cost for multiple services
- ✅ Auto-scaling per service
- ✅ Built-in HTTPS

---

### Option 3: Railway

**Best for**: Easy deployment, free tier, GitHub integration

#### Steps
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Configure services:
   ```
   Service 1: Master Orchestrator
   Start Command: python backend/main.py
   Port: 7860
   
   Service 2: N8N MCP
   Start Command: python backend/mcp_servers/n8n_automation/server.py
   Port: 7862
   
   (Repeat for other MCPs)
   ```
5. Add environment variables in Railway dashboard
6. Deploy

#### Railway Configuration File
Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "startCommand": "python launch_all_servers.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

### Option 4: Render

**Best for**: Free tier, easy setup, automatic deploys

#### Steps
1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect GitHub repository
4. Configure:
   ```
   Name: ultimate-mcp-system
   Environment: Python 3.11
   Build Command: pip install -r backend/requirements.txt && playwright install chromium
   Start Command: python launch_all_servers.py
   ```
5. Add environment variables
6. Deploy

#### render.yaml
```yaml
services:
  - type: web
    name: mcp-orchestrator
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: python backend/main.py
    envVars:
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: PORT
        value: 7860
  
  - type: web
    name: mcp-agent-builder
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: python backend/mcp_servers/agent_builder/server.py
    envVars:
      - key: PORT
        value: 7863
```

---

### Option 5: AWS EC2 (Self-Hosted)

**Best for**: Full control, custom configuration

#### Launch EC2 Instance
```bash
# Amazon Linux 2 or Ubuntu 22.04
# Instance type: t3.medium (minimum)
# Security Group: Open ports 7860-7864, 22 (SSH)
```

#### Setup Script
```bash
#!/bin/bash

# Update system
sudo yum update -y  # Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Python 3.11
sudo yum install python3.11 -y
# OR
sudo apt install python3.11 python3.11-venv -y

# Install Git
sudo yum install git -y
# OR
sudo apt install git -y

# Clone repository
git clone https://github.com/W3JDev/ultimate-mcp-system.git
cd ultimate-mcp-system

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
playwright install chromium
playwright install-deps chromium

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Install as systemd service
sudo cp deployment/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-orchestrator
sudo systemctl enable mcp-agent-builder
sudo systemctl enable mcp-n8n
sudo systemctl enable mcp-local-control
sudo systemctl start mcp-orchestrator
sudo systemctl start mcp-agent-builder
sudo systemctl start mcp-n8n
sudo systemctl start mcp-local-control

# Check status
sudo systemctl status mcp-*
```

#### Systemd Service Example
Create `/etc/systemd/system/mcp-orchestrator.service`:
```ini
[Unit]
Description=MCP Master Orchestrator
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/ultimate-mcp-system
Environment="PATH=/home/ec2-user/ultimate-mcp-system/venv/bin"
EnvironmentFile=/home/ec2-user/ultimate-mcp-system/.env
ExecStart=/home/ec2-user/ultimate-mcp-system/venv/bin/python backend/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Nginx Reverse Proxy
```nginx
# /etc/nginx/conf.d/mcp.conf

server {
    listen 80;
    server_name your-domain.com;

    # Master Orchestrator
    location / {
        proxy_pass http://localhost:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # N8N MCP
    location /n8n/ {
        proxy_pass http://localhost:7862/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }

    # Agent Builder
    location /agents/ {
        proxy_pass http://localhost:7863/;
    }

    # Local Control
    location /control/ {
        proxy_pass http://localhost:7864/;
    }
}
```

#### SSL with Let's Encrypt
```bash
# Install Certbot
sudo yum install certbot python3-certbot-nginx -y
# OR
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

### Option 6: DigitalOcean App Platform

**Best for**: Managed deployment, scalable

#### Steps
1. Create new App in DigitalOcean
2. Connect GitHub repository
3. Configure components:
   ```
   Component: orchestrator
   Source Directory: /
   Build Command: pip install -r backend/requirements.txt
   Run Command: python backend/main.py
   HTTP Port: 7860
   
   (Add more components for other MCPs)
   ```
4. Set environment variables
5. Deploy

---

### Option 7: Kubernetes (Advanced)

**Best for**: Large-scale, multi-environment deployments

#### Prerequisites
```bash
# Install kubectl, helm
# Have Kubernetes cluster ready (EKS, GKE, AKS, or local minikube)
```

#### Deploy
```bash
# Apply Kubernetes manifests
kubectl apply -f deployment/k8s/

# Check deployment
kubectl get pods -n mcp-system
kubectl get services -n mcp-system

# Access via LoadBalancer
kubectl get service mcp-orchestrator -n mcp-system
```

#### Helm Chart
```bash
# Install via Helm
helm repo add ultimate-mcp https://charts.ultimate-mcp.dev
helm install mcp ultimate-mcp/ultimate-mcp-system \
  --set orchestrator.apiKey=your_key \
  --set agentBuilder.enabled=true
```

---

## 🔒 Security Checklist

### Before Production Deployment

- [ ] Change default passwords (N8N, databases)
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules (only necessary ports)
- [ ] Use secrets manager for API keys (AWS Secrets Manager, GCP Secret Manager)
- [ ] Enable authentication (add auth layer)
- [ ] Set up monitoring (Prometheus, Grafana, Datadog)
- [ ] Configure log aggregation (ELK, CloudWatch, Papertrail)
- [ ] Enable rate limiting
- [ ] Set up backups (agent configs, workflows)
- [ ] Configure CORS properly
- [ ] Add request validation
- [ ] Enable audit logging

---

## 📊 Monitoring & Observability

### Health Checks

```bash
# Check all services
curl http://localhost:7860/health
curl http://localhost:7862/health
curl http://localhost:7863/health
curl http://localhost:7864/health
```

### Prometheus Metrics
```yaml
# Add to docker-compose.yml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Grafana Dashboard
```yaml
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🚨 Troubleshooting

### Issue: Containers won't start
```bash
# Check logs
docker-compose logs

# Check resource usage
docker stats

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Issue: Port conflicts
```bash
# Check what's using ports
netstat -tuln | grep 786

# Kill process
kill -9 $(lsof -t -i:7860)

# Change ports in docker-compose.yml
```

### Issue: Out of memory
```bash
# Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory → 8GB+

# Or in docker-compose.yml
services:
  orchestrator:
    mem_limit: 2g
    mem_reservation: 1g
```

---

## 📞 Support

- **Documentation**: [Full docs](../docs/)
- **Issues**: GitHub Issues
- **Community**: Discord/Slack
- **Email**: support@ultimate-mcp.dev

---

**Last Updated**: November 16, 2025  
**Version**: 1.0.0
