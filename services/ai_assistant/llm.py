from services.ai_assistant.models import LLMIntentExtraction

def call_llm_for_intent_extraction(message: str) -> LLMIntentExtraction:
    message_lower = message.lower()

    if "i want to take my annual leave" in message_lower:
        return LLMIntentExtraction(
            llm_intent="apply_leave",
            entities={"leave_type": "annual"},
            confidence_score=0.95
        )

    if "how many sick days do i have left" in message_lower:
        return LLMIntentExtraction(
            llm_intent="check_leave_balance",
            entities={"leave_type": "sick"},
            confidence_score=0.98
        )

    if any(k in message_lower for k in ["paycheck", "salary slip"]):
        return LLMIntentExtraction(
            llm_intent="show_payslip_link",
            entities={"timeframe": "latest"},
            confidence_score=0.90
        )

    if "attendance summary" in message_lower:
        return LLMIntentExtraction(
            llm_intent="show_attendance_summary",
            entities={},
            confidence_score=0.90
        )

    return LLMIntentExtraction(
        llm_intent="general_info",
        entities={},
        confidence_score=0.5
    )
