import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from services.ocr_service import extract_text
from services.paraphrase_service import paraphrase_text
from utils.file_handler import validate_file, save_upload, delete_file

# -------------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# App initialization
# -------------------------------------------------------------------
app = FastAPI(
    title="Text Simplifier API",
    description="Upload an image, extract text via Tesseract OCR, get it paraphrased by AI.",
    version="1.0.0",
)

# CORS — allows the frontend to call the API from a browser
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Serve frontend — only if static folder exists
import os

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------------------------------------------
# Request logging middleware
# -------------------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    logger.info(f"Response: {response.status_code} | Duration {duration}s")
    return response


# -------------------------------------------------------------------
# Health check endpoint
# -------------------------------------------------------------------
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Text Simplifier API is running"}


# -------------------------------------------------------------------
# Main endpoint
# -------------------------------------------------------------------


@app.post("/api/process", tags=["Core"])
async def process_image(image: UploadFile = File(...)):
    """
    Accepts an image upload, extracts text via OCR, returns paraphrased text.
    """
    start_time = time.time()
    filepath = None  # Track this so we can delete it in the finally block

    # Step 1: Validate file type
    validate_file(image)

    try:
        # Step 2: Save file temporarily to disk
        filepath = await save_upload(image)
        logger.info(f"File saved temporarily: {filepath}")

        # Step 3: Run OCR
        original_text = extract_text(filepath)
        logger.info(f"OCR extracted {len(original_text)} characters")

        if not original_text:
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": "No text could be extracted from the image. "
                    "Ensure the image contains clear, readable text.",
                },
            )

        # Step 4: Paraphrase via AI API
        paraphrased = paraphrase_text(original_text)
        logger.info("Paraphrasing complete")

        processing_time = f"{round(time.time() - start_time, 2)}s"

        return {
            "success": True,
            "original_text": original_text,
            "paraphrased_text": paraphrased,
            "processing_time": processing_time,
        }

    except ValueError as e:
        return JSONResponse(
            status_code=400, content={"success": False, "error": str(e)}
        )

    except RuntimeError as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "An unexpected error occurred."},
        )

    finally:
        # Always clean up the temp file, even if something fails
        if filepath:
            delete_file(filepath)
            logger.info(f"Cleaned up temp file: {filepath}")
