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


def resize_image(image, max_width=1000, max_height=1000):
    """Function to resize image for improving image processing"""
    # Get current size
    h, w = image.shape[:2]

    # Compute scaling factor, preserve aspect ratio
    scale = min(max_width / w, max_height / h, 1.0)  # don't upscale!
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return image


def get_ocr_text(texts: list) -> str:
    """Function to validate whether the text from the image is engine number
    """

    # NOTE: This is a temporary validation, will be modified for actual implementation
    ocr_text = [text for text in texts if (len(text) > 7)][0]

    return ocr_text


def scan_engine_number(image_bytes: bytes) -> str:
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

    # NOTE: image preprocessing
    # Resize image
    image = resize_image(image=image)

    # Check whether the image can be read by opencv
    if not isinstance(image, np.ndarray):
        raise ValueError("Invalid or unreadable image format")

    try:
    # Get the paddle ocr results if there are any 
        ocr_results = ocr_engine.predict(image)
        if ocr_results:
            # Get engine number from detected texts
            ocr_text = get_ocr_text(texts=ocr_results[0]["rec_texts"])

            return ocr_text
        else:
            return ""
    # Exception to handle unexpected behaviour from Paddle OCR
    except Exception as e:
        raise RuntimeError(f"Paddle OCR error: {e}") from e
