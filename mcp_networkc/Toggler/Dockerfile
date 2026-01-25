FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY toggl_server.py .

ENTRYPOINT ["python", "toggl_server.py"]

