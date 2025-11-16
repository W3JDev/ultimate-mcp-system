# Dockerfile for Ultimate MCP System
# Multi-stage build for production deployment

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (for Local Control MCP)
RUN playwright install chromium && \
    playwright install-deps chromium

# Copy application code
COPY backend/ ./backend/
COPY .env.example ./.env

# Create logs directory
RUN mkdir -p backend/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose ports for all 4 MCP servers
EXPOSE 7860 7862 7863 7864

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Default command - starts all servers via launcher
CMD ["python", "launch_all_servers.py"]
