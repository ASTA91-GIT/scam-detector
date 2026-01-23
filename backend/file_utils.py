"""
File Upload and Text Extraction Utilities
"""
import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting DOCX text: {str(e)}")

def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting TXT text: {str(e)}")

def extract_text_from_file(file_path, file_extension):
    """Extract text from uploaded file based on extension"""
    ext = file_extension.lower()
    
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ['doc', 'docx']:
        return extract_text_from_docx(file_path)
    elif ext == 'txt':
        return extract_text_from_txt(file_path)
    else:
        raise Exception(f"Unsupported file type: {ext}")

def save_uploaded_file(file, user_id):
    """Save uploaded file and return file path"""
    if not allowed_file(file.filename):
        raise Exception("File type not allowed")
    
    filename = secure_filename(file.filename)
    # Add user_id prefix to avoid conflicts
    filename = f"{user_id}_{filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    file.save(file_path)
    return file_path, filename
