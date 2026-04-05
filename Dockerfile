FROM python:3.11-slim

# System dependencies (Pandoc PRE-INSTALLED)
RUN apt-get update && apt-get install -y 
    poppler-utils \
    ghostscript \
    pandoc \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps (NO pandoc package)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Render port
EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 
