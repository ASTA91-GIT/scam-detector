import os
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from docx import Document
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, user_id):
    filename = secure_filename(file.filename)
    upload_dir = os.path.join("uploads", str(user_id))
    os.makedirs(upload_dir, exist_ok=True)

    path = os.path.join(upload_dir, filename)
    file.save(path)
    return path, filename


def extract_text_from_file(path, ext):
    ext = ext.lower()

    if ext in ["png", "jpg", "jpeg"]:
        return pytesseract.image_to_string(Image.open(path))

    if ext == "pdf":
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()

        if not text.strip():
            for page in doc:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img)

        return text

    if ext in ["doc", "docx"]:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == "txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    raise ValueError("Unsupported file format")
