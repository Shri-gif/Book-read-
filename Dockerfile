FROM python:3.11-slim

# Install system dependencies FIRST (faster builds)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    ghostscript \
    pandoc \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Render needs port 10000
EXPOSE 10000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:10000/health || exit 1

CMD ["sh", "-c", "celery -A app.tasks worker --loglevel=info & uvicorn app.main:app --host 0.0.0.0 --port 10000"] 
