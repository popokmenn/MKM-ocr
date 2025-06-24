from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import ocr



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

# Include OCR router
app.include_router(ocr.router, prefix="/v1", tags=["OCR"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "OK"}
