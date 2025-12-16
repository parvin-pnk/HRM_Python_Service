from typing import Dict, List, Optional, Union
from services.ai_assistant.models import QueryInput, QueryOutput, AIAction
from services.ai_assistant.llm import call_llm_for_intent_extraction
from common.logging_util import log

class AILogic:

    ActionDef = Dict[str, Optional[Union[str, List[AIAction]]]]

    INTENT_TO_SERVICE_MAP: Dict[str, ActionDef] = {
        "check_leave_balance": {
            "reply": "I'll fetch your leave balance.",
            "service": "leave-service",
            "endpoint_template": "/leave/balance/{employee_id}",
            "method": "GET"
        },
        "show_payslip_link": {
            "reply": "I can fetch your latest payslip link.",
            "service": "payroll-service",
            "endpoint_template": "/payroll/payslip/link/{employee_id}",
            "method": "GET"
        },
        "show_attendance_summary": {
            "reply": "Fetching your last month's attendance summary.",
            "service": "attendance-service",
            "endpoint_template": "/attendance/summary/{employee_id}",
            "method": "GET"
        },
        "apply_leave": {
            "reply": "I've detected the intent to apply for leave. Please provide dates if missing.",
            "service": None,
            "endpoint_template": None,
            "method": None
        },
        "general_info": {
            "reply": "I am Sisuni HR Assistant. How can I help you?",
            "service": None,
            "endpoint_template": None,
            "method": None
        }
    }

    def process_query(self, input: QueryInput) -> QueryOutput:
        message = input.message.lower()
        employee_id = input.employee_id

       
        if "leave" in message and "balance" in message:
            log.info("Quick intent match: check_leave_balance")
            return self._response(
                reply="Quick match: fetching your leave balance.",
                intent="check_leave_balance",
                actions=[
                    self._api_action(
                        "leave-service",
                        f"/leave/balance/{employee_id}",
                        "GET"
                    )
                ]
            )

        llm_result = call_llm_for_intent_extraction(input.message)
        intent_info = self.INTENT_TO_SERVICE_MAP.get(
            llm_result.llm_intent,
            self.INTENT_TO_SERVICE_MAP["general_info"]
        )

        actions: List[AIAction] = []
        if intent_info.get("service"):
            endpoint = intent_info["endpoint_template"].format(employee_id=employee_id)
            actions.append(
                self._api_action(
                    intent_info["service"],
                    endpoint,
                    intent_info["method"]
                )
            )

        reply = intent_info["reply"]
        if llm_result.llm_intent == "apply_leave" and llm_result.entities.get("leave_type"):
            reply += f" Detected **{llm_result.entities['leave_type']}** leave."

        return self._response(reply, llm_result.llm_intent, actions)

    def _api_action(self, service: str, endpoint: str, method: str) -> AIAction:
        return AIAction(
            type="CALL_API",
            service=service,
            endpoint=endpoint,
            method=method
        )

    def _response(self, reply: str, intent: str, actions: List[AIAction]) -> QueryOutput:
        return QueryOutput(reply=reply, intent=intent, actions=actions)
