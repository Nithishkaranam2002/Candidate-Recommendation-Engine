import pdfplumber
from docx import Document
from utils.text_processing import clean_text

def parse_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)

def parse_docx(file):
    doc = Document(file)
    return clean_text("\n".join([p.text for p in doc.paragraphs]))

def parse_txt(file):
    return clean_text(file.read().decode("utf-8"))
