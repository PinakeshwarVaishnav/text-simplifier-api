import pytesseract
from PIL import Image
import os


def extract_text(filepath: str) -> str:
    """
    Opens the image and runs Tesseract OCR.
    Returns stripped text or raises a descriptive exception.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image file not found: {filepath}")

    try:
        image = Image.open(filepath)

        # Convert to RGB to handle PNGs with transparency (RGBA mode breaks Tesseract)
        image = image.convert("RGB")

        text = pytesseract.image_to_string(image)
        return text.strip()

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError("Tesseract is not installed or not in PATH. ")
    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {str(e)}")
