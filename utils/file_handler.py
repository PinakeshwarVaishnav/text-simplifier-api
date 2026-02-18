import os
import uuid

from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException

load_dotenv()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_FILE_SIZE = (
    int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024
)  # Convert MB to bytes
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


def validate_file(file: UploadFile) -> None:
    """Validates content type. Raises HTTPException if invalid."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only JPG and PNG are allowed.",
        )


async def save_upload(file: UploadFile) -> str:
    """
    Reads file content, checks size, saves to disk with a UUID filename.
    Returns the saved file path.
    """
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {os.getenv('MAX_FILE_SIZE_MB', 5)}MB.",
        )

    # Use UUID to avoid filename collisions and path traversal attacks
    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(filepath, "wb") as f:
        f.write(contents)

    return filepath


def delete_file(filepath: str) -> None:
    """Deletes temp file after processing. Called in a finally block."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass  # Non-critical, don't crash the response
