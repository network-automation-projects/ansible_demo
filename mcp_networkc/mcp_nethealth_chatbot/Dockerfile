FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Netmiko
RUN apt-get update && apt-get install -y \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY network_monitor_server.py .

ENTRYPOINT ["python", "network_monitor_server.py"]

