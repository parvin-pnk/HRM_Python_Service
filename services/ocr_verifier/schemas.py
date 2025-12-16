from pydantic import BaseModel
from typing import Dict, Any

class DocumentInput(BaseModel):
    tenant_id: str
    doc_url: str
    document_type: str

class VerificationResponse(BaseModel):
    tenant_id: str
    document_type_input: str
    verification_status: str
    extraction_method: str
    ocr_engine_accuracy_score: float
    extracted_fields: Dict[str, Any]
    fraud_detection_flags: Dict[str, Any]
    validation_report: Dict[str, Any]
