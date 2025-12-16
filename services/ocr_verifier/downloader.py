import re, os, httpx
from fastapi import HTTPException

def download_document(url: str):
    modified_url = url

    if "drive.google.com" in url and "/view" in url:
        file_id = re.search(r"/d/([^/]+)", url).group(1)
        modified_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    if "github.com" in url and "/blob/" in url:
        modified_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(modified_url)
            response.raise_for_status()
    except Exception:
        raise HTTPException(400, "Failed to download document")

    file_ext = os.path.splitext(modified_url)[1].lower()
    if file_ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(400, "Unsupported file format")

    return response.content, file_ext.lstrip(".")
