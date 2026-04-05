FROM python:3.11-slim

# Fix 1: System deps + Tesseract PATH
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    tesseract-ocr \
    poppler-utils \
    ghostscript \
    pandoc \
    curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* 

ENV TESSERACT_CMD=/usr/bin/tesseract
ENV PANDOC_PATH=/usr/bin/pandoc

WORKDIR /app

# Fix 2: Optimized pip install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Fix 3: Render port + Healthcheck
EXPOSE 10000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Fix 4: Background services + API
CMD sh -c "redis-server --daemonize yes --port 6379 --bind 0.0.0.0 && \
           celery -A app.tasks worker --loglevel=info --detach && \
           uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload"
