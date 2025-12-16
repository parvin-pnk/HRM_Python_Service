from fastapi import APIRouter, HTTPException
from services.sprint_planner.schemas import (
    SprintPlanInput,
    SprintPlanOutput
)
from services.sprint_planner.service import plan_sprint_service

router = APIRouter(
    prefix="/ai/sprint",
    tags=["Sprint Planner"]
)

@router.post("/plan", response_model=SprintPlanOutput)
def plan_sprint(data: SprintPlanInput):
    try:
        return SprintPlanOutput(**plan_sprint_service(data))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sprint planning failed: {e}"
        )
