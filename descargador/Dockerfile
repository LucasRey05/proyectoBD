# Backend para Cloud Run: Python + ffmpeg (yt-dlp lo necesita para unir y convertir).
FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run inyecta el puerto en PORT.
CMD exec gunicorn --bind ":${PORT:-8080}" --workers 1 --threads 4 --timeout 300 app:app
