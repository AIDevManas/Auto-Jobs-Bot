import pdfplumber as pdfp
import re


def extract_text_from_pdf(file_path):
    with pdfp.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", text).lower()

    return cleaned_text
