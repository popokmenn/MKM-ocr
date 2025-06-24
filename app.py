from fastapi import FastAPI
from controllers import ocr



app = FastAPI(
    title="OCR Barcode API",
    version="0.1.0",
    description="Extract text from image using PaddleOCR, generate barcode, and store images."
)

# Include OCR router
app.include_router(ocr.router, prefix="/v1", tags=["OCR"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "OK"}
