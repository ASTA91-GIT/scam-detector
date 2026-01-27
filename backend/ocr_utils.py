# backend/ocr_utils.py
import pytesseract
import cv2
import numpy as np
from PIL import Image
import os

# ===============================
# CONFIGURE TESSERACT PATHS
# ===============================

# 🔴 CHANGE ONLY IF YOUR PATH IS DIFFERENT
pytesseract.pytesseract.tesseract_cmd = r"D:\SOFTWARES\tesseract.exe"

# Tell Tesseract where trained data lives
os.environ["TESSDATA_PREFIX"] = r"D:\SOFTWARES\tessdata"

# ===============================
# IMAGE PREPROCESSING
# ===============================

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image for OCR")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    gray = cv2.medianBlur(gray, 3)

    # Adaptive threshold for better OCR
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return thresh


# ===============================
# OCR FUNCTION
# ===============================

def extract_text_from_image(image_path):
    processed = preprocess_image(image_path)

    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(processed, lang="eng", config=config)

    return text.strip()
