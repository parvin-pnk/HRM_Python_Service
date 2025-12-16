from pydantic import BaseModel, Field
from typing import List

class TaskData(BaseModel):
    id: int
    title: str
    effort_hours: float = Field(..., description="Estimated effort")
    priority: int = Field(..., description="Business priority (1–10)")

class SprintPlanInput(BaseModel):
    available_tasks: List[TaskData]
    historical_velocity: List[float]
    team_capacity_raw: float

class SprintPlanOutput(BaseModel):
    team_velocity_prediction: float
    total_effort_planned: float
    predicted_success_rate: float
    planned_tasks: List[dict]
