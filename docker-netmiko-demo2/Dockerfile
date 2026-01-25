FROM python:3.12-slim

WORKDIR /app

COPY backup_config.py .

RUN pip install --no-cache-dir netmiko

CMD ["python", "backup_config.py"]