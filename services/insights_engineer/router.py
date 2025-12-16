from fastapi import APIRouter
from services.insights_engineer.schemas import EmployeeInput
from services.insights_engineer.service import (
    predict_attrition_service,
    predict_performance_service,
    get_hr_insights_service
)
from common.logging_util import log

router = APIRouter(prefix="/ai", tags=["HR Insights"])

@router.post("/prediction/attrition")
def predict_attrition(input_data: EmployeeInput):
    log.info("Attrition prediction request", extra={"payload": input_data.model_dump()})
    return predict_attrition_service(input_data)

@router.post("/prediction/performance")
def predict_performance(input_data: EmployeeInput):
    log.info("Performance prediction request", extra={"payload": input_data.model_dump()})
    return predict_performance_service(input_data)

@router.get("/insights/hr")
def hr_insights():
    log.info("HR insights requested")
    return get_hr_insights_service()
