import re, io, os, httpx
from fastapi import HTTPException
from pdfminer.high_level import extract_text_to_fp
from docx import Document
from common.logging_util import log

def _pdf_to_text(content: bytes) -> str:
    output = io.StringIO()
    extract_text_to_fp(io.BytesIO(content), output)
    return output.getvalue()

def _docx_to_text(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_url(file_url: str) -> str:
    modified_url = file_url

    if "drive.google.com" in file_url and "/view" in file_url:
        file_id = re.search(r"/d/([^/]+)", file_url).group(1)
        modified_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    if "github.com" in file_url and "/blob/" in file_url:
        modified_url = (
            file_url.replace("github.com", "raw.githubusercontent.com")
            .replace("/blob/", "/")
        )

    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(modified_url)
            response.raise_for_status()
            content = response.content
    except Exception as e:
        raise HTTPException(400, f"Failed to download resume: {e}")

    ext = os.path.splitext(modified_url)[1].lower()
    if ext == ".pdf":
        return _pdf_to_text(content)
    if ext == ".docx":
        return _docx_to_text(content)

    return content.decode("utf-8", errors="ignore")
