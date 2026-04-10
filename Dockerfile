# Multi-stage build for smaller final image
FROM python:3.12-slim AS builder

# Install build dependencies
# NOTE: libgl1-mesa-glx was renamed to libgl1 in Debian Trixie (python:3.12-slim base)
#       tesseract-ocr ? OCR engine called via subprocess by image_parser.py
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

# Runtime dependencies only
# libgl1 (renamed from libgl1-mesa-glx in Debian Trixie) ? opencv headless shared-library
# libglib2.0-0  ? also required by opencv
# tesseract-ocr ? called at runtime via subprocess in image_parser.py
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/uploads && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Environment variables
ENV DEBUG=False
ENV PORT=5000
ENV FLASK_APP=main.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "main:app"]