from services.ocr_verifier.downloader import download_document
from services.ocr_verifier.extractor import extract_raw_text
from services.ocr_verifier.gemini_client import verify_with_gemini

async def verify_document_service(input_data):
    file_bytes, ext = download_document(input_data.doc_url)
    raw_text = extract_raw_text(file_bytes, ext)

    gemini_report = await verify_with_gemini(raw_text, input_data.document_type)

    return {
        "tenant_id": input_data.tenant_id,
        "document_type_input": input_data.document_type,
        "verification_status": gemini_report["verification_status"],
        "extraction_method": ext.upper(),
        "ocr_engine_accuracy_score": gemini_report.get("confidence_score", 99.9),
        "extracted_fields": gemini_report["extracted_fields"],
        "fraud_detection_flags": gemini_report["fraud_flags"],
        "validation_report": gemini_report["validation_report"]
    }
