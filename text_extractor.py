import pdfplumber as pdfp
import re


def extract_text_from_pdf(file_path):
    with pdfp.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    text = re.sub(r"[^\w\s\+\.\-@,/]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text
