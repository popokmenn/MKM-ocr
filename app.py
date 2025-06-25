import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from services import scan_engine_number



# Create logging instance
logger = logging.getLogger(__name__)


# Create fast api instance
app = FastAPI(
    title="OCR Barcode API",
    version="0.1.0",
    description="Extract text from image using PaddleOCR, generate barcode, and store images."
)



# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# The main API services
@app.post("/v1/scan-image/", status_code=201)
async def scan_and_generate(file: UploadFile=File(...)):
    """API Router to scan image by its file and generate the Barcode
    """

    # Checking the file type. File must be jpeg or png
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {file.content_type}")

    # Exception if the below code causing error
    try:
        # Read image bytes
        image_bytes = await file.read()

        # Scanned the image
        ocr_texts = scan_engine_number(image_bytes=image_bytes)

        return {"ocr_texts": ocr_texts}

    except ValueError as e:
        logger.error(f"Image Processing Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurs when processing image"
        )
    except RuntimeError as e:
        logger.error(f"Processing Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="an error occurs when processing image"
        )
