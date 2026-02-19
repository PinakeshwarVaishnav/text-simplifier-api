# Use a lightweight Python base image
FROM python:3.12.3-slim

# Install Tesseract OCR and its dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user to avoid permission issues
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR $HOME/app

# Copy and install Python requirements
# Use --chown=user to ensure the new user owns the files
COPY --chown=user . .
RUN pip install --no-cache-dir -r requirements.txt

# Start your FastAPI app on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
