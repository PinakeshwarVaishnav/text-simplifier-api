---
title: FastAPI OCR Backend
sdk: docker
app_port: 7860
---

# Text Simplifier API

A FastAPI backend that extracts text from images using Tesseract OCR (local) and simplifies it using the Groq Cloud API.

## Prerequisites

- Python 3.8+
- Tesseract OCR installed ([installation guide](https://tesseract-ocr.github.io/tessdoc/Installation.html))

## Installation

```bash
git clone https://github.com/PinakeshwarVaishnav/text-simplifier-api.git
cd text-simplifier-api

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your Groq Cloud API key
```

## Running the API

```bash
uvicorn main:app --reload
```

Visit: `http://localhost:8000/docs` for interactive Swagger UI
Frontend: `http://localhost:8000/static/index.html`

## API Endpoints

| Method | Endpoint     | Description            |
| ------ | ------------ | ---------------------- |
| POST   | /api/process | Upload image, get text |
| GET    | /health      | Health check           |

## Example Usage

**cURL:**

```bash
curl -X POST http://localhost:8000/api/process \
  -F "image=@your_image.jpg"
```

**Postman:**

- Method: POST
- URL: `http://localhost:8000/api/process`
- Body: form-data → Key: `image` (type: File) → Value: select your image

## Example Response

```json
{
  "success": true,
  "original_text": "The quick brown fox jumps over the lazy dog.",
  "paraphrased_text": "A fast brown fox leaps over a resting dog.",
  "processing_time": "2.3s"
}
```

## Error Responses

| Scenario         | Status Code | Error Message                   |
| ---------------- | ----------- | ------------------------------- |
| Wrong file type  | 400         | Invalid file type '...'         |
| File too large   | 400         | File too large. Max size is 5MB |
| No text in image | 422         | No text could be extracted...   |
| Bad API key      | 500         | Invalid Groq API key            |
| API timeout      | 500         | Groq server is currently busy   |

## Troubleshooting

**`TesseractNotFoundError`:** Tesseract is not installed or not in PATH. On Windows, uncomment the `tesseract_cmd` line in `ocr_service.py` and point it to your install.

**`AuthenticationError`:** Your Groq API key is incorrect. Double-check your `.env` file.

**Empty text result:** The image may have low contrast, small font, or handwriting. Tesseract works best with clean, printed text on white backgrounds.
