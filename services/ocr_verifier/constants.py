REGEX_PATTERNS = {
    "PAN_CARD": r"^[A-Z]{3}[PCHFALTJG]{1}[A-Z]{1}\d{4}[A-Z]{1}$",
    "AADHAAR_NO": r"^[2-9]{1}[0-9]{11}$",
    "DATE_FORMAT": r"^(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[0-2])[-/.](19|20)\d{2}$"
}

VERIFICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "extracted_fields": {
            "type": "object",
            "properties": {
                "DOCUMENT_HOLDER_NAME": {"type": "string"},
                "PAN_NUMBER": {"type": "string", "nullable": True},
                "AADHAAR_NO": {"type": "string", "nullable": True},
                "DATE_OF_BIRTH": {"type": "string", "nullable": True},
                "GENDER": {"type": "string", "nullable": True},
                "COMPANY_ID": {"type": "string", "nullable": True},
                "GROSS_SALARY": {"type": "string", "nullable": True}
            },
            "required": ["DOCUMENT_HOLDER_NAME"]
        },

        "validation_report": {
            "type": "object",
            "properties": {
                "PAN_REGEX_VALID": {"type": "boolean"},
                "AADHAAR_REGEX_VALID": {"type": "boolean"},
                "DOB_FORMAT_VALID": {"type": "boolean"},
                "LOW_CONFIDENCE_FLAG": {"type": "boolean"}
            },
            "required": ["LOW_CONFIDENCE_FLAG"]
        },

        "verification_status": {
            "type": "string",
            "enum": [
                "VERIFIED_HIGH_CONFIDENCE",
                "FAILED_VALIDATION",
                "FLAGGED_FOR_MANUAL_REVIEW",
                "FAILED_UNKNOWN_DOCUMENT"
            ]
        },

        "fraud_flags": {
            "type": "object",
            "properties": {
                "TAMPERED_TEXT_DETECTED": {"type": "boolean"},
                "MISMATCHED_FONTS": {"type": "boolean"},
                "CONTEXTUAL_ANOMALY_DETECTED": {"type": "boolean"}
            },
            "required": [
                "TAMPERED_TEXT_DETECTED",
                "MISMATCHED_FONTS",
                "CONTEXTUAL_ANOMALY_DETECTED"
            ]
        },

        "confidence_score": {
            "type": "number"
        }
    },
    "required": [
        "extracted_fields",
        "validation_report",
        "verification_status",
        "fraud_flags",
        "confidence_score"
    ]
}
