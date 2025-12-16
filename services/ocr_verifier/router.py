from fastapi import APIRouter
from services.ocr_verifier.schemas import DocumentInput, VerificationResponse
from services.ocr_verifier.service import verify_document_service

router = APIRouter(prefix="/ai/document", tags=["OCR Verifier"])

@router.get("/health")
def health():
    return {"status": "UP", "service": "ocr_verifier"}

@router.post("/verify", response_model=VerificationResponse)
async def verify_document(input_data: DocumentInput):
    return await verify_document_service(input_data)
