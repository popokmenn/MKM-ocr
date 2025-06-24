import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
from dotenv import load_dotenv; load_dotenv()



REC_MODEL_DIR = os.environ.get("REC_MODEL_DIR")
DET_MODEL_DIR = os.environ.get("DET_MODEL_DIR")


# OCR engine object instantiation
ocr_engine = PaddleOCR(
    text_detection_model_dir=DET_MODEL_DIR,
    text_recognition_model_dir=REC_MODEL_DIR,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


def scan_engine_number(image_bytes: bytes) -> list[str]:
    """Function to use Paddle OCR to text in image

    Parameters
    ----------
    image_bytes: image in the form of bytes

    Return
    ------
    ocr_result: list of texts from ocr
    """

    # Read image as bytes and transform to cv2 RGB COLOR
    image = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # NOTE: add preprocessing on the code below if needed

    # Check whether the image can be read by opencv
    if not isinstance(image, np.ndarray):
        raise ValueError("Invalid or unreadable image format")

    try:
    # Get the paddle ocr results if 
        ocr_results = ocr_engine.predict(image)
        if ocr_results:
            return ocr_results[0]["rec_texts"]
        else:
            return []
    # Exception to handle unexpected behaviour from Paddle OCR
    except Exception as e:
        raise RuntimeError(f"Paddle OCR error: {e}") from e
