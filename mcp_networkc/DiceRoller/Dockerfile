FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dice_server.py .

ENTRYPOINT ["python", "dice_server.py"]

