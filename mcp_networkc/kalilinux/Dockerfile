FROM kalilinux/kali-rolling:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install security tools and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    nikto \
    sqlmap \
    wpscan \
    dirb \
    exploitdb \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/* && \
    # Ensure nmap binaries are executable and have proper permissions
    chmod +x /usr/bin/nmap && \
    chmod +x /usr/lib/nmap/nmap && \
    # Ensure all nmap-related binaries are executable
    find /usr/lib/nmap -type f -executable -exec chmod +x {} \; 2>/dev/null || true && \
    # Verify nmap installation
    nmap --version || true

# Explicitly set user to root for network tools like nmap
# that require raw socket access. The container itself is isolated,
# so this is acceptable for security testing tools.
USER root

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy server script
COPY security_server.py .

# Set entrypoint
ENTRYPOINT ["python3", "security_server.py"]

