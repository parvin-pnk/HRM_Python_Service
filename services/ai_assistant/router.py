from fastapi import APIRouter, HTTPException
from services.ai_assistant.models import (
    QueryInput, QueryOutput, ActionInput, ActionOutput, BaseResponse
)
from services.ai_assistant.service import AILogic
from common.logging_util import log
from common.http_client import java_client

router = APIRouter(prefix="/ai", tags=["AI Assistant"])
ai_logic = AILogic()

@router.get("/health")
def health():
    return {"status": "UP", "service": "ai_assistant"}

@router.post("/query", response_model=QueryOutput)
def handle_query(input: QueryInput):
    log.info("AI query received", extra={"payload":input.model_dump()})
    return ai_logic.process_query(input)

@router.post("/action", response_model=ActionOutput)
def execute_action(input: ActionInput):
    action_map = {
        "apply_leave": ("/leave/apply", "POST"),
        "check_leave_balance": (f"/leave/balance/{input.employee_id}", "GET"),
        "show_payslip_link": (f"/payroll/payslip/link/{input.employee_id}", "GET"),
        "show_attendance_summary": (f"/attendance/summary/{input.employee_id}", "GET"),
    }

    if input.intent not in action_map:
        raise HTTPException(
            status_code=400,
            detail=BaseResponse(success=False, error="Unknown intent").model_dump()
        )

    endpoint, method = action_map[input.intent]

    backend_response = java_client.call_api(
        method=method,
        endpoint=endpoint,
        json=input.action_data if method == "POST" else None
    )

    return ActionOutput(
        success=True,
        status_code=200,
        message="Action executed successfully",
        backend_response=backend_response
    )
