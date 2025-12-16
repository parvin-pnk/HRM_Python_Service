import io
from pdfminer.high_level import extract_text_to_fp
from docx import Document

def extract_raw_text(file_bytes: bytes, ext: str) -> str:
    if ext == "pdf":
        output = io.BytesIO()
        extract_text_to_fp(io.BytesIO(file_bytes), output)
        return output.getvalue().decode("utf-8", errors="ignore")

    if ext == "docx":
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported format")
