# Agent Builder MCP - Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from root
COPY backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional Gradio dependencies (skip audioop-lts on Python 3.11)
RUN pip install --no-cache-dir \
    aiofiles==24.1.0 \
    brotli \
    ffmpy \
    jinja2 \
    markupsafe \
    orjson \
    pandas \
    python-multipart \
    safehttpx \
    semantic-version \
    tomlkit \
    typer \
    "pydantic<=2.12.4" \
    numpy \
    "Pillow>=10.0,<13.0"

# Install Composio (without problematic dependencies)
RUN pip install --no-cache-dir composio-core --no-deps && \
    pip install --no-cache-dir \
    aiohttp \
    requests \
    jsonschema \
    sentry-sdk \
    pysher \
    importlib-metadata \
    jsonref \
    inflection \
    semver \
    click \
    pyperclip \
    paramiko \
    websocket-client

# Copy application code
COPY backend/ /app/backend/

# Create logs directory
RUN mkdir -p /app/backend/logs

# Expose port
EXPOSE 7863

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7863

# Run the server
CMD ["python", "backend/mcp_servers/agent_builder/server.py"]
