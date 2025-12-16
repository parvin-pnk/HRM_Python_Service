

from pydantic import BaseModel, Field

from typing import Optional, Dict, Any, List 


class QueryInput(BaseModel):
    tenant_id: str
    employee_id: str
    message: str 

class BaseResponse(BaseModel):
    success: bool
    error: Optional[str] = None

class AIAction(BaseModel):
    type: str 
    service: str
    endpoint: str
    method: str 

class QueryOutput(BaseModel):
    reply: str
    intent: str
    actions: List[AIAction] 

class ActionInput(BaseModel):
    tenant_id: str
    employee_id: str
    intent: str
    action_data: Optional[Dict[str, Any]] = None

class ActionOutput(BaseResponse):
    status_code: int
    message: str
    backend_response: Optional[Dict[str, Any]] = None


class LLMIntentExtraction(BaseModel):
   
    llm_intent: str = Field(..., description="The high-level intent detected.")
   
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities like 'leave_type', 'start_date', 'employee_id', etc.")
    confidence_score: float = Field(default=1.0, description="Confidence level of the detection.")