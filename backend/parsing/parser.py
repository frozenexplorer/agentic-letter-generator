import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(filepath: str) -> str:
    """Extracts full text from a PDF."""
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(filepath: str) -> str:
    """Extracts full text from a DOCX Word document."""
    doc = Document(filepath)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)

def extract_all_from_folder(folder_path: str, file_type: str = "pdf") -> dict:
    """Extracts text from all files of a given type in a folder."""
    output = {}
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if file_type == "pdf" and filename.endswith(".pdf"):
            output[filename] = extract_text_from_pdf(full_path)
        elif file_type == "docx" and filename.endswith(".docx"):
            output[filename] = extract_text_from_docx(full_path)
    return output
