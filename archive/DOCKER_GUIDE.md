# 🐳 Docker Deployment Guide

## Quick Start (Agent Builder MCP)

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop/))
- `.env` file configured (copy from `.env.example`)

### 1. Start Agent Builder in Docker

```powershell
# Navigate to agent builder directory
cd backend/mcp_servers/agent_builder

# Start the container (detached mode - runs in background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

**Access the UI**: Open `http://localhost:7863` in your browser

### 2. Development Mode (Auto-reload on code changes)

The default `docker-compose.yml` mounts your code as a volume, so changes are reflected immediately:

```powershell
# Start with live code reload
docker-compose up -d

# Watch logs in real-time
docker-compose logs -f agent-builder

# Restart after major changes
docker-compose restart
```

### 3. Production Mode (Immutable container)

For production, comment out the volume mount in `docker-compose.yml`:

```yaml
# volumes:
#   - ./logs:/app/backend/logs
#   # - ../../..:/app  # COMMENT THIS LINE FOR PRODUCTION
```

Then rebuild:

```powershell
docker-compose build --no-cache
docker-compose up -d
```

## Docker Commands Cheat Sheet

```powershell
# Build and start
docker-compose up -d --build

# View running containers
docker ps

# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f agent-builder

# Execute command in running container
docker-compose exec agent-builder python --version

# Restart specific service
docker-compose restart agent-builder

# Check resource usage
docker stats

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a
```

## Troubleshooting

### Container won't start
```powershell
# Check logs for errors
docker-compose logs agent-builder

# Inspect container
docker inspect agent-builder-mcp

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Port already in use
```powershell
# Find process using port 7863
Get-Process | Where-Object {$_.ProcessName -eq 'python'}

# Stop conflicting process
Stop-Process -Name python -Force

# Or change port in docker-compose.yml
ports:
  - "8863:7863"  # Host:Container
```

### Environment variables not loading
```powershell
# Verify .env file exists
ls .env

# Check if docker-compose sees variables
docker-compose config

# Pass variables explicitly
docker-compose up -d --env-file ../../.env
```

### Permission issues (Linux/Mac)
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Run with sudo if needed
sudo docker-compose up -d
```

## Multi-Server Deployment

To run all MCP servers (Agent Builder, N8N Automation, Local Control):

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  orchestrator:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "7860:7860"
    env_file:
      - .env
    networks:
      - mcp-network

  agent-builder:
    build:
      context: .
      dockerfile: backend/mcp_servers/agent_builder/Dockerfile
    ports:
      - "7863:7863"
    env_file:
      - .env
    networks:
      - mcp-network

  n8n-automation:
    build:
      context: .
      dockerfile: backend/mcp_servers/n8n_automation/Dockerfile
    ports:
      - "7862:7862"
    env_file:
      - .env
    networks:
      - mcp-network

  local-control:
    build:
      context: .
      dockerfile: backend/mcp_servers/local_control/Dockerfile
    ports:
      - "7864:7864"
    env_file:
      - .env
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

Then:
```powershell
docker-compose up -d
```

## Cloud Deployment (GCP Cloud Run)

```powershell
# Build for Cloud Run
gcloud builds submit --tag gcr.io/stellar-state-471406-f8/agent-builder

# Deploy
gcloud run deploy agent-builder \
  --image gcr.io/stellar-state-471406-f8/agent-builder \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars COMPOSIO_API_KEY=$COMPOSIO_API_KEY,GEMINI_API_KEY=$GEMINI_API_KEY
```

## Health Checks

Add to `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:7863"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Security Best Practices

1. **Never commit `.env`** - Already in `.gitignore`
2. **Use Docker secrets** for production:
   ```yaml
   secrets:
     composio_key:
       external: true
   ```
3. **Scan images** for vulnerabilities:
   ```powershell
   docker scan agent-builder-mcp
   ```
4. **Use non-root user** in Dockerfile (add after dependencies):
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

## Backup & Restore

```powershell
# Backup logs
docker cp agent-builder-mcp:/app/backend/logs ./backup-logs

# Backup entire container
docker export agent-builder-mcp > agent-builder-backup.tar

# Restore from backup
docker import agent-builder-backup.tar agent-builder:restored
```

## Performance Optimization

```yaml
# Add to docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

## Next Steps

- ✅ Agent Builder running in Docker
- 🔄 Add remaining MCP servers
- 🚀 Deploy to Cloud Run
- 📊 Set up monitoring (Grafana/Prometheus)
- 🔒 Implement proper secret management
