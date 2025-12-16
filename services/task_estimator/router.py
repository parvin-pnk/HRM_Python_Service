from fastapi import APIRouter, HTTPException
from services.task_estimator.schemas import TaskInput, TaskEstimateOutput
from services.task_estimator.service import estimate_task_service

router = APIRouter(
    prefix="/ai/task",
    tags=["Task Estimator"]
)

@router.post("/estimate", response_model=TaskEstimateOutput)
def estimate_task(task: TaskInput):
    try:
        return estimate_task_service(task)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Task effort estimation failed: {e}"
        )
