from pydantic import BaseModel, Field

class TaskInput(BaseModel):
    task_description: str = Field(
        ..., description="Detailed task or ticket description"
    )

class TaskEstimateOutput(BaseModel):
    predicted_effort_hours: float
    complexity_class: str
    complexity_scale_1_10: int
