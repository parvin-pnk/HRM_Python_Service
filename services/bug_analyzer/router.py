from fastapi import APIRouter
from services.bug_analyzer.schemas import BugInput, BugAnalysisOutput
from services.bug_analyzer.service import analyze_bug_service
from common.logging_util import log

router = APIRouter(prefix="/ai/bug", tags=["Bug Analyzer"])

@router.post("/analyze", response_model=BugAnalysisOutput)
def analyze_bug(bug: BugInput):
    log.info(
        "Bug analysis request received",
        extra={"payload": bug.model_dump()}
    )
    return analyze_bug_service(bug)
