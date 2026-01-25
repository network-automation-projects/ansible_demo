# Python Deployment Orchestrator Dockerfile
# Demonstrates venv isolation and requirements.txt usage

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python3 -m venv /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY deployctl/ /app/deployctl/
COPY config/ /app/config/
COPY setup.py /app/

# Install application in virtual environment
RUN /app/.venv/bin/pip install -e .

# Make venv Python available in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set Python path
ENV PYTHONPATH="/app"

# Default command
ENTRYPOINT ["deployctl"]
