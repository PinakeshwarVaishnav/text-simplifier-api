# Use a lightweight Python base image
FROM python:3.12.3-slim

# Install Tesseract OCR and its dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python requirements
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Start your FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]